# RESET
import shutil
import os

print('Dengan Menjalankan Program Ini, Anda Akan Menghapus Checkpoint terakhir member yang anda tambahkan')
print('-----------------------------------------------')

def replaceAllCheckpoint():
    direktori = os.listdir('output')
    print(direktori)
    for destination in direktori:
        shutil.copyfile('core/.lastmember', 'output/'+destination+'/.lastmember')


def replaceCustom(target_group):
    shutil.copyfile('core/.lastmember','output/'+target_group+'/.lastmember')

print('[1] Hapus Semua')
print('[2] Pilih Group')
question = input('>> ')

if question == '1':
    replaceAllCheckpoint()
elif question == '2':
    dirList = os.listdir('output')
    i=0
    for direktori in dirList:
        print(str(i) + '- ' + direktori)
        i+=1
    g_index = input("Masukkan nomor: ")
    target_group=groups[int(g_index)]
    replaceCustom(target_group)