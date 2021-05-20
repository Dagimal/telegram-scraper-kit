"""
Telegram Marketing Kit v0.2
==========================
Author   : Dagimal
E-mail   : daffagifariakmal@gmail.com
Date     : 26-April-2021
Platform : Python
--------------------------
Project ini adalah fork dari original author https://python.gotrained.com/author/majid-alizadeh/
dengan menambah beberapa fitur di dalamnya
"""
import os
from core.rich import *

# Header
print(
"""
 _____     _      _    _ _   
/__   \___| | ___| | _(_) |_ 
  / /\/ _ \ |/ _ \ |/ / | __|
 / / |  __/ |  __/   <| | |_ 
 \/   \___|_|\___|_|\_\_|\__|
 Telegram Marketing Kit v0.2
     Created By Dagimal
"""
)
def teleScraper():
	import core.scraper
def teleAdder():
	import core.adder
def mainMenu():
	print("[1] TELEGRAM SCRAPER :sun_with_face:")
	print("[2] TELEGRAM ADDER :coffee:")

#def inputChoice():
#	input("Ketik Nomor Untuk Memilih : ")
mainMenu() # call main_menu function
#inputChoice()
choice = input("Ketik Nomor Untuk Memilih : ")

if choice == "1":
	teleScraper()
elif choice == "2":
	teleAdder()
else:
	print("[red]INPUT ANDA SALAH !!![/red] :no_entry_sign:")
	print("HANYA ADA [red]2[/red] PILIHAN!!!")
