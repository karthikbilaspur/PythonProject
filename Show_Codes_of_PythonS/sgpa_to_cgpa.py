import tkinter as tk
from tkinter import messagebox, filedialog
import json

class SGPAtoCGPA:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SGPA to CGPA Converter")

        # Create input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=10)

        tk.Label(input_frame, text="Number of Semesters:").grid(row=0, column=0)
        self.semesters = tk.Entry(input_frame)
        self.semesters.grid(row=0, column=1)

        tk.Button(input_frame, text="Calculate CGPA", command=self.calculate_cgpa).grid(row=1, columnspan=2, pady=10)

        # Create result frame
        result_frame = tk.Frame(self.root)
        result_frame.pack(padx=10, pady=10)

        self.result = tk.Label(result_frame, text="")
        self.result.pack()

        # Create menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Save Result", command=self.save_result)
        filemenu.add_command(label="Load Result", command=self.load_result)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)

    def calculate_cgpa(self):
        try:
            semesters = int(self.semesters.get())
            total_credits = 0
            total_sgpa = 0
            self.semester_data = {}

            for i in range(semesters):
                sgpa = float(input(f"Enter SGPA for semester {i+1}: "))
                credits = int(input(f"Enter credits for semester {i+1}: "))
                total_sgpa += sgpa * credits
                total_credits += credits
                self.semester_data[f"Semester {i+1}"] = {"SGPA": sgpa, "Credits": credits}

            cgpa = total_sgpa / total_credits
            self.result.config(text=f"Your CGPA is: {cgpa:.2f}")
            self.cgpa = cgpa
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_result(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON File", "*.json")])
            if file_path:
                data = {
                    "CGPA": self.cgpa,
                    "Semester Data": self.semester_data
                }
                with open(file_path, "w") as file:
                    json.dump(data, file, indent=4)
                messagebox.showinfo("Success", "Result saved successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_result(self):
        try:
            file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON File", "*.json")])
            if file_path:
                with open(file_path, "r") as file:
                    data =