from msilib.schema import ListBox
from tkinter import *
import tkinter.ttk as ttk
from tkinter import font
from APIConnect import *

g_Tk = Tk()
g_Tk.title("경기도지역화폐가맹점정보")
g_Tk.geometry("600x700+450+100") # {width}x{height}+-{xpos}+-{ypos}

SIGUN_NM_Combo = None
INDUTYPE_NM_Combo = None
INPUT_CMPNM_NM = None
leftListBox = None
rightListBox = None

photo0 = PhotoImage(file = "Search.PNG")
photo1 = PhotoImage(file = "Homepage.PNG")
photo2 = PhotoImage(file = "Map.png")
photo3 = PhotoImage(file = "Mail.png")

def event_for_listbox(event): # 리스트 선택 시 내용 출력
    global rightListBox

    selection = event.widget.curselection()
    temp = []
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        temp = data.split("/")
        rightListBox.delete(0,rightListBox.size())
        for i in range (0, 5):
            if temp[i] != "None":
                rightListBox.insert(i, temp[i])
        

def InitScreen():
    fontTitle = font.Font(g_Tk, size = 18, weight='bold', family='바탕체')
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
    INDUTYPE_NM_List = ['소매업', '음식점업', '개인서비스업', '슈퍼/마트', '보건업', '교육서비스업', '기타'] 
    INDUTYPE_NM_Combo = ttk.Combobox(frameClassification, font=fontNormal, width = 10, height = 1, values=INDUTYPE_NM_List, state='readonly') 
    INDUTYPE_NM_Combo.pack(side='right', padx=10, expand=True, fill='both')
    INDUTYPE_NM_Combo.set("업종분류")

    global INPUT_CMPNM_NM
    INPUT_CMPNM_NM = Entry(frameName, font=fontNormal, width=26,borderwidth=12, relief='ridge')
    INPUT_CMPNM_NM.pack(side="left", padx=10, expand=True, fill='both')
    
    global photo0
    SearchButton = Button(frameName, image=photo0, command=onSearch)
    SearchButton.pack(side="right", padx=10, expand=True, fill='y')

    global leftListBox
    leftListBox = Listbox(frameList, selectmode='extended', font = fontNormal, width=10, height=15, borderwidth= 12, relief= 'ridge')
    leftListBox.bind('<<ListboxSelect>>', event_for_listbox)
    leftListBox.pack(side='left', anchor='n')

    global rightListBox
    rightListBox = Listbox(frameList, font = fontNormal, width=10, height=15, borderwidth= 12, relief= 'ridge')
    rightListBox.pack(side='right', anchor='n', expand=True, fill="x")

    global photo1, photo2, photo3

    HomepageLink = Button(frameETC, image = photo1, command=OpenPage)
    HomepageLink.pack(side="left", padx=10, fill="y")

    MapButton = Button(frameETC, image = photo2)
    MapButton.pack(side="right", padx=10, fill="y")

    MapButton = Button(frameETC, image = photo3)
    MapButton.pack(side="right", padx=10, fill="y")
    
def OpenPage():
    import webbrowser
    url = "https://www.gmoney.or.kr/base/main/view"
    webbrowser.open(url)

def onSearch():
    global SIGUN_NM_Combo
    global INDUTYPE_NM_Combo
    global INPUT_CMPNM_NM
    global leftListBox
    global ListMaket
    leftListBox.delete(0,leftListBox.size())
    num = 1
    for i in ListMaket:
        if INPUT_CMPNM_NM.get() != '':
            if str(i['Name']) == INPUT_CMPNM_NM.get():
                _text = str(i['Name']) + "/" + str(i['local']) + "/" + str(i['category']) + "/" + str(i['address_01']) + "/" + str(i['address_02'])
                leftListBox.insert(num - 1, _text)
        else:
            if str(INDUTYPE_NM_Combo.get() != "기타"):
                if str(i['category']) == INDUTYPE_NM_Combo.get() and str(i['local']) == SIGUN_NM_Combo.get():
                    _text = str(i['Name']) + "/" + str(i['local']) + "/" + str(i['category']) + "/" + str(i['address_01']) + "/" + str(i['address_02'])
                    leftListBox.insert(num - 1, _text)
            else:
                if str(i['local']) == SIGUN_NM_Combo.get():
                    _text = str(i['Name']) + "/" + str(i['local']) + "/" + str(i['category']) + "/" + str(i['address_01']) + "/" + str(i['address_02'])
                    leftListBox.insert(num - 1, _text)
                    
getData()
InitScreen()
g_Tk.mainloop()