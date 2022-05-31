from hashlib import new
from msilib.schema import ListBox
from tkinter import *
import tkinter.ttk as ttk
from tkinter import font
from turtle import title
from APIConnect import *
from email.mime.text import MIMEText
import tkintermapview
from tkinter import messagebox

g_Tk = Tk()
g_Tk.title("경기도지역화폐가맹점정보")
g_Tk.geometry("600x700+450+100") # {width}x{height}+-{xpos}+-{ypos}

SIGUN_NM_Combo = None
INDUTYPE_NM_Combo = None
INPUT_CMPNM_NM = None
INPUT_MAIL_WIDJET = None
leftListBox = None
rightListBox = None
currentData = {}
alreadyCallRegion = []
content = []

photo0 = PhotoImage(file = "image/Search.png")
photo1 = PhotoImage(file = "image/Homepage.PNG")
photo2 = PhotoImage(file = "image/Map.png")
photo3 = PhotoImage(file = "image/Mail.png")

def printmap():
    global new
    global currentData

    if currentData != {}:
        new = Toplevel()

        map_widget = tkintermapview.TkinterMapView(new, width=800, height=500, corner_radius=0)
        map_widget.pack()

        marker_1 = map_widget.set_address(currentData['address'], marker=True)
        marker_1.set_text(currentData['Name'])
        map_widget.set_zoom(19)

def setmail():
    global new_m, INPUT_MAIL_WIDJET
    new_m = Toplevel()
    new_m.geometry("200x100+750+450")

    INPUT_MAIL_Text = Label(new_m,text='수신하실 메일 주소를 입력하세요', width=10,height=2)
    INPUT_MAIL_Text.pack(side="top", padx=5, expand=True, fill='x')
    INPUT_MAIL_WIDJET = Text(new_m, width=10,height=2)
    INPUT_MAIL_WIDJET.pack(side="top", padx=5, expand=True, fill='x')

    SendButton = Button(new_m, text= '메일 전송', command=sendMail)
    SendButton.pack(side="right", padx=10, expand=True)

def setsend(fromAddr , toAddr, msg):
    import smtplib
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()

    s.login('sgj9946@gmail.com', 'xahqeslixkobexmw')
    s.sendmail(fromAddr , [toAddr], msg.as_string())
    s.close()

def sendMail():
    global content, INPUT_MAIL_WIDJET, new_m

    receiver = INPUT_MAIL_WIDJET.get("1.0", "end")

    msg = MIMEText('\n'.join(content),_charset="utf8")
    msg['Subject'] = "가맹점 정보"
    setsend('sgj9946@naver.com', receiver, msg)
    content.clear()
    INPUT_MAIL_WIDJET = None
    new_m.destroy()
   
def event_for_listbox(event): # 리스트 선택 시 내용 출력
    global rightListBox, content, currentData

    temp = []
    selection = event.widget.curselection()
    if selection:
        currentData = {}
        index = selection[0]
        data = event.widget.get(index)
        temp = data.split("/")
        content.clear()
        rightListBox.delete(0,rightListBox.size())
        for i in range (0, 5):
            if temp[i] != "None":
                rightListBox.insert(i, temp[i])
                content.append(temp[i])
        currentData = {'Name' : str(temp[0]), 'address' : str(temp[3])}

def InitScreen():
    fontTitle = font.Font(g_Tk, size = 20, weight='bold', family='궁서체')
    fontNormal = font.Font(g_Tk, size= 15, weight='bold')

    frameTitle = Frame(g_Tk, padx=10, pady=10,bg='#1fffbf')
    frameTitle.pack(side="top", fill="x")

    frameClassification = Frame(g_Tk, pady=20, bg='#96d3ff')
    frameClassification.pack(side="top",fill="x")
   
    frameName = Frame(g_Tk, pady=10, bg='#96d3ff')
    frameName.pack(side="top", fill="x")

    frameList = Frame(g_Tk, padx=10, pady=30, bg='#96d3ff')
    frameList.pack(side="top", fill="x")

    frameETC = Frame(g_Tk, padx=10, bg='#1fffbf')
    frameETC.pack(side="bottom", fill="both", expand=True)

    MainText = Label(frameTitle,font = fontTitle, text="경기도 지역화폐 가맹점", bg= '#1fffbf')
    MainText.pack(anchor="center", fill="both")

    global SIGUN_NM_Combo
    SIGUN_NM_List = ["가평군", "고양시", "과천시", "광명시", "광주시", "구리시", "군포시", "김포시", "남양주시", "동두천시", "부천시", "성남시", "수원시", "시흥시", "안산시", "안성시", "안양시", "양주시", "양평군", "여주시", "연천군", "오산시", "용인시", "의왕시", "의정부시", "이천시", "파주시", "평택시", "포천시", "하남시", "화성시"]
    SIGUN_NM_Combo = ttk.Combobox(frameClassification, font=fontNormal, width = 10, height = 10, values=SIGUN_NM_List, state='readonly')
    SIGUN_NM_Combo.pack(side='left', padx=10, expand=True, fill='both')
    SIGUN_NM_Combo.set("시/군")

    global INDUTYPE_NM_Combo
    INDUTYPE_NM_List = ['음식', '골프', '병원', '미용', '레저', '학원', '헬스', '주유소', '가스충전소', '기타']
    INDUTYPE_NM_Combo = ttk.Combobox(frameClassification, font=fontNormal, width = 10, height = 10, values=INDUTYPE_NM_List, state='readonly')
    INDUTYPE_NM_Combo.pack(side='right', padx=10, expand=True, fill='both')
    INDUTYPE_NM_Combo.set("업종분류")

    global INPUT_CMPNM_NM
    INPUT_CMPNM_NM = Entry(frameName, font=fontNormal, width=26,borderwidth=12, relief='ridge')
    INPUT_CMPNM_NM.pack(side="left", padx=10, expand=True, fill='both')
   
    global photo0
    SearchButton = Button(frameName, image=photo0, command=onSearch)
    SearchButton.pack(side="right", padx=10, expand=True, fill='y')

    global leftListBox
    LScrollbar = Scrollbar(frameList)
    leftListBox = Listbox(frameList, selectmode='extended', font = fontNormal, width=20, height=15, borderwidth= 12, relief= 'ridge', yscrollcommand=LScrollbar.set)
    leftListBox.bind('<<ListboxSelect>>', event_for_listbox)
    leftListBox.pack(side='left', anchor='n')
    LScrollbar.pack(side='left', fill='y')
    LScrollbar.config(command=leftListBox.yview)

    global rightListBox
    rightListBox = Listbox(frameList, font = fontNormal, width=10, height=15, borderwidth= 12, relief= 'ridge')
    rightListBox.pack(side='right', anchor='n', expand=True, fill="x")

    global photo1, photo2, photo3

    HomepageLink = Button(frameETC, image = photo1, command=OpenPage)
    HomepageLink.pack(side="left", padx=10, fill="y")

    MapButton = Button(frameETC, image = photo2, command=printmap)
    MapButton.pack(side="right", padx=10, fill="y")

    MailButton = Button(frameETC, image = photo3, command=setmail)
    MailButton.pack(side="right", padx=10, fill="y")
       
def OpenPage():
    import webbrowser
    url = "https://www.gmoney.or.kr/base/main/view"
    webbrowser.open(url)

def onSearch():
    global SIGUN_NM_Combo, INDUTYPE_NM_Combo, INPUT_CMPNM_NM, leftListBox, rightListBox, ListMaket, currentData, alreadyCallRegion
    leftListBox.delete(0,leftListBox.size())
    rightListBox.delete(0,rightListBox.size())
    currentData = {}
    num = 0
    count = 0
    if SIGUN_NM_Combo.get() == "시/군":
        messagebox.showinfo(title='알림', message='지역을 선택해주세요.')
        return
    if not ListMaket:
        getData(SIGUN_NM_Combo.get())
    else:
        if SIGUN_NM_Combo.get() != ListMaket[0]['local']:
            ListMaket.clear()
            getData(SIGUN_NM_Combo.get())
            
    for i in ListMaket:
        if INPUT_CMPNM_NM.get() != '':
            if INPUT_CMPNM_NM.get() in str(i['Name']):
                _text = str(i['Name']) + "/" + str(i['local']) + "/" + str(i['category']) + "/" + str(i['address_01']) + "/" + str(i['address_02'] )
                leftListBox.insert(num, _text)
                
        else:
            if str(INDUTYPE_NM_Combo.get()) != "기타" and str(INDUTYPE_NM_Combo.get()) != '업종분류':
                if INDUTYPE_NM_Combo.get() in str(i['category']):
                    _text = str(i['Name']) + "/" + str(i['local']) + "/" + str(i['category']) + "/" + str(i['address_01']) + "/" + str(i['address_02'] )
                    leftListBox.insert(num, _text)
            else:
                _text = str(i['Name']) + "/" + str(i['local']) + "/" + str(i['category']) + "/" + str(i['address_01']) + "/" + str(i['address_02'] )
                leftListBox.insert(num, _text)         

InitScreen()
g_Tk.mainloop()