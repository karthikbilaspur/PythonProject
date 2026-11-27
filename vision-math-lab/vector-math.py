import tkinter as tk, math
from tkinter import messagebox
class Vector:
 def __init__(self,x: float,y: float,z: float) -> None: self.x,self.y,self.z=float(x),float(y),float(z)
 def __str__(self): return f"({self.x}, {self.y}, {self.z})"
 def add(self, o: "Vector") -> "Vector": return Vector(self.x+o.x,self.y+o.y,self.z+o.z)
 def subtract(self, o: "Vector") -> "Vector": return Vector(self.x-o.x,self.y-o.y,self.z-o.z)
 def dot_product(self, o: "Vector") -> float: return self.x*o.x+self.y*o.y+self.z*o.z
 def cross_product(self, o: "Vector") -> "Vector": return Vector(self.y*o.z-self.z*o.y,self.z*o.x-self.x*o.z,self.x*o.y-self.y*o.x)
 def magnitude(self): return math.sqrt(self.x**2+self.y**2+self.z**2)
 def normalize(self):
  m=self.magnitude()
  if m==0: raise ValueError("Cannot normalize zero vector")
  return Vector(self.x/m,self.y/m,self.z/m)
class VectorTool:
 def __init__(self,parent: tk.Misc | None = None):
  self.window=tk.Toplevel(parent) if parent else tk.Tk(); self.window.title("3D Vector Math Lab"); self.window.geometry("480x460")
  tk.Label(self.window,text="3D Vector Math Lab",font=("Arial",14,"bold")).pack(pady=10)
  tk.Label(self.window,text="Vector 1 x,y,z:").pack(); self.v1=tk.Entry(self.window,width=30); self.v1.insert(0,"1, 2, 3"); self.v1.pack()
  tk.Label(self.window,text="Vector 2 x,y,z:").pack(pady=5); self.v2=tk.Entry(self.window,width=30); self.v2.insert(0,"4, 5, 6"); self.v2.pack()
  for txt,fn in [("Add","add"),("Subtract","sub"),("Dot Product","dot"),("Cross Product","cross"),("Magnitude + Normalize v1","mag")]:
   tk.Button(self.window,text=txt,width=30,command=lambda f=fn: self.calc(f)).pack(pady=3)
  self.out=tk.Label(self.window,text="",wraplength=420,font=("Arial",11),fg="green",justify="left"); self.out.pack(pady=12)
 def parse(self,s: str) -> Vector: x,y,z=[float(v.strip()) for v in s.split(",")]; return Vector(x,y,z)
 def calc(self,mode: str) -> None:
  try:
   a,b=self.parse(self.v1.get()),self.parse(self.v2.get())
   if mode=="add": r=f"v1 + v2 = {a.add(b)}"
   elif mode=="sub": r=f"v1 - v2 = {a.subtract(b)}"
   elif mode=="dot": r=f"v1 . v2 = {a.dot_product(b)}"
   elif mode=="cross": r=f"v1 x v2 = {a.cross_product(b)}"
   else: r=f"|v1| = {a.magnitude():.4f}\nv1 normalized = {a.normalize()}\n|v2| = {b.magnitude():.4f}"
   self.out.config(text=r)
  except Exception as e: messagebox.showerror("Error",str(e))
 def run(self): self.window.mainloop()
def open_window(parent: tk.Misc | None = None) -> VectorTool: return VectorTool(parent)
def main():
 v1,v2=Vector(1,2,3),Vector(4,5,6); print(f"v1+v2={v1.add(v2)}"); print(f"v1-v2={v1.subtract(v2)}"); print(f"dot={v1.dot_product(v2)}"); print(f"cross={v1.cross_product(v2)}"); print(f"|v1|={v1.magnitude()}"); print(f"norm={v1.normalize()}")
if __name__=="__main__":
 import sys
 if len(sys.argv)>1 and sys.argv[1]=="--cli": main()
 else: VectorTool().run()
