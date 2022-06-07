import sys
import telepot
from pprint import pprint
from urllib.request import urlopen
import traceback
from xml.etree import ElementTree
from xml.dom.minidom import parseString
from http.client import HTTPSConnection
from urllib.parse   import quote


conn = None
server = "openapi.gg.go.kr"
checkEnd = False

# 봇 주소 : t.me/gyeonggi_money_bot

TOKEN = '5550686384:AAEDq1Vjq66vBnzC5VqHvk0OSASzz9Ben1k' 
MAX_MSG_LENGTH = 300

bot = telepot.Bot(TOKEN)
res_list = []

def connectOpenAPIServer():
    global conn, server
    conn = HTTPSConnection(server)
    conn.set_debuglevel(0)

def SaveData(strXml, Name):
    from xml.dom.minidom import parseString
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    global res_list, checkEnd
    itemElements = tree.iter("row")
    Head = tree.iter("head")
    checkIN = 0
    
    for head in Head:
        checkIN = 1
        
    if checkIN == 0:
        checkEnd = True

    for row in itemElements:
        if row.find("LIVE_YN").text == 'Y':
            CMPNM_NM = row.find("CMPNM_NM").text
            INDUTYPE_NM = row.find("INDUTYPE_NM").text
            REFINE_LOTNO_ADDR = row.find("REFINE_LOTNO_ADDR").text
            REFINE_ROADNM_ADDR = row.find("REFINE_ROADNM_ADDR").text
            SIGUN_NM = row.find("SIGUN_NM").text
            if Name in CMPNM_NM:
                if CMPNM_NM != None:
                    list = '상호명 : ' + CMPNM_NM + '\n'
                if SIGUN_NM != None:
                    list += '시군명 : ' +  SIGUN_NM + '\n'
                if INDUTYPE_NM != None:
                    list += '업종명 : ' + INDUTYPE_NM + '\n'
                if REFINE_LOTNO_ADDR != None:
                    list += '소재지도로명주소 : ' + REFINE_LOTNO_ADDR + '\n'
                if REFINE_ROADNM_ADDR != None:
                    list += '소재지지번주소 : ' + REFINE_ROADNM_ADDR + '\n'
                res_list.append(list) 

def getData(SIGUN_NM, Name): 
    global conn, checkEnd
    if conn == None: 
        connectOpenAPIServer()
    req = []
    for i in range(559):
        if checkEnd == True:
            checkEnd = False
            return
        count = 0
        uri = "/RegionMnyFacltStus?KEY=8608449b435244de807e2eb607f8e793&pIndex=" + str(i + 1) + "&pSize=1000&SIGUN_NM=" + quote(SIGUN_NM)
        conn.request("GET", uri)
        req.append(conn.getresponse())
        if int(req[i].status) == 200 : 
            SaveData(req[i].read(), Name) 

def sendMessage(user, msg): 
    try:
        bot.sendMessage(user, msg) 
    except:
        traceback.print_exception(*sys.exc_info(), file=sys.stdout)