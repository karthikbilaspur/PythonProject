"""
Queue Lab - All 4 Queues in ONE Visual App
Combines: DynamicQueue (Linked List) + LinearQueue + CircularQueue + PriorityQueue
Run: python index.py
Stdlib only - no pip needed.
"""
from typing import Callable, Optional, Protocol, Union
import tkinter as tk
from tkinter import ttk, messagebox


class Queue(Protocol):
    name: str
    capacity: Optional[int]
    grows: bool

    def enqueue(self, v: int) -> bool: ...
    def dequeue(self) -> Optional[int]: ...
    def peek(self) -> Optional[int]: ...
    def snapshot(self) -> list[Optional[int]]: ...
    def __len__(self) -> int: ...


# ---------- Core queue classes (logic separated from UI) ----------
class DynamicQueue:
    name = "Dynamic (Linked List)"
    capacity: Optional[int] = None
    grows = True

    def __init__(self) -> None:
        self.items: list[int] = []

    def enqueue(self, v: int) -> bool:
        self.items.append(v)
        return True

    def dequeue(self) -> Optional[int]:
        return self.items.pop(0) if self.items else None

    def peek(self) -> Optional[int]:
        return self.items[0] if self.items else None

    def snapshot(self) -> list[Optional[int]]:
        return list(self.items)

    def __len__(self) -> int:
        return len(self.items)


class LinearQueue:
    name = "Linear (Array)"
    grows = False

    def __init__(self, size: int = 8) -> None:
        self.size = size
        self.items: list[Optional[int]] = [None] * size
        self.front = 0
        self.rear = -1

    @property
    def capacity(self) -> int:
        return self.size

    def is_full(self) -> bool:
        return self.rear == self.size - 1

    def is_empty(self) -> bool:
        return self.front > self.rear

    def enqueue(self, v: int) -> bool:
        if self.is_full():
            return False
        self.rear += 1
        self.items[self.rear] = v
        return True

    def dequeue(self) -> Optional[int]:
        if self.is_empty():
            return None
        v = self.items[self.front]
        self.items[self.front] = None
        self.front += 1
        return v

    def peek(self) -> Optional[int]:
        return self.items[self.front] if not self.is_empty() else None

    def snapshot(self) -> list[Optional[int]]:
        return self.items[:]

    def __len__(self) -> int:
        return 0 if self.is_empty() else self.rear - self.front + 1


class CircularQueue:
    name = "Circular (Array)"
    grows = False

    def __init__(self, size: int = 8) -> None:
        self.size = size
        self.items: list[Optional[int]] = [None] * size
        self.front = 0
        self.rear = -1
        self.count = 0

    @property
    def capacity(self) -> int:
        return self.size

    def is_full(self) -> bool:
        return self.count == self.size

    def is_empty(self) -> bool:
        return self.count == 0

    def enqueue(self, v: int) -> bool:
        if self.is_full():
            return False
        self.rear = (self.rear + 1) % self.size
        self.items[self.rear] = v
        self.count += 1
        return True

    def dequeue(self) -> Optional[int]:
        if self.is_empty():
            return None
        v = self.items[self.front]
        self.items[self.front] = None
        self.front = (self.front + 1) % self.size
        self.count -= 1
        return v

    def peek(self) -> Optional[int]:
        return self.items[self.front] if not self.is_empty() else None

    def snapshot(self) -> list[Optional[int]]:
        return self.items[:]

    def __len__(self) -> int:
        return self.count


class PriorityQueue:
    name = "Priority (Sorted)"
    capacity: Optional[int] = None
    grows = True

    def __init__(self) -> None:
        self.items: list[int] = []

    def enqueue(self, v: int) -> bool:
        self.items.append(v)
        self.items.sort(reverse=True)
        return True

    def dequeue(self) -> Optional[int]:
        return self.items.pop(0) if self.items else None

    def peek(self) -> Optional[int]:
        return self.items[0] if self.items else None

    def snapshot(self) -> list[Optional[int]]:
        return list(self.items)

    def __len__(self) -> int:
        return len(self.items)


QUEUE_TYPES: dict[str, Callable[..., Queue]] = {
    "Dynamic (Linked List)": DynamicQueue,
    "Linear (Array)": LinearQueue,
    "Circular (Array)": CircularQueue,
    "Priority (Sorted)": PriorityQueue,
}


# ---------- UI ----------
class QueueLab:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Queue Lab - Compare 4 Queues")
        root.geometry("760x560")
        self.queue: Optional[Queue] = None
        self.log: list[str] = []

        top = ttk.Frame(root, padding=12)
        top.pack(fill="x")
        ttk.Label(top, text="Queue type:").pack(side="left")
        self.type_var = tk.StringVar(value="Dynamic (Linked List)")
        ttk.Combobox(top, textvariable=self.type_var, values=list(QUEUE_TYPES), state="readonly", width=24).pack(side="left", padx=5)
        ttk.Label(top, text="Size (for Linear/Circular):").pack(side="left", padx=(10, 0))
        self.size_var = tk.StringVar(value="8")
        ttk.Spinbox(top, from_=3, to=20, textvariable=self.size_var, width=5).pack(side="left", padx=5)
        ttk.Button(top, text="Create / Reset", command=self.create).pack(side="left", padx=5)

        ctrl = ttk.Frame(root, padding=12)
        ctrl.pack(fill="x")
        self.entry = ttk.Entry(ctrl, width=14)
        self.entry.pack(side="left")
        self.entry.bind("<Return>", lambda _event: self.do_enqueue())
        ttk.Button(ctrl, text="Enqueue", command=self.do_enqueue).pack(side="left", padx=4)
        ttk.Button(ctrl, text="Dequeue", command=self.do_dequeue).pack(side="left", padx=4)
        ttk.Button(ctrl, text="Peek", command=self.do_peek).pack(side="left", padx=4)
        ttk.Button(ctrl, text="Demo: Fill 1-5", command=self.demo).pack(side="left", padx=4)
        ttk.Button(ctrl, text="Clear Log", command=self.clear_log).pack(side="left", padx=4)

        self.info = ttk.Label(root, text="", font=("Helvetica", 11, "bold"), padding=12)
        self.info.pack(fill="x")
        self.canvas = tk.Canvas(root, height=110, bg="white")
        self.canvas.pack(fill="x", padx=12)
        ttk.Label(root, text="Log (what happened + why it matters):", padding=12).pack(anchor="w")
        self.log_box = tk.Text(root, height=14)
        self.log_box.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.create()
        ttk.Label(root, text="Try this: In Linear queue, enqueue 8 items, dequeue 3, then try to enqueue again — it says FULL even though 3 slots are free. Switch to Circular and the same steps work. That's the whole lesson.", wraplength=730, padding=12).pack(fill="x")

    def create(self) -> None:
        cls = QUEUE_TYPES[self.type_var.get()]
        try:
            size = int(self.size_var.get())
        except ValueError:
            size = 8
        self.queue = cls(size) if cls in (LinearQueue, CircularQueue) else cls()
        q = self.queue
        self.log_msg(f"Created {q.name} (capacity: {q.capacity or 'unlimited'})")
        self.refresh()

    def log_msg(self, msg: str) -> None:
        self.log.append(msg)
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")

    def clear_log(self) -> None:
        self.log_box.delete("1.0", "end")

    def refresh(self) -> None:
        q = self.queue
        if q is None:
            return
        snap = q.snapshot()
        cap = q.capacity or max(len(snap), 1)
        rear = snap[-1] if snap and any(x is not None for x in snap) else '-'
        self.info.config(text=f"{q.name}  •  Size: {len(q)} / {q.capacity or '∞'}  •  Front (peek): {q.peek()}  •  Rear: {rear}")
        self.canvas.delete("all")

        n = max(len(snap), cap if q.capacity else len(snap))
        if n == 0:
            n = 1
        w = 700 / n
        for i, val in enumerate(snap if snap else [None]):
            x0 = 10 + i * w
            x1 = x0 + w - 6
            y0 = 20
            y1 = 90
            color = "#E8F5E9" if val is not None else "#EEEEEE"
            if i == 0 and val is not None:
                color = "#BBDEFB"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#999")
            self.canvas.create_text((x0 + x1) / 2, 45, text=str(val) if val is not None else "empty", font=("Helvetica", 12, "bold"))
            self.canvas.create_text((x0 + x1) / 2, 70, text=f"[{i}]", font=("Helvetica", 9))

        if isinstance(q, LinearQueue):
            self.canvas.create_text(350, 8, text=f"front index={q.front}  rear index={q.rear}  ← notice front moves forward and space is wasted", font=("Helvetica", 9))
        if isinstance(q, CircularQueue):
            self.canvas.create_text(350, 8, text=f"front={q.front}  rear={q.rear}  count={q.count}  ← rear wraps around", font=("Helvetica", 9))

    def do_enqueue(self) -> None:
        raw = self.entry.get().strip()
        if not raw:
            messagebox.showwarning("Empty", "Enter a number to enqueue")
            return
        try:
            v = int(raw)
        except ValueError:
            messagebox.showerror("Invalid", "Enter an integer")
            return
        q = self.queue
        if q is None:
            return
        ok = q.enqueue(v)
        if ok:
            self.log_msg(f"Enqueue {v} → OK. {self.explain_enqueue()}")
        else:
            self.log_msg(f"Enqueue {v} → FAILED: Queue is FULL. {self.explain_full()}")
        self.entry.delete(0, "end")
        self.refresh()

    def do_dequeue(self) -> None:
        q = self.queue
        if q is None:
            return
        v = q.dequeue()
        if v is None:
            self.log_msg("Dequeue → FAILED: Queue is EMPTY")
            messagebox.showinfo("Empty", "Queue is empty")
        else:
            self.log_msg(f"Dequeue → removed {v} (FIFO: first-in, first-out)")
        self.refresh()

    def do_peek(self) -> None:
        q = self.queue
        if q is None:
            return
        v = q.peek()
        self.log_msg(f"Peek → {v if v is not None else 'empty (nothing to peek)'}")
        self.refresh()

    def demo(self) -> None:
        self.create()
        q = self.queue
        if q is None:
            return
        for v in [10, 20, 30, 40, 50]:
            q.enqueue(v)
        self.log_msg("Demo: enqueued 10,20,30,40,50")
        self.refresh()

    def explain_enqueue(self) -> str:
        q = self.queue
        if isinstance(q, PriorityQueue):
            return "Priority queue re-sorts: biggest value jumps to front."
        if isinstance(q, LinearQueue):
            return f"Stored at index {q.rear}."
        if isinstance(q, CircularQueue):
            return f"Stored at index {q.rear} (wrapped if needed)."
        return "Appended to linked list."

    def explain_full(self) -> str:
        if isinstance(self.queue, LinearQueue):
            return "Linear queue wastes freed front space — it only checks rear. Use Circular to fix this."
        return "Circular queue is truly full — all slots used."


if __name__ == "__main__":
    root = tk.Tk()
    QueueLab(root)
    root.mainloop()
