"""
Telegram Group Adder v0.3
==========================
Author   : Dagimal
E-mail   : daffagifariakmal@gmail.com
Date     : 26-April-2021
Platform : POSIX, Windows
--------------------------
Project ini adalah fork dari original author https://python.gotrained.com/author/majid-alizadeh/
dengan menambah beberapa fitur di dalamnya

This Version[0.3] -----> Auto Change API via CSV
                         Auto Save, automatic continue ...
                         Remove main menu for performance [DONE]
     |
     | COMING SOON ...
     |
     v
Next Version[0.4] ---> Coming Soon ...
                       Auto Ganti Nomor Setiap Flood
                       Ganti Conf Dalam Bentuk CSV
		       Compile To Exe
"""

from configparser import ConfigParser
from core.telethon.sync import TelegramClient
from core.telethon.tl.functions.messages import GetDialogsRequest
from core.telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from core.telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from core.telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random
import os

print(
"""
 _____     _      _    _ _   
/__   \___| | ___| | _(_) |_ 
  / /\/ _ \ |/ _ \ |/ / | __|
 / / |  __/ |  __/   <| | |_ 
 \/   \___|_|\___|_|\_\_|\__|
 Telegram Marketing Kit v0.3
     Created By Dagimal

   ++ TELEGRAM ADDER ++
"""
)

#last_add = open(".checkpoint","r").read()
#saveFile = open(".checkpoint","w")

parser = ConfigParser()
parser.read('config.conf')

api_id = parser.get('api_id', 'api-id')
api_hash = parser.get('api_hash', 'api-hash')
phone = parser.get('phone_number', 'phone')
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Masukkan Kode: '))

print('Daftar Grup Yang Sudah Anda Scrape: ')
dirList = os.listdir('output')
i=0
for direktori in dirList:
    print(str(i) + '- ' + direktori)
    i+=1

print('Pilih Hasil Scrape: (Cukup Masukkan Nomor)')
dirIndex = input('>> ')

lastMember = open('output/'+dirList[int(dirIndex)]+'/.lastmember').read() # Check Last Member
print('Member Terakhir Yang Anda Tambahkan Adalah '+str(lastMember)+', Ada '+str(len(dirList[int(dirIndex)]))+' File CSV')
print('--------------------')
print('[1] Add Last Member')
print('[2] Custom')
memberChoice = input('>> ')

if memberChoice == '1':
	direktori = 'output/'+dirList[int(dirIndex)]
	if lastMember == '0':
		input_file = direktori+'/members.csv'
	else:
		input_file = 'output/'+dirList[int(dirIndex)]+'/members'+lastMember+'.csv'
elif memberChoice == '2':
	memberList = os.listdir('output/'+dirList[int(dirIndex)])
	i=0
	for daftarMember in memberList:
		print(str(i) + '- ' + daftarMember)
		i+=1
	pilihMember = input('Cukup Masukkan Nomor : ')
	input_file = 'output/'+dirList[int(dirIndex)]+'/'+memberList[int(pilihMember)]
else:
	print('inputan salah!')

users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

print('Pilih group tujuan: ')
i=0
for group in groups:
    print(str(i) + '- ' + group.title)
    i+=1

g_index = input("Masukkan nomor: ")
target_group=groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

mode = int(input("Masukkan [1] untuk menambahkan dari username atau [2] untuk menambahkan dari ID: "))

n = 0

for user in users:
    n += 1
    if n % 50 == 0: # Maksimal add member per hari setiap akun telegram
        time.sleep(900)
    try:
        print ("Adding {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Mode Tidak Valid. Coba Lagi.")
        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
        print("Tunggu 5-10 Detik...")
        time.sleep(random.randrange(5, 10))
    except PeerFloodError:
        print("Telegram Flood Error. Script berhenti sekarang. Coba lagi lain kali atau ganti nomor...")
    except UserPrivacyRestrictedError:
        print("Setting privasi user tidak memperbolehkan anda melakukan ini. Melewati...")
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue

