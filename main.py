#!/usr/bin/python3

import time, os, sys, pyotp, json, shutil, base64
import tkinter
from tkinter import ttk
from tkinter.font import nametofont
from tkinter import messagebox
from json_file import JsonFile

app_path = os.path.dirname(sys.argv[0])

window = tkinter.Tk()
window.title("Py2FA Google Authenticator")
window.geometry("800x700")
window.resizable(False, False)

# Style
style = ttk.Style(window)
# Style theme
window.tk.call("source", app_path + "/forest-light.tcl")
window.tk.call("source", app_path + "/forest-dark.tcl")
# Set theme
style.theme_use("forest-dark")
# Dialog box font
window.option_add("*Dialog.msg.font", "roboto 16")

# Main frame
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
        if i % 2 == 0:
            treeview.insert("", tkinter.END, id=i, values=item_tuple, tags=("odd",))
        else:
            treeview.insert("", tkinter.END, id=i, values=item_tuple, tags=("even",))
        i = i + 1
    window.after(15000, update)
    print("Update", t)


# Show user codes
fr_codes = tkinter.LabelFrame(fr, text="2FA Codes", font="roboto 16")
fr_codes.grid(row=0, column=0)

treeFrame = ttk.Frame(fr_codes, padding=(10, 10))
treeFrame.grid(row=0)

treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

cols = ("Name", "Secret", "Code")
treeview = ttk.Treeview(
    treeFrame,
    show="headings",
    columns=cols,
    height=13,
    selectmode="browse",
    yscrollcommand=treeScroll.set,
    padding=(-4, -4),
    # displaycolumns=("Name", "Code"),
)

# Headings
treeview.heading(cols[0], text=cols[0], anchor=tkinter.W)
treeview.heading(cols[1], text=cols[1], anchor=tkinter.W)
treeview.heading(cols[2], text=cols[2], anchor=tkinter.E)

# Heading style
treeview.column("Name", width=200, stretch=True, anchor=tkinter.W)
treeview.column("Secret", width=200, stretch=True, anchor=tkinter.W)
treeview.column("Code", width=250, stretch=True, anchor=tkinter.E)

# Select event
treeview.bind("<<TreeviewSelect>>", selectItem)
# treeview.bind('<ButtonRelease-1>', selectItem)

# Style rows silver
treeview.tag_configure("odd", background="#3a4a5e", foreground="#ffffff")
treeview.tag_configure("even", background="#283240", foreground="#ffffff")
# # Blue
# treeview.tag_configure("odd", background="#0550ae", foreground="#ffffff")
# treeview.tag_configure("even", background="#0a3069", foreground="#ffffff")
# # Violet
# treeview.tag_configure("odd", background="#8250df", foreground="#ffffff")
# treeview.tag_configure("even", background="#a475f9", foreground="#ffffff")
# # Red
# treeview.tag_configure("odd", background="#82071e", foreground="#ffffff")
# treeview.tag_configure("even", background="#a40e26", foreground="#ffffff")

i = 0

for item_tuple in load_data():
    if i % 2 == 0:
        treeview.insert("", tkinter.END, id=i, values=item_tuple, tags=("odd",))
    else:
        treeview.insert("", tkinter.END, id=i, values=item_tuple, tags=("even",))
    i = i + 1

# Add
treeview.pack(fill="x")
# Scrollbar
treeScroll.config(command=treeview.yview)

# Style treeview
style.configure("Treeview.Heading", font=("Roboto", 13))
style.configure(
    "Treeview", font=("Roboto", 14), rowheight=30, highlightthickness=0, bd=0
)
# style.layout("Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})])
# nametofont("TkHeadingFont").configure(family="roboto", size=16, weight="bold")


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
fr_add_secret = tkinter.LabelFrame(
    fr, text="Add 2FA Secret", font="roboto 16", padx=5, pady=10
)
fr_add_secret.grid(row=1, column=0)
# fr_add_secret.pack(fill="x")

label_name = tkinter.Label(
    fr_add_secret, text="App name", font="roboto 14", anchor=tkinter.W
)
label_name.grid(row=0, column=0)

label_secret = tkinter.Label(
    fr_add_secret, text="App secret", font="roboto 14", anchor=tkinter.W
)
label_secret.grid(row=0, column=1)

input_name = tkinter.Entry(fr_add_secret, font="roboto 15", width=26, border=1)
input_name.grid(row=1, column=0, padx=5, pady=5)

input_secret = tkinter.Entry(fr_add_secret, font="roboto 15", width=26, border=1)
input_secret.grid(row=1, column=1, padx=5, pady=5)

button_add = tkinter.Button(
    fr_add_secret, text="Save", command=callback_add, font="roboto 15"
)
button_add.grid(row=2, column=1)

button_del = tkinter.Button(
    fr_add_secret, text="Delete", command=callback_del, font="roboto 15"
)
button_del.grid(row=2, column=0)

update()

window.mainloop()
