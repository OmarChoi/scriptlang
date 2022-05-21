from http.client import HTTPSConnection
import pprint

conn = None
server = "openapi.gg.go.kr"
ListMaket = []

def connectOpenAPIServer():
    global conn, server
    conn = HTTPSConnection(server)
    conn.set_debuglevel(0)

def SaveData(strXml):
    from xml.dom.minidom import parseString
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    global ListMaket
    itemElements = tree.iter("row")
    for row in itemElements:
        if row.find("LIVE_YN").text == 'Y':
            CMPNM_NM = row.find("CMPNM_NM")
            INDUTYPE_NM = row.find("INDUTYPE_NM")
            REFINE_LOTNO_ADDR = row.find("REFINE_LOTNO_ADDR")
            REFINE_ROADNM_ADDR = row.find("REFINE_ROADNM_ADDR")
            SIGUN_NM = row.find("SIGUN_NM")
            ListMaket.append({'Name' : CMPNM_NM.text, 'category' : INDUTYPE_NM.text, 'address_01' : REFINE_LOTNO_ADDR.text, 'address_02' : REFINE_ROADNM_ADDR.text, 'local' : SIGUN_NM.text})

def getData(): 
    global conn
    if conn == None: 
        connectOpenAPIServer()
    req = []
    for i in range(559):
        uri = "/RegionMnyFacltStus?KEY=8608449b435244de807e2eb607f8e793&pIndex=" + str(i + 1) + "&pSize=1000"
        conn.request("GET", uri)
        req.append(conn.getresponse())
        if int(req[i].status) == 200 : 
            SaveData(req[i].read())