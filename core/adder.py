"""
Telegram Adder Group v0.2
==========================
Author   : Dagimal
E-mail   : daffagifariakmal@gmail.com
Date     : 26-April-2021
Platform : POSIX, Windows
--------------------------
Project ini adalah fork dari original author https://python.gotrained.com/author/majid-alizadeh/
dengan menambah beberapa fitur di dalamnya
"""

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from configparser import ConfigParser
import sys
import csv
import traceback
import time
import random

parser = ConfigParser.read()

last_add = open(".checkpoint","r").read()
saveFile = open(".checkpoint","w")


api_id = 123456
api_hash = 'YOUR_API_HASH'
phone = '+111111111111'
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Masukkan Kode: '))

input_file = sys.argv[1]
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
    if n % 50 == 0:
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
        print("Waiting for 60-180 Seconds...")
        time.sleep(random.randrange(60, 180))
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
    except UserPrivacyRestrictedError:
        print("Setting privasi user tidak memperbolehkan anda melakukan ini. Melewati.")
        print(user, file=saveFile)
        break
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue

