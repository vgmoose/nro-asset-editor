import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import io

class Asset:
	def __init__(self, offset):
		self.nacp = bytearray([])
		self.icon = bytearray([])
		self.romfs = bytearray([])
		
		self.offset = offset
		
	# load this asset object with data from a bunch of bytes
	# at the end of a .nro file (after the nro.size)
	def load(self, data):
		# get icon data
		offset = 0x4 + 0x4
		
		icon_pos = int.from_bytes(data[offset:offset+0x8], "little")
		icon_size = int.from_bytes(data[offset+0x8:offset+0x10], "little")
		self.icon += data[icon_pos:icon_pos+icon_size]
		offset += 0x10
		
		nacp_pos = int.from_bytes(data[offset:offset+0x8], "little")
		nacp_size = int.from_bytes(data[offset+0x8:offset+0x10], "little")
		self.nacp += data[nacp_pos:nacp_pos+nacp_size]
		offset += 0x10
		
		romfs_pos = int.from_bytes(data[offset:offset+0x8], "little")
		romfs_size = int.from_bytes(data[offset+0x8:offset+0x10], "little")
		self.romfs += data[romfs_pos:romfs_pos+romfs_size]
		offset += 0x10
		
		# we need to load human readable strings out of the nacp
		self.name    = self.nacp[0:0x200].decode("utf-8").strip("\x00")
		self.author =  self.nacp[0x200:0x300].decode("utf-8").strip("\x00")
		self.version = self.nacp[0x3060:0x3070].decode("utf-8").strip("\x00")
		
	# return the bytes that makeup this object, based on the fields
	def getBytes(self):
		# asset header
		ret = b"ASET"
		ret += bytearray([0, 0, 0, 0])
		
		offset = self.offset + 0x38
		
		# first asset section, icon
		ret += (offset).to_bytes(8, "little")
		icon_size = len(self.icon)
		ret += (icon_size).to_bytes(8, "little")
		offset += icon+size
		
		# 2nd asset section, nacp metadata
		ret += (offset).to_bytes(8, "little")
		nacp_size = len(self.nacp)
		ret += (nacp_size).to_bytes(8, "little")
		offset += nacp_size
		
		# 3rd asset section, romfs
		ret += (offset).to_bytes(8, "little")
		romfs_size = len(self.romfs)
		ret += (romfs_size).to_bytes(8, "little")
		offset += romfs_size
		
		# write data bytes
		ret += self.icon
		ret += self.nacp
		ret += self.romfs
		
		# all done
		return ret

class Editor:
	def __init__(self, elems):
		self.filename = None
		self.elements = elems
		
		self.name = tk.StringVar()
		self.name.set("Untitled Homebrew")
		self.author = tk.StringVar()
		self.author.set("Unknown Author")
		self.version = tk.StringVar()
		self.version.set("0.0.0")
		
		self.image = None
		self.data = None
		self.nrosize = 0
		
	# prompt for an image file
	def browse_image(self):
		# load either the new image or the default one
		img_url = filedialog.askopenfilename(title = "Select image file",filetypes = (("PNG Files","*.png"),("JPG Files","*.jpg"),("JPEG Files","*.jpeg"), ("GIF Files","*.gif"), ("BMP Files","*.bmp"), ("TGA Files","*.tga"), ("All Files","*.*"))) or 'default.jpg'
		
		self.image = Image.open(img_url).convert("RGB")
		self.image = self.image.resize((256, 256), Image.ANTIALIAS)
		
		buffer = io.BytesIO()
		self.image.save(buffer,format="JPEG")
		self.image = Image.open(buffer)
		
		image2 = ImageTk.PhotoImage(self.image)
		self.imagebox.configure(image=image2)
		self.imagebox.image = image2
		
	# update the current NRO with the new asset data
	def saveNRO(self):
		with open(self.filename, "wb") as nro:
			nro.write(self.asset.getBytes())
			nro.flush()

	# prompt for a file browser to select a .NRO file to extract data from
	def browse(self):
		self.filename = filedialog.askopenfilename(title = "Select NRO",filetypes = (("NRO Files","*.nro"),("All Files","*.*"))) or self.filename
		
		# load out some info
		with open(self.filename, "rb") as binary:
			self.data = binary.read()
			data = self.data
			
			# verify NRO0 format
			if data[0x10:0x14] != b"NRO0":
				return False
			
			# get the filesize, so we can go to the assets section
			self.nrosize = int.from_bytes(data[0x18:0x1C], byteorder="little")
			size = self.nrosize
			
			# check for ASET data
			self.asset = Asset(size)
			asset = self.asset
			if len(data) > size+4 and data[size:size+0x4] == B"ASET":
				# load the asset data
				self.asset.load(bytearray(data[size:]))
				
				self.name.set(asset.name)
				self.author.set(asset.author)
				self.version.set(asset.version)
				
				self.image = Image.open(io.BytesIO(asset.icon))
				image2 = ImageTk.PhotoImage(self.image)
				self.imagebox.configure(image=image2)
				self.imagebox.image = image2
				
				# truncate the old assset data from memory
				self.data = data[:size]
				
		
		if self.filename:
			# enable all buttons and fields
			self.elements[0].configure(state = "active")
			for elem in self.elements[1:]:
				elem.configure(state = "normal")

				
root = tk.Tk()
root.title("NRO Asset Editor")

# batch of UI input elements
elems = []
editor = Editor(elems)

# frame containing load and save buttons
fileframe = tk.Frame(root)
fileframe.grid(row=0, column=2, columnspan=1)

tk.Button(fileframe, text="Load NRO...", command=editor.browse).grid(row=0, column=0)
saveb = tk.Button(fileframe, text="Save", state="disabled", command=editor.saveNRO)
saveb.grid(row=0, column=1)
elems.append(saveb)

frame = tk.Frame(root)
frame.grid(row=3, column=2, columnspan=2)

# main text entry boxes (disabled by default)
tk.Label(frame, text="App Name").grid(row=0, column=0, padx=5)
t1 = tk.Entry(frame, state="disabled", textvariable=editor.name)
t1.grid(row=0, column=1, padx=5)
elems.append(t1)

tk.Label(frame, text="Author").grid(row=1, column=0, padx=5)
t2 = tk.Entry(frame, state="disabled", textvariable=editor.author)
t2.grid(row=1, column=1, padx=5)
elems.append(t2)

tk.Label(frame, text="Version").grid(row=2, column=0, padx=5)
t3 = tk.Entry(frame, state="disabled", textvariable=editor.version)
t3.grid(row=2, column=1, padx=5)
elems.append(t3)

b1 = tk.Button(frame, text="Open Image...", state="disabled", command=editor.browse_image)
b1.grid(row=3, column=1, padx=(50, 5))
elems.append(b1)

#tk.Label(frame, text="GPLv3 License").grid(row=6, column=1, padx=(50, 5))
#tk.Button(frame, text="Source code").grid(row=7, column=1, padx=(50, 5))

# icon preview
im = Image.open('default.jpg')
tkimage = ImageTk.PhotoImage(im)

canvas = tk.Label(frame, image=tkimage)
canvas.grid(row=0, rowspan=8, column=2)
editor.imagebox = canvas

root.geometry("550x300")
root.resizable(0, 0)

root.mainloop()