import os
import webbrowser
from tkinter import *
from tkinter import filedialog

root = Tk()

def create_window():
	window = Toplevel(root)

	return window

def create_disk():
	window = create_window()
	window.title("Create Disk Image")
	window.geometry("180x240")
	window.resizable(False, False)
	window.transient(root)

	name_label = Label(window, text="Name")
	name_label.pack()

	name_input = Entry(window, width=10)
	name_input.pack()

	size_label = Label(window, text="Size (Mb)")
	size_label.pack()

	size_input = Entry(window, width=10)
	size_input.pack()

	location_label = Label(window, text="Location")
	location_label.pack()

	def get_directory():
		directory = filedialog.askdirectory()
		location_label.configure(text=directory)

	location_button = Button(window, text="Choose", command=get_directory)
	location_button.pack()

	space = Label(window, text="")
	space.pack()

	def create():
		name = name_input.get()
		size = size_input.get()
		location = location_label.cget("text")

		cmd = "qemu-img create -f qcow2 " + location + "/" + name + ".img " + size + "M"
		os.system(cmd)

		window.destroy()

	def cancel():
		window.destroy()

	create_button = Button(window, text="Create", command=create)
	create_button.pack()

	cancel_button = Button(window, text="Cancel", command=cancel)
	cancel_button.pack()

def boot_menu():
	window = create_window()
	window.title("Boot Menu")
	window.geometry("200x460")
	window.resizable(False, False)
	window.transient(root)

	cores_label = Label(window, text="Cores")
	cores_label.pack()

	cores_input = Entry(window, width=10)
	cores_input.pack()

	ram_label = Label(window, text="Ram")
	ram_label.pack()

	ram_input = Entry(window, width=10)
	ram_input.pack()

	architecture_label = Label(window, text="Architecture")
	architecture_label.pack()

	architecture = StringVar()

	choices = {"x86", "x86_64", "PowerPC"}
	architecture.set("x86")

	architecture_dropdown = OptionMenu(window, architecture, *choices)
	architecture_dropdown.pack()

	def get_disk_directory():
		directory = filedialog.askopenfilename()
		disk_label.configure(text=directory)

	disk_label = Label(window, text="Disk Image")
	disk_label.pack()

	disk_button = Button(window, text="Choose", command=get_disk_directory)
	disk_button.pack()

	def get_iso_directory():
		directory = filedialog.askopenfilename()
		iso_label.configure(text=directory)

	iso_label = Label(window, text="Iso file (leave blank to skip)")
	iso_label.pack()

	iso_button = Button(window, text="Choose", command=get_iso_directory)
	iso_button.pack()

	space = Label(window, text="")
	space.pack()

	def boot():
		cores = cores_input.get()
		ram = ram_input.get()
		disk_directory = disk_label.cget("text")
		iso_directory = iso_label.cget("text")

		if architecture.get() == "x86":
			if iso_directory == "Iso file (leave blank to skip)":
				cmd = "sudo qemu-system-i386 -m " + ram + " -boot d -enable-kvm -smp " + cores + " -net nic -net user -hda " + disk_directory
				os.system(cmd)
			else:
				cmd = "sudo qemu-system-i386 -m " + ram + " -boot d -enable-kvm -smp " + cores + " -net nic -net user -hda " + disk_directory + " -cdrom " + iso_directory
				os.system(cmd)

		elif architecture.get() == "x86_64":
			if iso_directory == "Iso file (leave blank to skip)":
				cmd = "sudo qemu-system-x86_64 -m " + ram + " -boot d -enable-kvm -smp " + cores + " -net nic -net user -hda " + disk_directory
				os.system(cmd)
			else:
				cmd = "sudo qemu-system-x86_64 -m " + ram + " -boot d -enable-kvm -smp " + cores + " -net nic -net user -hda " + disk_directory + " -cdrom " + iso_directory
				os.system(cmd)          

		elif architecture.get() == "PowerPC":
			if iso_directory == "Iso file (leave blank to skip)":
				cmd = "sudo qemu-system-ppc -M mac99 -m " + ram + " -boot c -smp " + cores + " -net nic -net user -hda " + disk_directory
				os.system(cmd)
			else:
				cmd = "sudo qemu-system-ppc -M mac99 -m " + ram + " -boot d -smp " + cores + " -net nic -net user -hda " + disk_directory + " -cdrom " + iso_directory
				os.system(cmd)

	def save_config():
		try:
			os.mkdir("./configurations")
		except:
			pass

		directory = "./configurations/" + save_name_input.get()

		cores = cores_input.get()
		ram = ram_input.get()
		disk_directory = disk_label.cget("text")
		iso_directory = iso_label.cget("text")

		with open(directory, "w+") as f:
			if architecture.get() == "x86":
				if iso_directory == "Iso file (leave blank to skip)":
					cmd = "sudo qemu-system-i386 -m " + ram + " -boot d -enable-kvm -smp " + cores + " -net nic -net user -hda " + disk_directory
					f.write(cmd)
				else:
					cmd = "sudo qemu-system-i386 -m " + ram + " -boot d -enable-kvm -smp " + cores + " -net nic -net user -hda " + disk_directory + " -cdrom " + iso_directory
					f.write(cmd)

			elif architecture.get() == "x86_64":
				if iso_directory == "Iso file (leave blank to skip)":
					cmd = "sudo qemu-system-x86_64 -m " + ram + " -boot d -enable-kvm -smp " + cores + " -net nic -net user -hda " + disk_directory
					f.write(cmd)
				else:
					cmd = "sudo qemu-system-x86_64 -m " + ram + " -boot d -enable-kvm -smp " + cores + " -net nic -net user -hda " + disk_directory + " -cdrom " + iso_directory
					f.write(cmd)          

			elif architecture.get() == "PowerPC":
				if iso_directory == "Iso file (leave blank to skip)":
					cmd = "sudo qemu-system-ppc -M mac99 -m " + ram + " -boot c -smp " + cores + " -net nic -net user -hda " + disk_directory
					f.write(cmd)
				else:
					cmd = "sudo qemu-system-ppc -M mac99 -m " + ram + " -boot d -smp " + cores + " -net nic -net user -hda " + disk_directory + " -cdrom " + iso_directory
					f.write(cmd)

	def cancel():
		window.destroy()

	create_button = Button(window, text="Boot", command=boot)
	create_button.pack()

	space = Label(window, text="")
	space.pack()

	save_name_label = Label(window, text="Configuration name")
	save_name_label.pack()

	save_name_input = Entry(window, width=10)
	save_name_input.pack()

	save_configuration_button = Button(window, text="Save", command=save_config)
	save_configuration_button.pack()

	space = Label(window, text="")
	space.pack()

	cancel_button = Button(window, text="Cancel", command=cancel)
	cancel_button.pack()

def install_dependencies():
	window = create_window()
	window.title("Dependencies")
	window.geometry("180x180")
	window.resizable(False, False)

	title = Label(window, text="Choose distribution")
	title.pack()

	distro = StringVar()

	values = {"Ubuntu" : "ubuntu",
		"Fedora" : "fedora",
		"OpenSuse" : "suse",
		"Archlinux" : "arch",}

	for (text, value) in values.items():
		Radiobutton(window, text=text, variable=distro, value = value).pack()

	def install():
		if distro.get() == "ubuntu":
			cmd = "sudo apt install qemu qemu-kvm libvirt-bin"
			os.system(cmd)
		elif distro.get() == "fedora":
			cmd = "sudo dnf install qemu qemu-kvm"
			os.system(cmd)
		elif distro.get() == "suse":
			cmd = "sudo zypper in qemu"
			os.system(cmd)
		elif distro.get() == "arch":
			cmd = "sudo pacman -S qemu"
			os.system(cmd)

	space = Label(window, text="")
	space.pack()

	install_button = Button(window, text="Install/Update", command=install)
	install_button.pack()

def visit_documentation():
	webbrowser.open("https://github.com/vinnyhorgan/Qemu.py")

def create_menubar():
	menubar = Menu(root)

	general = Menu(menubar, tearoff=0)
	general.add_command(label="Create Disk Image", command=create_disk)
	general.add_command(label="Boot Menu", command=boot_menu)
	general.add_separator()
	general.add_command(label="Quit", command=root.quit)
	menubar.add_cascade(label="General", menu=general)

	configure = Menu(menubar, tearoff=0)
	configure.add_command(label="Install/Update dependencies", command=install_dependencies)
	menubar.add_cascade(label="Configure", menu=configure)

	help = Menu(menubar, tearoff=0)
	help.add_command(label="Documentation", command=visit_documentation)
	menubar.add_cascade(label="Help", menu=help)

	root.config(menu=menubar)

def main():
	root.title("Qemu.py v1.0")
	root.geometry("320x200")
	root.resizable(False, False)

	create_menubar()

	version = Label(root, text="Qemu.py v1.0")
	version.place(x=0, y=180)

	def open_configuration():
		with open("./configurations/" + configuration_input.get(), "r") as f:
			cmd = f.readline()
			os.system(cmd)

	configurations_label = Label(root, text="Saved Configurations")
	configurations_label.pack()

	space = Label(root, text="")
	space.pack()

	try:
		files = os.listdir("./configurations")

		for filename in files:
			label = Label(root, text=filename)
			label.pack()
	except:
		pass

	space = Label(root, text="")
	space.pack()

	configuration_input = Entry(root, width=10)
	configuration_input.pack()

	launch_configuration_button = Button(root, text="Launch", command=open_configuration)
	launch_configuration_button.pack()

	root.mainloop()

main()