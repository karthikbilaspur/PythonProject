import cv2, numpy as np
COLOR_RANGES=[[5,107,0,19,255,255],[133,56,0,159,156,255],[57,76,0,100,255,255],[90,48,0,118,255,255]]
COLOR_VALUES=[[51,153,255],[255,0,255],[0,255,0],[255,0,0]]; NAMES=["Orange","Purple","Green","Blue"]
class ColorTracker:
 def __init__(self): self.points: list[list[int]]=[]
 def find_color(self,img: cv2.typing.MatLike) -> list[list[int]]:
  hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV); pts: list[list[int]]=[]
  for i,cr in enumerate(COLOR_RANGES):
   mask=cv2.inRange(hsv,np.array(cr[:3]),np.array(cr[3:])); x,y=self.get_contours(mask)
   if x!=0 and y!=0: pts.append([x,y,i]); cv2.circle(img,(x,y),15,COLOR_VALUES[i],cv2.FILLED); cv2.putText(img,NAMES[i],(x+20,y),cv2.FONT_HERSHEY_SIMPLEX,0.6,COLOR_VALUES[i],2)
  return pts
 def get_contours(self,img: cv2.typing.MatLike) -> tuple[int, int]:
  contours,_=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); x,y,best=0,0,0
  for cnt in contours:
   area=cv2.contourArea(cnt)
   if area>500 and area>best:
    best=area; peri=cv2.arcLength(cnt,True); approx=cv2.approxPolyDP(cnt,0.02*peri,True); bx,by,bw,bh=cv2.boundingRect(approx); x,y=bx+bw//2,by+bh//2
  return x,y
 def draw(self,img: cv2.typing.MatLike) -> None:
  for p in self.points: cv2.circle(img,(p[0],p[1]),10,COLOR_VALUES[p[2]],cv2.FILLED)
 def run_camera(self):
  cap=cv2.VideoCapture(0); cap.set(3,640); cap.set(4,480)
  print("Press Q to quit, C to clear")
  while True:
   ok,img=cap.read()
   if not ok: break
   res=img.copy(); self.points.extend(self.find_color(img)); self.draw(res); cv2.imshow("Color Tracker",res)
   k=cv2.waitKey(1)&0xFF
   if k==ord("q"): break
   if k==ord("c"): self.points.clear()
  cap.release(); cv2.destroyAllWindows()
def open_window(_parent: object | None = None):
 import threading; threading.Thread(target=ColorTracker().run_camera,daemon=True).start(); print("Camera started - Q to quit, C to clear")
if __name__=="__main__": ColorTracker().run_camera()
