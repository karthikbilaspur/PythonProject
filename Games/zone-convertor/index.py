import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timezone
from typing import Literal
from zoneinfo import ZoneInfo, available_timezones

# --- Curated list: most-used zones first, easy to scan ---
CURATED = [
    "UTC",
    "US/Pacific", "US/Mountain", "US/Central", "US/Eastern",
    "America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles",
    "America/Mexico_City", "America/Sao_Paulo", "America/Toronto",
    "Europe/London", "Europe/Paris", "Europe/Berlin", "Europe/Moscow",
    "Africa/Cairo", "Africa/Lagos",
    "Asia/Dubai", "Asia/Kolkata", "Asia/Dhaka", "Asia/Bangkok",
    "Asia/Singapore", "Asia/Hong_Kong", "Asia/Shanghai", "Asia/Tokyo", "Asia/Seoul",
    "Australia/Sydney", "Australia/Melbourne", "Pacific/Auckland",
]

ALL_ZONES = sorted(available_timezones())


def describe_dst_issue(
    dt_naive: datetime, tz: ZoneInfo
) -> (
    tuple[Literal["ok"], None]
    | tuple[Literal["nonexistent"], str]
    | tuple[Literal["ambiguous"], tuple[datetime, datetime]]
):
    """
    Detect DST edge cases for a naive wall time in a zoneinfo zone.
    Returns: ("ok", None) | ("nonexistent", msg) | ("ambiguous", (fold0, fold1))
    zoneinfo doesn't raise like pytz, so we detect by round-tripping.
    """
    # Non-existent: wall time -> UTC -> back gives a different wall time
    aware = dt_naive.replace(tzinfo=tz)
    back = aware.astimezone(timezone.utc).astimezone(tz).replace(tzinfo=None)
    if back != dt_naive:
        return ("nonexistent",
                f"{dt_naive.strftime('%Y-%m-%d %H:%M')} does not exist in {tz.key} "
                f"(clocks jump forward for DST). Try a time 1 hour later.")

    # Ambiguous: fold=0 and fold=1 give different UTC offsets
    fold0 = dt_naive.replace(tzinfo=tz, fold=0)
    fold1 = dt_naive.replace(tzinfo=tz, fold=1)
    if fold0.utcoffset() != fold1.utcoffset():
        return ("ambiguous", (fold0, fold1))

    return ("ok", None)


class TimezoneConverter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Timezone Converter")
        self.window.minsize(520, 340)
        self.window.resizable(True, False)

        self.show_all = tk.BooleanVar(value=False)
        self.ambiguous_choice = tk.StringVar(value="first")  # for DST fall-back

        self._build_ui()
        self._set_now()

    # ---------- UI ----------
    def _build_ui(self):
        frame = ttk.Frame(self.window, padding=16)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        # From
        ttk.Label(frame, text="From:").grid(row=0, column=0, sticky="w", padx=5, pady=6)
        self.from_tz = tk.StringVar(value="Asia/Kolkata")
        self.from_combo = ttk.Combobox(frame, textvariable=self.from_tz,
                                        values=CURATED, width=32)
        self.from_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=6)
        self.from_combo.bind("<<ComboboxSelected>>", lambda e: self._update_result_hint())

        # To
        ttk.Label(frame, text="To:").grid(row=1, column=0, sticky="w", padx=5, pady=6)
        self.to_tz = tk.StringVar(value="US/Eastern")
        self.to_combo = ttk.Combobox(frame, textvariable=self.to_tz,
                                      values=CURATED, width=32)
        self.to_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=6)

        # Show all toggle + filter hint
        ttk.Checkbutton(frame, text="Show all timezones (searchable)",
                        variable=self.show_all,
                        command=self._toggle_zone_list).grid(
                            row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        ttk.Label(frame, text="Tip: type in the box to filter, e.g. 'Kolkata' or 'London'",
                  foreground="gray").grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=2)

        # Datetime entry
        ttk.Label(frame, text="Date and Time:").grid(row=4, column=0, sticky="w", padx=5, pady=6)
        self.datetime_entry = ttk.Entry(frame, width=32)
        self.datetime_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=6)
        self.datetime_entry.bind("<Return>", lambda e: self.convert_time())

        # DST ambiguous choice (only shown when needed)
        self.dst_frame = ttk.Frame(frame)
        self.dst_frame.grid(row=5, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        ttk.Label(self.dst_frame, text="This time occurs twice (DST fall-back):").pack(side="left")
        ttk.Radiobutton(self.dst_frame, text="First occurrence", variable=self.ambiguous_choice,
                        value="first", command=self.convert_time).pack(side="left", padx=(8, 4))
        ttk.Radiobutton(self.dst_frame, text="Second occurrence", variable=self.ambiguous_choice,
                        value="second", command=self.convert_time).pack(side="left")
        self.dst_frame.grid_remove()

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=12)
        ttk.Button(btn_frame, text="Convert", command=self.convert_time).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Swap ⇅", command=self.swap).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Now", command=self._set_now).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Copy Result", command=self.copy_result).pack(side="left", padx=4)

        # Result
        self.result_var = tk.StringVar(value="")
        self.result_label = ttk.Label(frame, textvariable=self.result_var,
                                      wraplength=480, font=("", 11, "bold"))
        self.result_label.grid(row=7, column=0, columnspan=2, sticky="w", padx=5, pady=8)

        self.error_var = tk.StringVar(value="")
        ttk.Label(frame, textvariable=self.error_var, foreground="red",
                  wraplength=480).grid(row=8, column=0, columnspan=2, sticky="w", padx=5)

        # Live filtering for comboboxes
        for combo in (self.from_combo, self.to_combo):
            combo.bind("<KeyRelease>", lambda e, c=combo: self._filter_combo(c))

    # ---------- Helpers ----------
    def _zone_list(self):
        return ALL_ZONES if self.show_all.get() else CURATED

    def _toggle_zone_list(self):
        values = self._zone_list()
        self.from_combo["values"] = values
        self.to_combo["values"] = values

    def _filter_combo(self, combo: ttk.Combobox):
        typed = combo.get().strip().lower()
        if not typed:
            combo["values"] = self._zone_list()
            return
        matches = [z for z in self._zone_list() if typed in z.lower()]
        # Keep what user typed, show matches as dropdown
        combo["values"] = matches if matches else self._zone_list()

    def _set_now(self):
        # Now in the From timezone
        try:
            tz = ZoneInfo(self.from_tz.get())
        except Exception:
            tz = timezone.utc
        now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        self.datetime_entry.delete(0, tk.END)
        self.datetime_entry.insert(0, now)
        self._update_result_hint()

    def _update_result_hint(self):
        self.error_var.set("")

    def swap(self):
        a, b = self.from_tz.get(), self.to_tz.get()
        self.from_tz.set(b)
        self.to_tz.set(a)
        self.convert_time()

    def copy_result(self):
        text = self.result_var.get()
        if not text:
            return
        self.window.clipboard_clear()
        self.window.clipboard_append(text)
        self.error_var.set("Copied to clipboard.")

    # ---------- Core ----------
    def convert_time(self):
        self.error_var.set("")
        self.dst_frame.grid_remove()
        raw = self.datetime_entry.get().strip()
        from_name = self.from_tz.get().strip()
        to_name = self.to_tz.get().strip()

        # Parse - accept "YYYY-MM-DD HH:MM:SS" or "YYYY-MM-DD HH:MM"
        dt_naive = None
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                dt_naive = datetime.strptime(raw, fmt)
                break
            except ValueError:
                continue
        if dt_naive is None:
            self.result_var.set("")
            self.error_var.set("Use format YYYY-MM-DD HH:MM:SS  (e.g. 2026-11-27 15:30:00)")
            return

        try:
            from_tz = ZoneInfo(from_name)
        except Exception:
            self.result_var.set("")
            self.error_var.set(f"Unknown 'From' timezone: {from_name!r}. Pick one from the list.")
            return
        try:
            to_tz = ZoneInfo(to_name)
        except Exception:
            self.result_var.set("")
            self.error_var.set(f"Unknown 'To' timezone: {to_name!r}. Pick one from the list.")
            return

        status, info = describe_dst_issue(dt_naive, from_tz)

        if status == "nonexistent" and isinstance(info, str):
            self.result_var.set("")
            self.error_var.set(info)
            return

        if status == "ambiguous":
            # Show the choice, use it
            self.dst_frame.grid()
            fold = 0 if self.ambiguous_choice.get() == "first" else 1
            from_time = dt_naive.replace(tzinfo=from_tz, fold=fold)
            label = " (first occurrence)" if fold == 0 else " (second occurrence)"
        else:
            from_time = dt_naive.replace(tzinfo=from_tz)
            label = ""

        to_time = from_time.astimezone(to_tz)
        result = (f"{dt_naive.strftime('%Y-%m-%d %H:%M:%S')} {from_name}{label}  →  "
                  f"{to_time.strftime('%Y-%m-%d %H:%M:%S')} {to_name}")
        self.result_var.set(result)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    TimezoneConverter().run()