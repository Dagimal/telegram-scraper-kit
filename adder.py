"""
Telegram Group Adder v0.2
==========================
Author   : Dagimal
E-mail   : daffagifariakmal@gmail.com
Date     : 26-April-2021
Platform : POSIX, Windows
--------------------------
Project ini adalah fork dari original author https://python.gotrained.com/author/majid-alizadeh/
dengan menambah beberapa fitur di dalamnya

This Version[0.2] -----> ConfigParser
     |
     | COMING SOON ...
     |
     v
Next Version[0.3] -----> Auto Change API via CSV
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

input_file = '../output/members.csv'
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

print('Pilih group yang ingin di tambahkan member:')
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
        sleep(900)
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
        print(user, file=saveFile)
        break
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue

