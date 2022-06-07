import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
import re
from datetime import date, datetime
import noti
from noti import *

SIGUN = ["가평군", "고양시", "과천시", "광명시", "광주시", "구리시", "군포시", "김포시", "남양주시", "동두천시", "부천시", "성남시", "수원시", "시흥시", "안산시", "안성시", "안양시", "양주시", "양평군", "여주시", "연천군", "오산시", "용인시", "의왕시", "의정부시", "이천시", "파주시", "평택시", "포천시", "하남시", "화성시"]

def replyAptData(SIGUN_NM, user, CMPNM_NM): 
    global res_list
    res_list.clear()
    noti.getData( SIGUN_NM, CMPNM_NM )
    msg = '' 
    if res_list != []:
        noti.sendMessage(user, '다음 업체는 지역화폐 사용이 가능합니다.')
    for r in res_list: 
        if len(r+msg)+1>noti.MAX_MSG_LENGTH: 
            noti.sendMessage( user, msg ) 
            msg = r +'\n' 
        else: msg += r+'\n'
    if msg: 
        noti.sendMessage( user, msg ) 
    else: 
        noti.sendMessage( user, '해당 조건의 업체는 지역화폐 사용이 불가능합니다.')

def save( user, loc_param ): 
    conn = sqlite3.connect('users.db') 
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS \ users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try: 
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param)) 
    except sqlite3.IntegrityError: 
        noti.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' ) 
        return
    else: 
        noti.sendMessage( user, '저장되었습니다.' ) 
        conn.commit()

def check( user ): 
    conn = sqlite3.connect('users.db') 
    cursor = conn.cursor() 
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, locationTEXT, PRIMARY KEY(user, location) )') 
    cursor.execute('SELECT * from users WHERE user="%s"' % user)

    for data in cursor.fetchall(): 
        row = 'id:' + str(data[0]) + ', location:' + data[1] 
        noti.sendMessage( user, row )

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text': 
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.') 
        return
    text = msg['text'] 
    args = text.split(' ')
    if args[0] in SIGUN and len(args) == 2: 
        replyAptData( args[0], chat_id, args[1] ) 
    else:
        noti.sendMessage(chat_id, '지역명 ["가평군", "고양시", "과천시", "광명시", "광주시", "구리시", "군포시", "김포시", "남양주시", "동두천시", "부천시", "성남시", "수원시", "시흥시", "안산시", "안성시", "안양시", "양주시", "양평군", "여주시", "연천군", "오산시", "용인시", "의왕시", "의정부시", "이천시", "파주시", "평택시", "포천시", "하남시", "화성시"]과 \n상호명 순으로 입력해주세요.')

today = date.today() 
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', noti.TOKEN )

from noti import bot
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...') 

while 1: 
    time.sleep(10)