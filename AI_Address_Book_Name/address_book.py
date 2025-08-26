import sqlite3
from sqlite3 import Error
import tkinter as tk
from tkinter import messagebox
from typing import Optional

class AddressBook:
    def __init__(self, db_file: str):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.create_table()
        except Error as e:
            print(e)

    def create_table(self):
        sql_create_table = """CREATE TABLE IF NOT EXISTS contacts (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                phone text NOT NULL,
                                email text,
                                address text,
                                notes text
                            );"""
        try:
            if self.conn is not None:
                c = self.conn.cursor()
                c.execute(sql_create_table)
            else:
                print("Error: Database connection is not established.")
        except Error as e:
            print(e)

def add_contact(self, name: str, phone: str, email: str, address: str, notes: str) -> None:
    sql = ''' INSERT INTO contacts(name, phone, email, address, notes)
              VALUES(?,?,?,?,?) '''
    try:
        cur = self.conn.cursor()
        cur.execute(sql, (name, phone, email, address, notes))
        self.conn.commit()
        return cur.lastrowid
    except Error as e:
        print(e)

    def delete_contact(self, id):
        sql = 'DELETE FROM contacts WHERE id=?'
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (id,))
            self.conn.commit()
        except Error as e:
            print(e)
    def update_contact(
        self,
        id: int,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
        notes: Optional[str] = None
    ) -> None:
   
        sql = ''' UPDATE contacts
                  SET name = ?, phone = ?, email = ?, address = ?, notes = ?
                  WHERE id = ?'''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (name, phone, email, address, notes, id))
            self.conn.commit()
        except Error as e:
            print(e)

    def search_contact(self, name):
        sql = 'SELECT * FROM contacts WHERE name LIKE ?'
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (f'%{name}%',))
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)

    def display_contacts(self):
        sql = 'SELECT * FROM contacts'
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return rows
        except Error as e:
            print(e)

class GUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.address_book = AddressBook('address_book.db')
        self.name = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.address = tk.StringVar()
        self.notes = tk.StringVar()
        self.id = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text='Name').grid(row=0, column=0)
        tk.Entry(self.master, textvariable=self.name).grid(row=0, column=1)

        tk.Label(self.master, text='Phone').grid(row=1, column=0)
        tk.Entry(self.master, textvariable=self.phone).grid(row=1, column=1)

        tk.Label(self.master, text='Email').grid(row=2, column=0)
        tk.Entry(self.master, textvariable=self.email).grid(row=2, column=1)

        tk.Label(self.master, text='Address').grid(row=3, column=0)
        tk.Entry(self.master, textvariable=self.address).grid(row=3, column=1)

        tk.Label(self.master, text='Notes').grid(row=4, column=0)
        tk.Entry(self.master, textvariable=self.notes).grid(row=4, column=1)

        tk.Label(self.master, text='ID').grid(row=5, column=0)
        tk.Entry(self.master, textvariable=self.id).grid(row=5, column=1)

        tk.Button(self.master, text='Add Contact', command=self.add_contact).grid(row=6, column=0)
        tk.Button(self.master, text='Delete Contact', command=self.delete_contact).grid(row=6, column=1)
        tk.Button(self.master, text='Update Contact', command=self.update_contact).grid(row=7, column=0)
        tk.Button(self.master, text='Search Contact', command=self.search_contact).grid(row=7, column=1)
        tk.Button(self.master, text='Display Contacts', command=self.display_contacts).grid(row=8, column=0)

    def add_contact(self):
        self.address_book.add_contact(self.name.get(), self.phone.get(), self.email.get(), self.address.get(), self.notes.get())
        messagebox.showinfo('Contact Added', 'Contact added successfully')

    def delete_contact(self):
        self.address_book.delete_contact(int(self.id.get()))
        messagebox.showinfo('Contact Deleted', 'Contact deleted successfully')

    def update_contact(self):
        self.address_book.update_contact(int(self.id.get()), self.name.get(), self.phone.get(), self.email.get(), self.address.get(), self.notes.get())
        messagebox.showinfo('Contact Updated', 'Contact updated successfully')

    def search_contact(self):
        rows = self.address_book.search_contact(self.name.get())
        if rows:
            result = ''
            for row in rows:
                result += f'ID: {row[0]}\nName: {row[1]}\nPhone: {row[2]}\nEmail: {row[3]}\nAddress: {row[4]}\nNotes: {row[5]}\n\n'
            messagebox.showinfo('Contacts Found', result)
        else:
            messagebox.showinfo('No Contacts Found', 'No contacts found')

    def display_contacts(self):
        rows = self.address_book.display_contacts()
        if rows:
            result = ''
            for row in rows:
                result += f'ID: {row[0]}\nName: {row[1]}\nPhone: {row[2]}\nEmail: {row[3]}\nAddress: {row[4]}\nNotes: {row[5]}\n\n'
            messagebox.showinfo('Contacts', result)
        else:
            messagebox.showinfo('No Contacts', 'No contacts found')

root = tk.Tk()
gui = GUI(root)
root.mainloop()