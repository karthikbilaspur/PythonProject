import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class CustomerSegmentation:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Segmentation")

        # Load data button
        self.load_button = tk.Button(root, text="Load Data", command=self.load_data)
        self.load_button.pack()

        # Select columns button
        self.select_columns_button = tk.Button(root, text="Select Columns", command=self.select_columns)
        self.select_columns_button.pack()

        # Segment customers button
        self.segment_button = tk.Button(root, text="Segment Customers", command=self.segment_customers)
        self.segment_button.pack()

        # Data and columns variables
        self.data = None
        self.columns = None

    def load_data(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.data = pd.read_csv(filename)
        messagebox.showinfo("Info", "Data loaded successfully")

    def select_columns(self):
        if self.data is not None:
            columns_window = tk.Toplevel(self.root)
            columns_window.title("Select Columns")

            # Listbox for column selection
            listbox = tk.Listbox(columns_window, selectmode=tk.MULTIPLE)
            for column in self.data.columns:
                listbox.insert(tk.END, column)
            listbox.pack()

            def get_selected_columns():
                selected_columns = [listbox.get(i) for i in listbox.curselection()]
                self.columns = selected_columns
                messagebox.showinfo("Info", "Columns selected successfully")
                columns_window.destroy()

            # Button to get selected columns
            button = tk.Button(columns_window, text="Get Selected Columns", command=get_selected_columns)
            button.pack()
        else:
            messagebox.showerror("Error", "Load data first")

    def segment_customers(self):
        if self.data is not None and self.columns is not None:
            # Select relevant columns
            data = self.data[self.columns]

            # Scale data
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(data)

            # Perform K-means clustering
            kmeans = KMeans(n_clusters=3)
            kmeans.fit(scaled_data)
            labels = kmeans.labels_

            # Add cluster labels to original data
            self.data['Cluster'] = labels

            # Save segmented data
            self.data.to_csv('segmented_customers.csv', index=False)
            messagebox.showinfo("Info", "Customers segmented successfully")
        else:
            messagebox.showerror("Error", "Load data and select columns first")

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerSegmentation(root)
    root.mainloop()