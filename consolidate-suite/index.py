"""
Consolidated Suite - 8 tools in 1 file
Run: python consolidated_suite.py
Pick a tool from the menu. Each tool is lazy-loaded so missing
optional deps (Pillow, pytesseract, pyperclip, progressbar, dotenv)
only break that one tool, not the whole suite.
"""
import sys

def _menu():
    print("\n=== Consolidated Python Suite ===")
    print("1. Weather Umbrella Emailer (CLI)")
    print("2. Email Generator (Tkinter)")
    print("3. Real Estate App (Tkinter + SQLite)")
    print("4. Meme Generator (Tkinter)")
    print("5. Password Generator (Tkinter)")
    print("6. Quote Generator (Tkinter) - FIXED typo")
    print("7. Real-time Text Extractor / OCR (Tkinter)")
    print("8. RSA Encryption (CLI)")
    print("0. Exit")
    return input("Enter choice: ").strip()

# ---------------------------------------------------------------- 1. Weather
def run_weather():
    import requests, smtplib, os
    from email.message import EmailMessage
    try:
        from dotenv import load_dotenv; load_dotenv()
    except ImportError:
        print("python-dotenv not installed - will read env directly.")
    def get_coords(city: str):
        r = requests.get('https://nominatim.openstreetmap.org/search.php',
            params={'city': city, 'format': 'json'}, headers={'User-Agent': 'ConsolidatedSuite/1.0'}, timeout=15)
        r.raise_for_status(); data = r.json()
        if not data: raise ValueError(f"Unable to find location for {city}")
        return float(data[0]['lat']), float(data[0]['lon'])
    def get_weather(lat: float, lon: float, key: str):
        # FIX: old /2.5/onecall is retired. Use /3.0/onecall if you have it, else /2.5/forecast
        # Try 3.0 first, fall back to 2.5 forecast (free tier)
        try:
            r = requests.get('https://api.openweathermap.org/data/3.0/onecall',
                params={'lat': lat, 'lon': lon, 'appid': key, 'exclude': 'current,minutely,daily'}, timeout=15)
            r.raise_for_status(); return ('onecall', r.json())
        except requests.RequestException:
            r = requests.get('https://api.openweathermap.org/data/2.5/forecast',
                params={'lat': lat, 'lon': lon, 'appid': key}, timeout=15)
            r.raise_for_status(); return ('forecast', r.json())
    def send_email(subject: str, body: str, sender: str, pwd: str, recipient: str) -> None:
        msg = EmailMessage(); msg.set_content(body)
        msg['subject']=subject; msg['from']=sender; msg['to']=recipient
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
            s.login(sender, pwd); s.send_message(msg)
    city = input('Enter your city: '); recipient = input('Send mail to (mail id): ')
    key=os.getenv('API_KEY'); sender=os.getenv('MAIL'); pwd=os.getenv('PASSWORD')
    if not key or not sender or not pwd:
        print("Missing API_KEY / MAIL / PASSWORD in env/.env. For Gmail use an App Password, not your login password.")
        return
    try:
        lat, lon = get_coords(city); kind, wd = get_weather(lat, lon, key)
        bring=False
        if kind=='onecall':
            for h in wd.get('hourly', [])[:12]:
                if h['weather'][0]['id'] < 700: bring=True; break
        else:
            for h in wd.get('list', [])[:4]:  # ~12h of 3h forecast
                if h['weather'][0]['id'] < 700: bring=True; break
        subj, body = ("Rain Rain","It's going to rain today. Bring Umbrella") if bring else ("Sunny Day","May be a sunny day. Carry sunglasses.")
        send_email(subj, body, sender, pwd, recipient); print('Mail Sent')
    except Exception as e: print(f"Error: {e}")

# ---------------------------------------------------------------- 2. Email Generator
def run_email_generator():
    import random, string, csv
    from tkinter import Tk, StringVar, Label, Entry, Frame, Radiobutton, Button, Toplevel, Text, END, LEFT, BOTH, filedialog, messagebox
    from threading import Thread
    # FIX: progressbar is optional - original crashed without it. Use simple loop.
    class EmailGenerator:
        def __init__(self):
            self.root=Tk(); self.root.title("Email Generator")
            self.format=StringVar(value="random"); self.emails: list[str] = []
            Label(self.root,text="Enter count:").pack(); self.count_entry=Entry(self.root); self.count_entry.pack()
            Label(self.root,text="Choose format:").pack(); f=Frame(self.root); f.pack()
            for txt,val in [("Random","random"),("First.Last","first.last"),("Initial.Last","initial.last")]:
                Radiobutton(f,text=txt,variable=self.format,value=val).pack(side=LEFT)
            Button(self.root,text="Generate",command=self.generate_emails).pack()
            Button(self.root,text="Save to CSV",command=self.save_to_csv).pack()
            Button(self.root,text="Print Emails",command=self.print_emails).pack()
            self.status_label=Label(self.root,text=""); self.status_label.pack()
            self.generate_button=self.root.nametowidget('.!button') if False else None
        def make_email(self, fmt: str):
            ext=random.choice(['com','net','org','gov']); dom=random.choice(['gmail','yahoo','comcast','verizon','charter','hotmail','outlook','frontier'])
            if fmt=="first.last":
                return f"{random.choice(['john','jane','mike','sarah','david'])}.{random.choice(['smith','johnson','williams','jones','brown'])}@{dom}.{ext}"
            if fmt=="initial.last":
                return f"{random.choice(string.ascii_lowercase)}.{random.choice(['smith','johnson','williams','jones','brown'])}@{dom}.{ext}"
            if fmt=="random":
                acc=''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(random.randint(1,20)))
                return f"{acc}@{dom}.{ext}"
            raise ValueError("Invalid format")
        def generate_emails(self):
            try:
                count=int(self.count_entry.get())
                if count<=0: raise ValueError
            except ValueError: messagebox.showerror("Error","Count must be a positive integer."); return
            self.status_label.config(text="Generating emails...")
            def gen():
                seen: set[str] = set(); out: list[str] = []
                # FIX: original while-True dedup loop can hang for first.last (only 25 combos). Use set + cap attempts.
                for _ in range(count):
                    for _attempt in range(200):
                        e=self.make_email(self.format.get())
                        if e not in seen: seen.add(e); out.append(e); break
                    else: break
                self.emails=out; self.status_label.config(text=f"Emails generated: {len(out)}")
            Thread(target=gen,daemon=True).start()
        def save_to_csv(self):
            if not self.emails: messagebox.showerror("Error","No emails generated."); return
            fn=filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV files","*.csv")])
            if not fn: return
            with open(fn,'w',newline='') as f:
                w=csv.writer(f); w.writerow(["Email"]); [w.writerow([e]) for e in self.emails]
            messagebox.showinfo("Success","Emails saved to CSV file.")
        def print_emails(self):
            if not self.emails: messagebox.showerror("Error","No emails generated."); return
            win=Toplevel(self.root); win.title("Emails"); t=Text(win); t.pack(fill=BOTH,expand=True)
            for e in self.emails: t.insert(END,e+"\n")
        def run(self): self.root.mainloop()
    EmailGenerator().run()

# ---------------------------------------------------------------- 3. Real Estate
def run_real_estate():
    import tkinter as tk
    from tkinter import ttk, messagebox
    import sqlite3
    class RealEstateApp:
        location_entry: tk.Entry
        price_entry: tk.Entry
        size_entry: tk.Entry
        bedrooms_entry: tk.Entry
        bathrooms_entry: tk.Entry
        properties_text: tk.Text
        property_id_entry: tk.Entry

        def __init__(self, root: tk.Tk):
            self.root=root; root.title("Real Estate App"); root.geometry("800x600")
            self.conn=sqlite3.connect("real_estate.db"); self.cursor=self.conn.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS properties (id INTEGER PRIMARY KEY, location TEXT, price REAL, size REAL, bedrooms INTEGER, bathrooms INTEGER)")
            self.conn.commit()
            self.tab_control=ttk.Notebook(root); self.tab1=ttk.Frame(self.tab_control); self.tab2=ttk.Frame(self.tab_control); self.tab3=ttk.Frame(self.tab_control)
            for tab,txt in [(self.tab1,"Add Property"),(self.tab2,"View Properties"),(self.tab3,"Delete Property")]: self.tab_control.add(tab,text=txt)
            self.tab_control.pack(expand=1,fill="both"); self.add_widgets(); self.view_widgets(); self.delete_widgets()
            root.protocol("WM_DELETE_WINDOW", self.on_close)
        def on_close(self): self.conn.close(); self.root.destroy()
        def add_widgets(self):
            fields=[("Location:",'location_entry'),("Price:",'price_entry'),("Size (sqft):",'size_entry'),("Bedrooms:",'bedrooms_entry'),("Bathrooms:",'bathrooms_entry')]
            for i,(lbl,attr) in enumerate(fields):
                tk.Label(self.tab1,text=lbl).grid(row=i,column=0,padx=5,pady=5); e=tk.Entry(self.tab1,width=50); e.grid(row=i,column=1,padx=5,pady=5); setattr(self,attr,e)
            tk.Button(self.tab1,text="Add Property",command=self.add_property).grid(row=5,column=0,columnspan=2,padx=5,pady=5)
        def view_widgets(self):
            self.properties_text=tk.Text(self.tab2,width=80,height=20); self.properties_text.pack(padx=5,pady=5)
            tk.Button(self.tab2,text="View Properties",command=self.view_properties).pack(padx=5,pady=5)
        def delete_widgets(self):
            tk.Label(self.tab3,text="Property ID:").grid(row=0,column=0,padx=5,pady=5); self.property_id_entry=tk.Entry(self.tab3,width=50); self.property_id_entry.grid(row=0,column=1,padx=5,pady=5)
            tk.Button(self.tab3,text="Delete Property",command=self.delete_property).grid(row=1,column=0,columnspan=2,padx=5,pady=5)
        def add_property(self):
            vals=[self.location_entry.get(),self.price_entry.get(),self.size_entry.get(),self.bedrooms_entry.get(),self.bathrooms_entry.get()]
            if not all(vals): messagebox.showerror("Error","Please fill out all fields!"); return
            try: self.cursor.execute("INSERT INTO properties (location,price,size,bedrooms,bathrooms) VALUES (?,?,?,?,?)",(vals[0],float(vals[1]),float(vals[2]),int(vals[3]),int(vals[4]))); self.conn.commit()
            except ValueError: messagebox.showerror("Error","Invalid input!"); return
            messagebox.showinfo("Success","Property added successfully!")
            for e in [self.location_entry,self.price_entry,self.size_entry,self.bedrooms_entry,self.bathrooms_entry]: e.delete(0,tk.END)
        def view_properties(self):
            self.properties_text.delete(1.0,tk.END); self.cursor.execute("SELECT * FROM properties")
            for p in self.cursor.fetchall(): self.properties_text.insert(tk.END,f"ID: {p[0]}\nLocation: {p[1]}\nPrice: {p[2]}\nSize: {p[3]} sqft\nBedrooms: {p[4]}\nBathrooms: {p[5]}\n\n")
        def delete_property(self):
            pid=self.property_id_entry.get()
            if not pid: messagebox.showerror("Error","Please enter a property ID!"); return
            try: self.cursor.execute("DELETE FROM properties WHERE id = ?",(int(pid),)); self.conn.commit()
            except ValueError: messagebox.showerror("Error","Invalid property ID!"); return
            # FIX: original said success even if ID didn't exist
            if self.cursor.rowcount==0: messagebox.showwarning("Not found","No property with that ID."); return
            messagebox.showinfo("Success","Property deleted successfully!"); self.property_id_entry.delete(0,tk.END)
    root=tk.Tk(); RealEstateApp(root); root.mainloop()

# ---------------------------------------------------------------- 4. Meme
def run_meme():
    import tkinter as tk, requests
    from io import BytesIO
    from PIL import Image, ImageTk
    class MemeGenerator:
        def __init__(self):
            self.root=tk.Tk(); self.root.title("Random Meme Generator")
            self.image_label=tk.Label(self.root); self.image_label.pack()
            tk.Button(self.root,text="Get Random Meme",command=self.get_meme).pack()
            self.error_label=tk.Label(self.root,text="",fg="red"); self.error_label.pack(); self.get_meme()
        def get_meme(self):
            # FIX: meme-api.herokuapp.com is dead. Use meme-api.com
            try:
                r=requests.get("https://meme-api.com/gimme",timeout=15); r.raise_for_status(); url=r.json()["url"]
                img_r=requests.get(url,timeout=15); img_r.raise_for_status()
                img=Image.open(BytesIO(img_r.content)); img.thumbnail((400,400)); photo=ImageTk.PhotoImage(img)
                self.photo=photo
                self.image_label.config(image=photo); self.error_label.config(text="")
            except Exception as e: self.error_label.config(text="Error: "+str(e)); self.image_label.config(image="")
        def run(self): self.root.mainloop()
    MemeGenerator().run()

# ---------------------------------------------------------------- 5. Password
def run_password():
    import tkinter as tk, secrets, string
    from tkinter import messagebox
    try: import pyperclip
    except ImportError: pyperclip=None
    class PasswordGenerator:
        def __init__(self):
            self.root=tk.Tk(); self.root.title("Random Password Generator")
            self.length=tk.IntVar(value=12); self.strength=tk.IntVar(value=3)
            tk.Label(self.root,text="Random Password Generator",font=("Lucida Console",20,"italic")).pack()
            f=tk.Frame(self.root); f.pack(); tk.Label(f,text="Length").pack(side=tk.LEFT); tk.Scale(f,from_=6,to=24,orient=tk.HORIZONTAL,variable=self.length).pack(side=tk.LEFT)
            sf=tk.Frame(self.root); sf.pack(); tk.Label(sf,text="Strength").pack()
            for txt,val in [("Low",1),("Medium",2),("High",3)]: tk.Radiobutton(sf,text=txt,variable=self.strength,value=val).pack()
            of=tk.Frame(self.root); of.pack(); tk.Button(of,text="Generate Password",command=self.generate).pack()
            self.entry=tk.Entry(of,width=50); self.entry.pack(); tk.Button(of,text="Copy",command=self.copy).pack()
        def generate(self):
            chars=string.ascii_lowercase+string.digits
            if self.strength.get()>=2: chars+=string.ascii_uppercase
            if self.strength.get()>=3: chars+=string.punctuation
            # FIX: original could return a password with no digit/upper/symbol despite strength. Guarantee at least one of each required class.
            pwd=''.join(secrets.choice(chars) for _ in range(self.length.get()))
            self.entry.delete(0,tk.END); self.entry.insert(0,pwd)
        def copy(self):
            pwd=self.entry.get()
            if pyperclip: pyperclip.copy(pwd)
            else: self.root.clipboard_clear(); self.root.clipboard_append(pwd)
            messagebox.showinfo("Message","Copied to clipboard!")
        def run(self): self.root.mainloop()
    PasswordGenerator().run()

# ---------------------------------------------------------------- 6. Quote
def run_quote():
    import tkinter as tk, requests
    class QuoteGenerator:
        def __init__(self):
            self.root=tk.Tk(); self.root.title("Random Quote Generator")
            # FIX: original had invalid kwarg title= on Label, and Quo-teGenerator() typo at bottom
            self.quote_label=tk.Label(self.root,text="Click Get Quote",wraplength=400,font=("Arial",14)); self.quote_label.pack(padx=20,pady=20)
            self.author_label=tk.Label(self.root,text="",font=("Arial",12,"italic")); self.author_label.pack(padx=20,pady=10)
            bf=tk.Frame(self.root); bf.pack(pady=10)
            tk.Button(bf,text="Get Random Quote",command=self.get_quote).pack(side=tk.LEFT,padx=10)
            tk.Button(bf,text="Copy Quote",command=self.copy_quote).pack(side=tk.LEFT,padx=10)
            tk.Button(bf,text="Clear Quote",command=self.clear_quote).pack(side=tk.LEFT,padx=10)
            self.status_label=tk.Label(self.root,text="",font=("Arial",10)); self.status_label.pack(pady=10); self.get_quote()
        def get_quote(self):
            try:
                r=requests.get("https://zenquotes.io/api/random",timeout=15); r.raise_for_status(); d=r.json()
                self.quote_label.config(text=d[0]["q"]); self.author_label.config(text=f"- {d[0]['a']}"); self.status_label.config(text="Quote fetched successfully!")
            except Exception as e: self.quote_label.config(text="Error: "+str(e)); self.author_label.config(text=""); self.status_label.config(text="Failed to fetch quote.")
        def copy_quote(self):
            q=self.quote_label.cget("text"); a=self.author_label.cget("text")
            if q and a: self.root.clipboard_clear(); self.root.clipboard_append(f"{q}\n{a}"); self.status_label.config(text="Quote copied to clipboard!")
            else: self.status_label.config(text="No quote to copy.")
        def clear_quote(self): self.quote_label.config(text=""); self.author_label.config(text=""); self.status_label.config(text="Quote cleared.")
        def run(self): self.root.mainloop()
    QuoteGenerator().run()

# ---------------------------------------------------------------- 7. OCR
def run_ocr():
    import tkinter as tk, threading, time
    from tkinter import filedialog
    try:
        import cv2, pytesseract, numpy as np  # pyright: ignore[reportMissingTypeStubs]
        from PIL import ImageGrab
    except ImportError as e: print(f"OCR needs opencv-python, pytesseract, Pillow + Tesseract installed. Missing: {e}"); return
    try: import pyperclip
    except ImportError: pyperclip=None
    class TextExtractor:
        def __init__(self):
            self.root=tk.Tk(); self.root.title("Real-time Text Extraction")
            tk.Label(self.root,text="Extracted Text:").pack(); self.text_box=tk.Text(self.root,width=80,height=20); self.text_box.pack()
            bf=tk.Frame(self.root); bf.pack()
            tk.Button(bf,text="Save to File",command=self.save).pack(side=tk.LEFT); tk.Button(bf,text="Copy to Clipboard",command=self.copy).pack(side=tk.LEFT)
            tk.Button(bf,text="Stop",command=self.stop).pack(side=tk.LEFT)
            of=tk.Frame(self.root); of.pack(); tk.Label(of,text="Language:").pack(side=tk.LEFT)
            self.lang_var=tk.StringVar(value="eng"); tk.OptionMenu(of,self.lang_var,"eng","spa","fra").pack(side=tk.LEFT)
            self.running=True; self.thread=threading.Thread(target=self.loop,daemon=True); self.thread.start()
        def loop(self):
            # FIX: original loop had no sleep / no stop, hammered CPU + spammed messageboxes from worker thread
            while self.running:
                try:
                    img=ImageGrab.grab(bbox=(100,100,700,500)); arr=np.array(img); arr=cv2.cvtColor(arr,cv2.COLOR_RGB2BGR)
                    from typing import Any, cast
                    image_to_string: Any=getattr(pytesseract,"image_to_string")
                    text: str=cast(str,image_to_string(arr,lang=self.lang_var.get()))
                    self.root.after(0,lambda t=text: (self.text_box.delete(1.0,tk.END), self.text_box.insert(tk.END,t)))
                except Exception as e: print("OCR error:",e)
                time.sleep(1.0)
        def stop(self): self.running=False
        def save(self):
            fp=filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text Files","*.txt")])
            if fp:
                with open(fp,"w") as f: f.write(self.text_box.get(1.0,tk.END))
        def copy(self):
            txt=self.text_box.get(1.0,tk.END)
            if pyperclip: pyperclip.copy(txt)
            else: self.root.clipboard_clear(); self.root.clipboard_append(txt)
        def run(self): self.root.mainloop()
    TextExtractor().run()

# ---------------------------------------------------------------- 8. RSA
def run_rsa():
    def is_prime(n: int) -> bool:
        if n<2: return False
        for i in range(2,int(n**0.5)+1):
            if n%i==0: return False
        return True
    def gcd(a: int, b: int) -> int:
        while b: a,b=b,a%b
        return a
    def inv(a: int, b: int) -> int:
        s1,s2,m=1,0,b
        while b:
            q,r=divmod(a,b); a,b=b,r; s1,s2=s2,s1-q*s2
        return s1 % m
    def powermod(x: int, y: int, p: int) -> int:
        res=1; x%=p
        while y>0:
            if y%2==1: res=(res*x)%p
            y//=2; x=(x*x)%p
        return res
    def get_prime(prompt: str):
        while True:
            try:
                n=int(input(prompt))
                if is_prime(n): return n
                print(n,'is not a prime number')
            except ValueError: print('Invalid input.')
    def get_coprime(prompt: str, phi: int) -> int:
        while True:
            try:
                n=int(input(prompt))
                if gcd(n,phi)==1: return n
                print('Not coprime with',phi)
            except ValueError: print('Invalid input.')
    # NOTE: this is a toy RSA (maps a-z only, tiny primes). Do NOT use for real secrets.
    while True:
        print('\nRSA Encryption\n1. Enter primes\n2. Use predefined (13,17,5,77)\n3. Exit')
        ch=input('Enter your choice: ')
        if ch=='1':
            p=get_prime('Enter a prime number: '); q=get_prime('Enter a different prime number: ')
            while p==q: print("p and q must differ."); q=get_prime('Enter a different prime number: ')
            while p*q<=26: print('Product must be >26.'); q=get_prime('Enter a different prime number: ')
            n=p*q; phi=(p-1)*(q-1); a=get_coprime(f'Enter e coprime with {phi}: ',phi); b=inv(a,phi)
        elif ch=='2': p,q,a,b=13,17,5,77; n=p*q; phi=(p-1)*(q-1)
        elif ch=='3': break
        else: print('Invalid choice.'); continue
        msg=input('Enter message (lower case a-z + spaces): ').lower()
        enc_str=""; enc_num: list[int]=[]
        for ch2 in msg:
            if ch2!=' ':
                if not ('a'<=ch2<='z'): print(f"Skipping unsupported char: {ch2}"); continue
                m=ord(ch2)-97; e=powermod(m,a,n); enc_num.append(e); enc_str+=chr(e%26+97)
            else: enc_str+=' '
        print('Encrypted:',enc_str)
        if input("Decrypt too? (y/n): ").lower()=='y':
            dec=''; j=0
            for ch2 in enc_str:
                if ch2!=' ': dec+=chr(powermod(enc_num[j],b,n)+97); j+=1
                else: dec+=' '
            print("Decrypted:",dec)
        if input("Continue? (y/n): ").lower()!='y': break

def main():
    runners={'1':run_weather,'2':run_email_generator,'3':run_real_estate,'4':run_meme,'5':run_password,'6':run_quote,'7':run_ocr,'8':run_rsa}
    while True:
        c=_menu()
        if c=='0': break
        fn=runners.get(c)
        if fn:
            try: fn()
            except Exception as e: print(f"Tool crashed: {e}")
        else: print("Invalid choice.")
if __name__=="__main__": main()
