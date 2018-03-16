import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class Editor:
	def __init__(self, elems):
		self.filename = None
		self.elements = elems

	def browse(self):
		self.filename = filedialog.askopenfilename(title = "Select NRO",filetypes = (("NRO Files","*.nro"),("All Files","*.*"))) or self.filename
		
		if self.filename:
			# enable all buttons and fields
			self.elements[0].configure(state = "active")
			for elem in self.elements[1:]:
				elem.configure(state = "normal")

# batch of UI input elements
elems = []
editor = Editor(elems)

root = tk.Tk()
root.title("NRO Asset Editor")

fileframe = tk.Frame(root)
fileframe.grid(row=0, column=2, columnspan=1)

tk.Button(fileframe, text="Load NRO...", command=editor.browse).grid(row=0, column=0)
saveb = tk.Button(fileframe, text="Save", state="disabled")
saveb.grid(row=0, column=1)
elems.append(saveb)

frame = tk.Frame(root)
frame.grid(row=3, column=2, columnspan=2)

tk.Label(frame, text="App Name").grid(row=0, column=0, padx=5)
t1 = tk.Entry(frame, state="disabled")
t1.grid(row=0, column=1, padx=5)
elems.append(t1)

tk.Label(frame, text="Author").grid(row=1, column=0, padx=5)
t2 = tk.Entry(frame, state="disabled")
t2.grid(row=1, column=1, padx=5)
elems.append(t2)

tk.Label(frame, text="Version").grid(row=2, column=0, padx=5)
t3 = tk.Entry(frame, state="disabled")
t3.grid(row=2, column=1, padx=5)
elems.append(t3)

b1 = tk.Button(frame, text="Open Image...", state="disabled")
b1.grid(row=3, column=1, padx=(50, 5))
elems.append(b1)

tk.Label(frame, text="GPLv3 License").grid(row=6, column=1, padx=(50, 5))
tk.Button(frame, text="Source code").grid(row=7, column=1, padx=(50, 5))

im = Image.open('default.jpg')
tkimage = ImageTk.PhotoImage(im)

tk.Label(frame, image=tkimage).grid(row=0, rowspan=8, column=2)

root.geometry("550x300")
root.resizable(0, 0)

root.mainloop()