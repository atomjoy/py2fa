#!/usr/bin/python3

import pyotp, time, json, os, shutil, base64
import tkinter
from tkinter import ttk
from tkinter import messagebox
from json_file import JsonFile

window = tkinter.Tk()
window.title("Py2FA Google Authenticator")
# window.geometry('300x200')
# window.resizable(False, False)

fr = tkinter.Frame(window)
fr.pack()


# Callbacks
def load_data():
    jf = JsonFile("secrets.json")
    return jf.getAll()


def selectItem(event):
    tree = event.widget
    current_item = tree.focus()
    item = tree.item(current_item)
    # print("Selected Item", item)
    try:
        if hasattr(item, "values"):
            code = format(item["values"][2], "06d")
            messagebox.showinfo("Code", code)
            # print("Id:", current_item, "Item:", item, "Code:", code)
    except (IndexError, Exception):
        # print("Item not selected")
        pass


def update():
    t = time.strftime("%H:%M:%S", time.localtime())
    treeview.delete(*treeview.get_children())
    i = 0
    for item_tuple in load_data():
        treeview.insert("", tkinter.END, id=i, values=item_tuple)
        i = i + 1
    window.after(15000, update)
    print("Update", t)


# Show user codes
fr_codes = tkinter.LabelFrame(fr, text="2FA Codes", font="roboto 16")
fr_codes.grid(row=0, column=0)

treeFrame = ttk.Frame(fr_codes)
treeFrame.grid(row=0, column=0, pady=10)
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

cols = ("Name", "Secret", "Code")
treeview = ttk.Treeview(
    treeFrame,
    show="headings",
    columns=cols,
    height=20,
    selectmode="browse",
    yscrollcommand=treeScroll.set,
)
treeview.column("Name", width=250)
treeview.bind("<<TreeviewSelect>>", selectItem)
# treeview.bind('<ButtonRelease-1>', selectItem)

for col_name in cols:
    treeview.heading(
        col_name,
        text=col_name,
    )

i = 0

for item_tuple in load_data():
    treeview.insert("", tkinter.END, id=i, values=item_tuple)
    i = i + 1

treeview.pack()
treeScroll.config(command=treeview.yview)


# Saving user secret callbacks
def callback_add():
    name = input_name.get()
    secret = input_secret.get()
    input_name.delete(0, "end")
    input_secret.delete(0, "end")
    js = JsonFile("secrets.json")
    if len(name) >= 3:
        if len(secret) >= 16:
            # print("Name", name, "Secret", secret)
            js.addItem(name, secret)
            update()


def callback_del():
    name = input_name.get()
    input_name.delete(0, "end")
    js = JsonFile("secrets.json")
    js.removeItem(name)
    update()


# Saving user secret
fr_add_secret = tkinter.LabelFrame(fr, text="Add secret", font="roboto 16")
fr_add_secret.grid(row=1, column=0)
# fr_add_secret.pack(fill="x")

label_name = tkinter.Label(fr_add_secret, text="App name")
label_name.grid(row=0, column=0)

label_secret = tkinter.Label(fr_add_secret, text="App secret")
label_secret.grid(row=0, column=1)

input_name = tkinter.Entry(fr_add_secret)
input_name.grid(row=1, column=0)

input_secret = tkinter.Entry(fr_add_secret)
input_secret.grid(row=1, column=1)

button_add = tkinter.Button(fr_add_secret, text="Append", command=callback_add)
button_add.grid(row=2, column=1)

button_del = tkinter.Button(fr_add_secret, text="Delete", command=callback_del)
button_del.grid(row=2, column=0)

update()

window.mainloop()
