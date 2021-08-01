"""
Telegram Marketing Kit v0.3 [Control Panel]
==========================
Author       : Dagimal
E-mail       : daffagifariakmal@gmail.com
Release Date : 26-April-2021
Platform     : Python
Last Update  : 20-July-2021
--------------------------
Project ini adalah fork dari original author https://python.gotrained.com/author/majid-alizadeh/
dengan menambah beberapa fitur di dalamnya
"""
import os
#from scraper import scraper

# Header
print(
"""
 _____     _      _    _ _   
/__   \___| | ___| | _(_) |_ 
  / /\/ _ \ |/ _ \ |/ / | __|
 / / |  __/ |  __/   <| | |_ 
 \/   \___|_|\___|_|\_\_|\__|
 Telegram Marketing Kit v0.3
     Created By Dagimal
"""
)

def mainMenu():
	print("[1] TELEGRAM SCRAPER")
	print("[2] TELEGRAM ADDER")

#def inputChoice():
#	input("Ketik Nomor Untuk Memilih : ")
mainMenu() # call main_menu function
#inputChoice()
choice = input("Ketik Nomor Untuk Memilih : ")

if choice == "1":
	import scraper
elif choice == "2":
	import adder
else:
	print("INPUT ANDA SALAH !!!")
	print("HANYA ADA 2 PILIHAN!!!")
