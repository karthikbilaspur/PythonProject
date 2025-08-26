from tkinter import *

def clear_all():
    Player1_field.delete(0, END)
    Player2_field.delete(0, END)
    Status_field.delete(0, END)
    Player1_field.focus_set()
    return

def tell_status():
    p1 = Player1_field.get()
    p2 = Player2_field.get()
    p1 = p1.replace(" ", "")
    p2 = p2.replace(" ", "")
    p1 = list(p1)
    p2 = list(p2)
    Status_field.delete(0, END)
    Status_field.insert(0, result_flame(p1, p2))

def result_flame(x, y):
    # FLAMES algorithm
    for i in x[:]:
        if i in y:
            x.remove(i)
            y.remove(i)
    count = len(x) + len(y)
    result = ["Friends", "Love", "Affection", "Marriage", "Enemy", "Siblings"]
    while len(result) > 1:
        split_index = (count % len(result) - 1)
        if (split_index >= 0):
            right = result[split_index + 1:]
            left = result[:split_index]
            result = right + left
        else:
            result = result[:len(result) - 1]
    return result[0]

if __name__ == "__main__":
    root = Tk()
    root.configure(background='light pink')
    root.geometry("350x125")
    root.title("Flames Game")

    label1 = Label(root, text="Name 1 ", fg='black', bg='light green')
    label2 = Label(root, text="Name 2 ", fg='black', bg='light blue')
    label3 = Label(root, text="Relationship Status", fg='black', bg='#FFE4C4')

    label1.grid(row=1, column=0, sticky="E")
    label2.grid(row=2, column=0, sticky="E")
    label3.grid(row=4, column=0, sticky="E")

    Player1_field = Entry(root)
    Player2_field = Entry(root)
    Status_field = Entry(root)

    Player1_field.grid(row=1, column=1, ipadx="50")
    Player2_field.grid(row=2, column=1, ipadx="50")
    Status_field.grid(row=4, column=1, ipadx="50")

    button1 = Button(root, text="Calculate FLAMES", bg="#FF7F50", fg="black", command=tell_status)
    button2 = Button(root, text="Clear", bg="#CD5C5C", fg="black", command=clear_all)

    button1.grid(row=3, column=1)
    button2.grid(row=5, column=1)

    root.mainloop()