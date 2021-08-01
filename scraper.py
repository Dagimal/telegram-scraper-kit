"""
Telegram Group Scraper v0.3
==========================
Author   : Dagimal
E-mail   : daffagifariakmal@gmail.com
Date     : 26-April-2021
Platform : POSIX, Windows
--------------------------
Project ini adalah fork dari original author https://python.gotrained.com/author/majid-alizadeh/
dengan menambah beberapa fitur di dalamnya
"""

from core.CsvSplitter.split import split_csv
from core.CsvSplitter import *
from configparser import ConfigParser
from core.telethon.sync import TelegramClient
from core.telethon.tl.functions.messages import GetDialogsRequest
from core.telethon.tl.types import InputPeerEmpty
import csv
import os
import shutil

print(
"""
 _____     _      _    _ _   
/__   \___| | ___| | _(_) |_ 
  / /\/ _ \ |/ _ \ |/ / | __|
 / / |  __/ |  __/   <| | |_ 
 \/   \___|_|\___|_|\_\_|\__|
 Telegram Marketing Kit v0.3
     Created By Dagimal

   ++ TELEGRAM SCRAPER ++
"""
)

# def scraper():
parser = ConfigParser()
parser.read('config.conf')

api_id = parser.get('api_id', 'api-id')
api_hash = parser.get('api_hash', 'api-hash')
phone = parser.get('phone_number', 'phone')
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


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

print('Pilih group yang akan di scrape:')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1

g_index = input("Masukkan Nomor: ")
target_group=groups[int(g_index)]

# Create Group Dir
dir = 'output/'+target_group.title
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir)


# Create Zero Last Member File
def lastMember():
    text = open(dir+'/.lastmember','w')
    text.write('0')
    text.close
print('Fetching Members...')
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)

print('Menyimpan Ke Dalam File...')
with open("output/"+target_group.title+"/members.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])


# Split File
split_csv(target_group.title)
lastMember()           
print('Member Berhasil Di Scrape...')
