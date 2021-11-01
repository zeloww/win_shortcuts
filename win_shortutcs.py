import winreg, sys
from time import sleep
from subprocess import Popen
from ctypes import windll, WinError
from urllib.request import urlopen, Request
from os import system, environ, path, listdir, remove, rename

raccourcis_text = """
                    ███████╗██╗  ██╗ ██████╗ ██████╗ ████████╗ ██████╗██╗   ██╗████████╗███████╗
                    ██╔════╝██║  ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██║   ██║╚══██╔══╝██╔════╝
                    ███████╗███████║██║   ██║██████╔╝   ██║   ██║     ██║   ██║   ██║   ███████╗
                    ╚════██║██╔══██║██║   ██║██╔══██╗   ██║   ██║     ██║   ██║   ██║   ╚════██║
                    ███████║██║  ██║╚██████╔╝██║  ██║   ██║   ╚██████╗╚██████╔╝   ██║   ███████║
                    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝
                                       1 > center taskbar | 4 > set wallpaper        by github.com/zeloww
                                  2 > transparent taskbar | 5 > programs & features
                                        3 > reset taskbar | 6 > blue light filter
"""

def make_admin():
	if not windll.shell32.IsUserAnAdmin():
		input("You aren't admin!")
		
		windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
		return exit()

def is_64_bits_windows():
	return 'PROGRAMFILES(X86)' in environ

def get_sys_parameters_info():
	if is_64_bits_windows():
		return windll.user32.SystemParametersInfoW

	return windll.user32.SystemParametersInfoA

def center_taskbar():
	input("Only works on Windows 11 !\nFor continue press enter")
	make_admin()

	registry_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced"

	try:
		key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_key, 0, winreg.KEY_ALL_ACCESS)
		winreg.SetValueEx(key, "TaskbarAl", 0, winreg.REG_DWORD, 1)

		return "Successfully center taskbar, now click on your background to update!"

	except Exception as e:
		return e

def transparent_taskbar():
	make_admin()

	registry_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced"

	try:
		key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_key, 0, winreg.KEY_ALL_ACCESS)
		winreg.SetValueEx(key, "UseOLEDTaskbarTransparency", 0, winreg.REG_DWORD, 1)

		return "Successfully set transparent taskbar, now click on your background to update!"

	except Exception as e:
		return e

def reset_taskbar():
	make_admin()

	registry_key_center = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
	registry_key_transparent = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced"

	try:
		key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_key, 0, winreg.KEY_ALL_ACCESS)
		winreg.DeleteValue(key, "UseOLEDTaskbarTransparency")

		print("Successfully reset transparent taskbar")

		key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_key, 0, winreg.KEY_ALL_ACCESS)
		winreg.SetValueEx(key, "TaskbarAl", 0, winreg.REG_DWORD, 1)

		print("Successfully reset center taskbar")

	except Exception as e:
		return e

	return "Successfully reset taskbar, now click on your background to update!"

def static_wallpaper(file:str=None, url:str=None):
	try:
		if url:
			headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}
			req = Request(url, headers=headers)

			response = urlopen(req).read()

			file = "static-wallpaper.png"
			with open(file, "wb") as image:
				image.write(response)
		
		file = path.abspath(file)
		
		sys_parameters_info = get_sys_parameters_info()
		r = sys_parameters_info(20, 0, file, 0)

		if url:
			remove(file)

		if not r:
			return WinError()

		if url:
			return "Successfully set wallpaper to '{}'!".format(url)

		else:
			return "Successfully set wallpaper to '{}'!".format(file)

	except Exception as e:
		return e

def gif_wallpaper(folder:str, delay:float):
	sys_parameters_info = get_sys_parameters_info()
	list_of_frames = listdir(folder)

	print("Press ctrl + c for stop gif wallpaper!\nSuccessfully set gif wallpaper to '{}'".format(folder))
	while True:
		for frame_path in list_of_frames:
			try:
				sys_parameters_info(20, 0, folder + "/" + frame_path, 0)
				sleep(delay)

			except KeyboardInterrupt:
				sys_parameters_info(20, 0, "None", 0)
				return"Successfully stop gif wallpaper of '{}'".format(folder)

def blue_light_filter():
	system(r"C:\Windows\System32\DpiScaling.exe")
	return "Successfully opened blue light filter settings!\nClick on 'Night Light Settings'"

def remove_programs():
	system(r"C:\Windows\System32\appwiz.cpl")
	return "Successfully opened Programs & Features in the Control Panel!"

def main():
	system("color d")
	while True:
		system("cls")
		print(raccourcis_text)

		choice = input(">>> ")

		if choice == "1":
			input(center_taskbar())

		elif choice == "2":
			input(transparent_taskbar())

		elif choice == "3":
			input(reset_taskbar())

		elif choice == "4":
			type_choice = input("gif or static? >>> ").lower()

			if type_choice in ["s", "static"]:
				file_choice = input("file path or url? >>> ").lower()

				if file_choice in ["f", "file"]:
					file = input("Enter file path >>> ")

					if not path.isfile(file):
						input("File not exist!")
						continue

					input(static_wallpaper(file=file))

				elif file_choice in ["u", "url"]:
					url = input("Enter url >>> ")
					input(static_wallpaper(url=url))

				else:
					input("Error, specified a good file choice please!")

			elif type_choice in ["g", "gif"]:
				print("Tips: You can get frames of a gif on 'https://ezgif.com/split'!")
				folder = input("Enter folder with frames path >>> ")
				delay = input("Enter delay of the frames >>> ")

				try:
					delay = float(delay)

				except:
					input("Error, please enter a valid delay!")
					continue

				if not path.isdir(folder):
					input("Folder not exist!")
					continue

				input(gif_wallpaper(folder=path.abspath(folder), delay=delay))

			else:
				input("Error, bad choice!")

		elif choice == "5":
			input(remove_programs())

		elif choice == "6":
			input(blue_light_filter())

if __name__ == "__main__":
	main()