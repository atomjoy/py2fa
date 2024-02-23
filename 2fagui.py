#!/usr/bin/python3

import pyotp, time, json, os
import tkinter
from tkinter import ttk
from tkinter import messagebox

window = tkinter.Tk()
window.title("2FA Google Authenticator")
# window.geometry('300x200')
# window.resizable(False, False)

fr = tkinter.Frame(window)
fr.pack()

# Callbacks
def load_data():
	rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	with open(os.path.join(rel,'secrets.json'), 'r') as f:
		secrets = json.load(f)
		items = list(secrets.items())
		code_items = []
		for tuple_val in items:
			item = list(tuple_val)
			item.append(pyotp.TOTP(item[1]).now())
			code_items.append(tuple(item))
		print(code_items)
	return code_items

def selectItem(event):
	tree = event.widget
	current_item = tree.focus()
	item = tree.item(current_item)
	print("Item", item)
	if hasattr(item, 'values'):
		try:
			messagebox.showinfo('Current code', f'{item["values"][2]}')
			print("Id:", current_item, "Item:", item, "Code:", item["values"][2])
		except IndexError:
			print('')

def update():
	t=time.strftime('%I:%M:%S', time.localtime())
	treeview.delete(*treeview.get_children())
	i = 0
	for item_tuple in load_data():
		treeview.insert('', tkinter.END, id=i, values=item_tuple)
		i = i + 1
	window.after(30000, update)
	print("Update", t)

# Show user codes
fr_codes = tkinter.LabelFrame(fr, text="2FA Codes", font='times 21')
fr_codes.grid(row=0, column=0)

treeFrame = ttk.Frame(fr_codes)
treeFrame.grid(row=0, column=0, pady=10)
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

cols = ("Name", "Secret", "Code")
treeview = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=13, selectmode="browse")
treeview.column("Name", width=250)
treeview.bind('<<TreeviewSelect>>', selectItem)
# treeview.bind('<ButtonRelease-1>', selectItem)

for col_name in cols:
	treeview.heading(col_name, text=col_name)

i = 0

for item_tuple in load_data():
	treeview.insert('', tkinter.END, id=i, values=item_tuple)
	i = i + 1

treeview.pack()
treeScroll.config(command=treeview.yview)

# # Saving user secret callbacks
# def callback_button():
# 	name = input_name.get()
# 	secret = input_secret.get()
# 	print('Name', name, 'Secret', secret)
#
# # Saving user secret
# fr_add_secret = tkinter.LabelFrame(fr, text="Add secret", font='times 21')
# fr_add_secret.grid(row=1, column=0)

# label_name = tkinter.Label(fr_add_secret, text="App name")
# label_name.grid(row=0, column=0)

# label_secret = tkinter.Label(fr_add_secret, text="App secret")
# label_secret.grid(row=0, column=1)

# input_name = tkinter.Entry(fr_add_secret)
# input_name.grid(row=1, column=0)

# input_secret = tkinter.Entry(fr_add_secret)
# input_secret.grid(row=1, column=1)

# button_add = tkinter.Button(fr_add_secret, text="Save", command=callback_button)
# button_add.grid(row=2, column=1)

update()

window.mainloop()
