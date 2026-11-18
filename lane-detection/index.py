import cv2
import numpy as np
from numpy.typing import NDArray
from collections import deque
import math
import time


class AdvancedLaneDetector:
    def __init__(self, history_len: int = 15) -> None:
        self.left_fit_history: deque[NDArray[np.float64]] = deque(maxlen=history_len)
        self.right_fit_history: deque[NDArray[np.float64]] = deque(maxlen=history_len)
        self.left_fit: NDArray[np.float64] | None = None
        self.right_fit: NDArray[np.float64] | None = None

        # Real-world conversions - tune for your camera
        # 30m of road in 720px height, 3.7m lane width in ~700px width
        self.ym_per_pix = 30 / 720
        self.xm_per_pix = 3.7 / 700

        self.frame_count = 0
        self.lost_frames = 0

    # --------- 1. Perspective Transform ----------
    def _get_perspective_matrices(
        self, w: int, h: int
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        # Source: trapezoid in original image
        src: NDArray[np.float32] = np.array([
            [w * 0.43, h * 0.65],  # top-left
            [w * 0.57, h * 0.65],  # top-right
            [w * 0.95, h],         # bottom-right
            [w * 0.05, h],         # bottom-left
        ], dtype=np.float32)
        # Destination: rectangle in warped image
        dst: NDArray[np.float32] = np.array([
            [w * 0.20, 0],
            [w * 0.80, 0],
            [w * 0.80, h],
            [w * 0.20, h],
        ], dtype=np.float32)
        M = np.asarray(cv2.getPerspectiveTransform(src, dst), dtype=np.float64)
        Minv = np.asarray(cv2.getPerspectiveTransform(dst, src), dtype=np.float64)
        return M, Minv

    # ---------- 2. Thresholding ----------
    def _threshold(self, image: NDArray[np.uint8]) -> NDArray[np.uint8]:
        hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        # White: high Lightness
        white = cv2.inRange(hls, np.array([0, 200, 0]), np.array([255, 255, 255]))
        # Yellow: Hue ~20, high Saturation
        yellow = cv2.inRange(hls, np.array([15, 30, 115]), np.array([35, 204, 255]))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Sobel X
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        abs_sobel = np.absolute(sobelx)
        scaled: NDArray[np.uint8] = np.asarray(
            255 * abs_sobel / (np.max(abs_sobel) + 1e-6), dtype=np.uint8
        )
        sobel_binary = cv2.inRange(scaled, 30, 255)

        combined = cv2.bitwise_or(white, yellow)
        combined = cv2.bitwise_or(combined, sobel_binary)
        return np.asarray(combined, dtype=np.uint8)

    def threshold(self, image: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """Public alias for thresholding compatibility."""
        return self._threshold(image)

    # ---------- 3. Sliding Window ----------
    def _sliding_window(
        self, binary_warped: NDArray[np.uint8]
    ) -> tuple[
        NDArray[np.int64],
        NDArray[np.int64],
        NDArray[np.int64],
        NDArray[np.int64],
    ]:
        h, w = binary_warped.shape
        histogram = np.sum(binary_warped[h // 2:, :], axis=0)

        midpoint = w // 2
        left_base = np.argmax(histogram[:midpoint])
        right_base = np.argmax(histogram[midpoint:]) + midpoint

        nwindows = 9
        window_height = h // nwindows
        margin = 100
        minpix = 50

        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        left_current = left_base
        right_current = right_base

        left_inds: list[NDArray[np.intp]] = []
        right_inds: list[NDArray[np.intp]] = []

        for window in range(nwindows):
            win_y_low = h - (window + 1) * window_height
            win_y_high = h - window * window_height

            win_xleft_low = left_current - margin
            win_xleft_high = left_current + margin
            win_xright_low = right_current - margin
            win_xright_high = right_current + margin

            good_left = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) &
                         (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
            good_right = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) &
                          (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]

            left_inds.append(good_left)
            right_inds.append(good_right)

            if len(good_left) > minpix:
                left_current = int(np.mean(nonzerox[good_left]))
            if len(good_right) > minpix:
                right_current = int(np.mean(nonzerox[good_right]))

        left_inds_array: NDArray[np.intp] = (
            np.concatenate(left_inds) if left_inds else np.empty(0, dtype=np.intp)
        )
        right_inds_array: NDArray[np.intp] = (
            np.concatenate(right_inds) if right_inds else np.empty(0, dtype=np.intp)
        )

        leftx = nonzerox[left_inds_array] if len(left_inds_array) > 0 else np.array([])
        lefty = nonzeroy[left_inds_array] if len(left_inds_array) > 0 else np.array([])
        rightx = nonzerox[right_inds_array] if len(right_inds_array) > 0 else np.array([])
        righty = nonzeroy[right_inds_array] if len(right_inds_array) > 0 else np.array([])

        return leftx, lefty, rightx, righty

    def _search_around_poly(
        self,
        binary_warped: NDArray[np.uint8],
        left_fit: NDArray[np.float64],
        right_fit: NDArray[np.float64],
    ) -> tuple[NDArray[np.intp], NDArray[np.intp], NDArray[np.intp], NDArray[np.intp]]:
        """Faster: search only near previous polynomial (for video)."""
        margin = 80
        nonzero = binary_warped.nonzero()
        nonzeroy: NDArray[np.intp] = np.asarray(nonzero[0], dtype=np.intp)
        nonzerox: NDArray[np.intp] = np.asarray(nonzero[1], dtype=np.intp)

        left_lane = ((nonzerox > (left_fit[0] * nonzeroy**2 + left_fit[1] * nonzeroy + left_fit[2] - margin)) &
                     (nonzerox < (left_fit[0] * nonzeroy**2 + left_fit[1] * nonzeroy + left_fit[2] + margin)))
        right_lane = ((nonzerox > (right_fit[0] * nonzeroy**2 + right_fit[1] * nonzeroy + right_fit[2] - margin)) &
                      (nonzerox < (right_fit[0] * nonzeroy**2 + right_fit[1] * nonzeroy + right_fit[2] + margin)))

        return nonzerox[left_lane], nonzeroy[left_lane], nonzerox[right_lane], nonzeroy[right_lane]

    def _fit_poly(
        self,
        leftx: NDArray[np.intp],
        lefty: NDArray[np.intp],
        rightx: NDArray[np.intp],
        righty: NDArray[np.intp],
    ) -> tuple[NDArray[np.float64] | None, NDArray[np.float64] | None]:
        left_fit: NDArray[np.float64] | None = (
            np.asarray(np.polyfit(lefty, leftx, 2), dtype=np.float64)
            if len(leftx) > 200
            else None
        )
        right_fit: NDArray[np.float64] | None = (
            np.asarray(np.polyfit(righty, rightx, 2), dtype=np.float64)
            if len(rightx) > 200
            else None
        )
        return left_fit, right_fit

    def _smooth_fit(
        self,
        history: deque[NDArray[np.float64]],
        new_fit: NDArray[np.float64] | None,
    ) -> NDArray[np.float64] | None:
        if new_fit is not None:
            # Sanity check: don't accept crazy jumps
            if history:
                prev = np.mean(history, axis=0)
                if np.max(np.abs(new_fit - prev)) > 0.005 and len(history) > 5:
                    # Too big a jump, likely false detection - keep old
                    return prev
            history.append(new_fit)
        if not history:
            return None
        return np.mean(history, axis=0)

    # ---------- 4. Metrics ----------
    def _curvature_and_offset(
        self,
        left_fit: NDArray[np.float64],
        right_fit: NDArray[np.float64],
        h: int,
        w: int,
    ) -> tuple[float, float]:
        y_eval = h  # bottom of image
        # Convert to real-world meters
        y_points: NDArray[np.float64] = np.asarray(
            [0, h // 2, h], dtype=np.float64
        )
        y_points_cr = y_points * self.ym_per_pix

        left_x_points = (
            left_fit[0] * y_points**2
            + left_fit[1] * y_points
            + left_fit[2]
        ) * self.xm_per_pix
        right_x_points = (
            right_fit[0] * y_points**2
            + right_fit[1] * y_points
            + right_fit[2]
        ) * self.xm_per_pix

        left_fit_cr: NDArray[np.float64] = np.asarray(
            np.polyfit(y_points_cr, left_x_points, 2), dtype=np.float64
        )
        right_fit_cr: NDArray[np.float64] = np.asarray(
            np.polyfit(y_points_cr, right_x_points, 2), dtype=np.float64
        )
        # Radius = (1 + (2Ay + B)^2)^1.5 / |2A|
        left_curv = ((1 + (2 * left_fit_cr[0] * y_eval * self.ym_per_pix + left_fit_cr[1])**2)**1.5) / abs(2 * left_fit_cr[0] + 1e-6)
        right_curv = ((1 + (2 * right_fit_cr[0] * y_eval * self.ym_per_pix + right_fit_cr[1])**2)**1.5) / abs(2 * right_fit_cr[0] + 1e-6)
        curvature = (left_curv + right_curv) / 2

        # Vehicle offset: center of car vs center of lane
        left_x = left_fit[0] * y_eval**2 + left_fit[1] * y_eval + left_fit[2]
        right_x = right_fit[0] * y_eval**2 + right_fit[1] * y_eval + right_fit[2]
        lane_center = (left_x + right_x) / 2
        car_center = w / 2
        offset_m = (car_center - lane_center) * self.xm_per_pix  # + = car is right of center
        return curvature, offset_m

    def _steering_angle(
        self,
        left_fit: NDArray[np.float64] | None,
        right_fit: NDArray[np.float64] | None,
        h: int,
        w: int,
    ) -> float:
        """Simple: look ahead 1/3 up, steer toward lane center."""
        if left_fit is None or right_fit is None:
            return 0.0
        y_lookahead = int(h * 0.65)
        left_x = left_fit[0] * y_lookahead**2 + left_fit[1] * y_lookahead + left_fit[2]
        right_x = right_fit[0] * y_lookahead**2 + right_fit[1] * y_lookahead + right_fit[2]
        lane_center = (left_x + right_x) / 2
        error_px = lane_center - (w / 2)
        # P-controller: 0.08 deg per pixel, clamp to +-25 deg
        angle = float(np.clip(error_px * 0.08, -25, 25))
        return angle

    # ---------- 5. Main ----------
    def detect(self, image: NDArray[np.uint8]) -> NDArray[np.uint8]:
        start = time.time()
        h, w = image.shape[:2]
        self.frame_count += 1

        binary = self._threshold(image)
        M, Minv = self._get_perspective_matrices(w, h)
        warped: NDArray[np.uint8] = np.asarray(
            cv2.warpPerspective(binary, M, (w, h), flags=cv2.INTER_LINEAR),
            dtype=np.uint8,
        )

        # Choose detection method
        if self.left_fit is None or self.right_fit is None or self.lost_frames > 5:
            leftx, lefty, rightx, righty = self._sliding_window(warped)
        else:
            leftx, lefty, rightx, righty = self._search_around_poly(warped, self.left_fit, self.right_fit)

        left_fit_new, right_fit_new = self._fit_poly(leftx, lefty, rightx, righty)

        # Sanity: lane width should be ~500-900px in warped view
        if left_fit_new is not None and right_fit_new is not None:
            y_eval = h
            lx = left_fit_new[0] * y_eval**2 + left_fit_new[1] * y_eval + left_fit_new[2]
            rx = right_fit_new[0] * y_eval**2 + right_fit_new[1] * y_eval + right_fit_new[2]
            if not (400 < (rx - lx) < 1000):
                left_fit_new, right_fit_new = None, None
                self.lost_frames += 1
            else:
                self.lost_frames = 0
        else:
            self.lost_frames += 1

        self.left_fit = self._smooth_fit(self.left_fit_history, left_fit_new)
        self.right_fit = self._smooth_fit(self.right_fit_history, right_fit_new)

        # --- Draw ---
        result = image.copy()

        if self.left_fit is not None and self.right_fit is not None:
            # Draw lane polygon in warped space, then unwarp
            ploty = np.linspace(0, h - 1, h)
            left_fitx = self.left_fit[0] * ploty**2 + self.left_fit[1] * ploty + self.left_fit[2]
            right_fitx = self.right_fit[0] * ploty**2 + self.right_fit[1] * ploty + self.right_fit[2]

            warp_zero = np.zeros_like(warped)
            color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

            pts_left = np.column_stack((left_fitx, ploty))
            pts_right = np.flipud(np.column_stack((right_fitx, ploty)))
            pts = np.vstack((pts_left, pts_right)).astype(np.int32)

            curvature, offset = self._curvature_and_offset(self.left_fit, self.right_fit, h, w)
            steering = self._steering_angle(self.left_fit, self.right_fit, h, w)

            # Lane departure: offset > 0.4m = danger
            departing = abs(offset) > 0.45
            lane_color = (0, 0, 255) if departing else (0, 255, 0)  # BGR: red if departing

            cv2.fillPoly(color_warp, [pts], lane_color)
            newwarp = cv2.warpPerspective(color_warp, Minv, (w, h))
            result = cv2.addWeighted(result, 1, newwarp, 0.3, 0)

            # Draw lane lines
            for fitx in [left_fitx, right_fitx]:
                pts_line = np.array([np.transpose(np.vstack([fitx, ploty]))], dtype=np.int32)
                cv2.polylines(result, [pts_line], False, (255, 0, 0), 8)  # need unwarp? use warped->unwarp trick
            # Re-draw correctly via unwarp:
            # (simpler: draw lines in warped, unwarp, overlay)
            line_warp = np.zeros_like(color_warp)
            cv2.polylines(line_warp, [pts_left.astype(np.int32).reshape(-1, 1, 2)], False, (255, 255, 0), 15)
            cv2.polylines(line_warp, [pts_right.astype(np.int32).reshape(-1, 1, 2)], False, (255, 255, 0), 15)
            line_unwarp = cv2.warpPerspective(line_warp, Minv, (w, h))
            result = cv2.addWeighted(result, 1, line_unwarp, 0.8, 0)

            # HUD
            result = np.asarray(result, dtype=np.uint8)
            self._draw_hud(result, curvature, offset, steering, departing, time.time() - start)
        else:
            cv2.putText(result, "LANE LOST - Searching...", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            cv2.putText(result, f"FPS: {1 / max(time.time() - start, 1e-3):.1f}", (20, 75),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        return np.asarray(result, dtype=np.uint8)

    def _draw_hud(self, img: NDArray[np.uint8], curvature: float, offset: float,
                  steering: float, departing: bool, dt: float) -> None:
        h, w = img.shape[:2]
        # Semi-transparent panel
        overlay = img.copy()
        cv2.rectangle(overlay, (10, 10), (360, 150), (0, 0, 0), -1)
        img[:] = cv2.addWeighted(overlay, 0.6, img, 0.4, 0)

        direction = "Left" if offset > 0.1 else "Right" if offset < -0.1 else "Center"
        fps = 1 / max(dt, 1e-3)

        texts = [
            f"Curvature: {curvature:.0f} m",
            f"Offset: {abs(offset):.2f} m {direction}",
            f"Steering: {steering:+.1f} deg",
            f"FPS: {fps:.1f}",
        ]
        for i, t in enumerate(texts):
            cv2.putText(img, t, (20, 40 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if departing:
            cv2.putText(img, "!!! LANE DEPARTURE !!!", (w // 2 - 220, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
            # Flash border
            if self.frame_count % 20 < 10:
                cv2.rectangle(img, (0, 0), (w - 1, h - 1), (0, 0, 255), 15)

        # Steering wheel indicator - bottom center
        cx, cy = w // 2, h - 60
        cv2.circle(img, (cx, cy), 45, (255, 255, 255), 2)
        rad = math.radians(steering)
        end_x = int(cx + 40 * math.sin(rad))
        end_y = int(cy - 40 * math.cos(rad))
        cv2.line(img, (cx, cy), (end_x, end_y), (0, 255, 255), 4)

def run_video(
    video_path: int | str = 0,
    save_path: str | None = None,
    show_debug: bool = False,
) -> None:
    detector = AdvancedLaneDetector()
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Cannot open: {video_path}")
        return

    writer = None
    if save_path:
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
        video_writer_fourcc = getattr(cv2, "VideoWriter_fourcc")
        writer = cv2.VideoWriter(save_path, video_writer_fourcc(*"mp4v"), fps, (w, h))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out = detector.detect(np.asarray(frame, dtype=np.uint8))
        if writer:
            writer.write(out)
        cv2.imshow('Advanced Lane Detection - Q to quit', out)
        if show_debug:
            # Show bird's-eye view for tuning
            binary = detector.threshold(np.asarray(frame, dtype=np.uint8))
            frame_w, frame_h = frame.shape[1], frame.shape[0]
            src = np.array([
                [frame_w * 0.43, frame_h * 0.65],
                [frame_w * 0.57, frame_h * 0.65],
                [frame_w * 0.95, frame_h],
                [frame_w * 0.05, frame_h],
            ], dtype=np.float32)
            dst = np.array([
                [frame_w * 0.20, 0],
                [frame_w * 0.80, 0],
                [frame_w * 0.80, frame_h],
                [frame_w * 0.20, frame_h],
            ], dtype=np.float32)
            M = cv2.getPerspectiveTransform(src, dst)
            warped = cv2.warpPerspective(binary, M, (frame_w, frame_h))
            cv2.imshow('Bird Eye (debug)', warped)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Test on video file:
    # run_video('challenge_video.mp4', save_path='output.mp4', show_debug=True)

    # Webcam:
    run_video(0)