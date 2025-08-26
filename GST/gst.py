from tkinter import *

def gst_calculator():
    org_cost = int(original_priceField.get())
    gst_rate = float(gst_rateField.get())

    gst_amount = (org_cost * gst_rate) / 100
    net_price = org_cost + gst_amount
    cgst_rate = gst_rate / 2
    sgst_rate = gst_rate / 2
    cgst_amount = gst_amount / 2
    sgst_amount = gst_amount / 2

    cgst_percentField.delete(0, END)
    cgst_percentField.insert(10, str(cgst_rate) + " % ")
    sgst_percentField.delete(0, END)
    sgst_percentField.insert(10, str(sgst_rate) + " % ")
    total_gstField.delete(0, END)
    total_gstField.insert(10, f"₹ {gst_amount:.2f}")
    net_priceField.delete(0, END)
    net_priceField.insert(10, f"₹ {net_price:.2f}")
    cgst_amountField.delete(0, END)
    cgst_amountField.insert(10, f"₹ {cgst_amount:.2f}")
    sgst_amountField.delete(0, END)
    sgst_amountField.insert(10, f"₹ {sgst_amount:.2f}")


def gst_calculator_reverse():
    net_price = int(net_priceField_reverse.get())
    org_cost = int(original_priceField_reverse.get())
    total_gst_rate = ((net_price - org_cost) * 100) / org_cost
    cgst_rate = total_gst_rate / 2
    sgst_rate = total_gst_rate / 2
    total_gst = net_price - org_cost

    cgst_percentField_reverse.delete(0, END)
    cgst_percentField_reverse.insert(10, str(cgst_rate) + " % ")
    sgst_percentField_reverse.delete(0, END)
    sgst_percentField_reverse.insert(10, str(sgst_rate) + " % ")
    total_gstField_reverse.delete(0, END)
    total_gstField_reverse.insert(10, f"₹ {total_gst:.2f}")


def clearAll():
    original_priceField.delete(0, END)
    gst_rateField.delete(0, END)
    cgst_percentField.delete(0, END)
    sgst_percentField.delete(0, END)
    total_gstField.delete(0, END)
    net_priceField.delete(0, END)
    cgst_amountField.delete(0, END)
    sgst_amountField.delete(0, END)


def clearAll_reverse():
    original_priceField_reverse.delete(0, END)
    net_priceField_reverse.delete(0, END)
    cgst_percentField_reverse.delete(0, END)
    sgst_percentField_reverse.delete(0, END)
    total_gstField_reverse.delete(0, END)


gui = Tk()
gui.configure(background="light blue")
gui.title("GST Calculator")
gui.geometry("800x600")

notebook = Notebook(gui)
notebook.pack(pady=10, expand=True)

frame1 = Frame(notebook)
frame2 = Frame(notebook)

notebook.add(frame1, text='GST Calculator')
notebook.add(frame2, text='Reverse GST Calculator')

label_font = ('Arial', 14)
entry_font = ('Arial', 12)
button_font = ('Arial', 12, 'bold')

original_price = Label(frame1, text="Original Price:", font=label_font)
original_price.grid(row=1, column=0, padx=10, pady=10, sticky='w')
original_priceField = Entry(frame1, font=entry_font)
original_priceField.grid(row=1, column=1, padx=10, pady=10, sticky='w')

gst_rate = Label(frame1, text="GST Rate (%):", font=label_font)
gst_rate.grid(row=2, column=0, padx=10, pady=10, sticky='w')
gst_rateField = Entry(frame1, font=entry_font)
gst_rateField.grid(row=2, column=1, padx=10, pady=10, sticky='w')

find = Button(frame1, text="Calculate GST", fg="black",
              bg="light yellow", font=button_font, command=gst_calculator)
find.grid(row=3, column=1, padx=10, pady=10, sticky='w')

cgst_percent = Label(frame1, text="CGST Rate:", font=label_font)
cgst_percent.grid(row=4, column=0, padx=10, pady=10, sticky='w')
cgst_percentField = Entry(frame1, font=entry_font)
cgst_percentField.grid(row=4, column=1, padx=10, pady=10, sticky='w')

sgst_percent = Label(frame1, text="SGST Rate:", font=label_font)
sgst_percent.grid(row=5, column=0, padx=10, pady=10, sticky='w')
sgst_percentField = Entry(frame1, font=entry_font)
sgst_percentField.grid(row=5, column=1, padx=10, pady=10, sticky='w')

total_gst_label = Label(frame1, text="Total GST Amount:", font=label_font)
total_gst_label.grid(row=6, column=0, padx=10, pady=10, sticky='w')
total_gstField = Entry(frame1, font=entry_font)
total_gstField.grid(row=6, column=1, padx=10, pady=10, sticky='w')

net_price_label = Label(frame1, text="Net Price:", font=label_font)
net_price_label.grid(row=7, column=0, padx=10, pady=10, sticky='w')
net_priceField = Entry(frame1, font=entry_font)
net_priceField.grid(row=7, column=1, padx=10, pady=10, sticky='w')

cgst_amount_label = Label(frame1, text="CGST Amount:", font=label_font)
cgst_amount_label.grid(row=8, column=0, padx=10, pady=10, sticky='w')
cgst_amountField = Entry(frame1, font=entry_font)
cgst_amountField.grid(row=8, column=1, padx=10, pady=10, sticky='w')

sgst_amount_label = Label(frame1, text="SGST Amount:", font=label_font)
sgst_amount_label.grid(row=9, column=0, padx=10, pady=10, sticky='w')
sgst_amountField = Entry(frame1, font=entry_font)
sgst_amountField.grid(row=9, column=1, padx=10, pady=10, sticky='w')

clear = Button(frame1, text="Clear All", fg="black",
               bg="light yellow", font=button_font, command=clearAll)
clear.grid(row=10, column=1, padx=10, pady=10, sticky='w')

original_price_reverse = Label(frame2, text="Original Price:", font=label_font)
original_price_reverse.grid(row=1, column=0, padx=10, pady=10, sticky='w')
original_priceField_reverse = Entry(frame2, font=entry_font)
original_priceField_reverse.grid(row=1, column=1, padx=10, pady=10, sticky='w')

net_price_reverse = Label(frame2, text="Net Price:", font=label_font)
net_price_reverse.grid(row=2, column=0, padx=10, pady=10, sticky='w')
net_priceField_reverse = Entry(frame2, font=entry_font)
net_priceField_reverse.grid(row=2, column=1, padx=10, pady=10, sticky='w')

find_reverse = Button(frame2, text="Calculate GST", fg="black",
                     bg="light yellow", font=button_font, command=gst_calculator_reverse)
find_reverse.grid(row=3, column=1, padx=10, pady=10, sticky='w')

cgst_percent_reverse = Label(frame2, text="CGST Rate:", font=label_font)
cgst_percent_reverse.grid(row=4, column=0, padx=10, pady=10, sticky='w')
cgst_percentField_reverse = Entry(frame2, font=entry_font)
cgst_percentField_reverse.grid(row=4, column=1, padx=10, pady=10, sticky='w')

sgst_percent_reverse = Label(frame2, text="SGST Rate:", font=label_font)
sgst_percent_reverse.grid(row=5, column=0, padx=10, pady=10, sticky='w')
sgst_percentField_reverse = Entry(frame2, font=entry_font)
sgst_percentField_reverse.grid(row=5, column=1, padx=10, pady=10, sticky='w')

total_gst_label_reverse = Label(frame2, text="Total GST Amount:", font=label_font)
total_gst_label_reverse.grid(row=6, column=0, padx=10, pady=10, sticky='w')
total_gstField_reverse = Entry(frame2, font=entry_font)
total_gstField_reverse.grid(row=6, column=1, padx=10, pady=10, sticky='w')

clear_reverse = Button(frame2, text="Clear All", fg="black",
                       bg="light yellow", font=button_font, command=clearAll_reverse)
clear_reverse.grid(row=7, column=1, padx=10, pady=10, sticky='w')

gui.mainloop()
