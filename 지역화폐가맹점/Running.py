from tkinter import *
from tkinter import font
from tkinter import messagebox
import tkintermapview
import tkinter.ttk as ttk
from email.mime.text import MIMEText
from APIConnect import *

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

classification = {
    "음식": ["음식점업", "일반한식", "갈비전문점", "카페/베이커리", "분식", "일반음식점", "서양음식", "한정식"], 
    "병원" : ["동물병원", "보건업", "병원", "병원/약국", "산후조리원", "약국", "한의원", "한약방", "한방병원",], 
    "교육" : ["교육서비스업", "기능학원", "대학등록금", "독서실", "교육용테이프판매", "과학기자재", "학원", "학습지 교육", "학원/교육", "문구용품", "보습학원", "예 체능계학원", "외국어학원", "컴퓨터학원"],
    "스포츠":["골프경기장", "골프연습장", "골프용품 전문점", "스포츠및여가관련서비스업", "스포츠 레져용품", "스포츠/헬스", "스포츠의류",  "수 영 장", "헬스클럽", ],
    "숙박업" : ["1급 호텔", "2급 호텔", "숙박업", "숙박/캠핑", "여관/기타숙박업"],
    "주유소": ["E1가스충전소", "GS 가스충전소", "GS주유소", "LPG 취급점", "SK가스충전소", "SK주유소", "쌍용S-OIL", "쌍용S-OIL 가스충전소", "현대정유 가스충전소", "현대정유(오일뱅크)"],
    "전자": ["가전제품", "가전/통신", "냉열기기", "기계공구", "보일러 펌프 샷시", "사무 통신기기수리"],
    "소매업": ["소매업", "가방", "건강식품", "CATV홈쇼핑", "기념품점", "국산신차판매", "구내매점(국가기관 등)", "골동품점", "공무원 연금 매점", "단체복", "내의판매", "슈퍼/마트", "미용재료", "슈퍼마켓", "스넥", "시장/거리", "신발", "안경", "애완동물", "액세서리", "시계", "아동의류", "악기점", "양품점"],
    "서비스업": ["신변잡화수리", "CATV", "가정용품수리", "개인서비스업", "가례서비스업", "견인서비스", "국산신차 직영부품 정비업소", "렌터카", "레져용품수리", "미용/뷰티/위생", "고속버스", "공공요금대행비스/소득공제비", "맞춤복점", "미용원", "법률회계서비스(개인)",\
                "법률회계서비스(법인)", "복지매장", "부동산 분양", "부동산 중개 임대", "부동산/인테리어", "사무서비스", "사진관", "산모/육아", "세차장", "세탁소", "소프트웨어", "손해보험", "안마시술소", "위탁급식업", "편의점" ],
    "여가" : ["도서/문화/공연", "당 구 장", "노 래 방", "관광여행", "레저", "레져업소", "문화취미기타", "볼 링 장", "서적", "수족관", "스크린골프", "여객선", "영화관"],
    "제조 및 유통업" : ["제조업", "건축용 요업제품", "목재 석재 철물", "민예 공예품", "보관및 창고업", "옷감 직물"],
    "농수산물" : ["농 축 수산품", "농,축협 직영매장", "농기계", "농축수산 가공품", "농협하나로클럽", "미곡상", "비료,사료,종자"],
}

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
   
def event_for_listbox(event):
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
    INDUTYPE_NM_List = ["음식", "병원", "교육" , "스포츠", "숙박업" , "주유소", "전자", "소매업", "서비스업", "여가", "제조 및 유통업", "농수산물", "모두표시"]
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
            if str(INDUTYPE_NM_Combo.get()) != "모두표시" and str(INDUTYPE_NM_Combo.get()) != '업종분류':
                if str(i['category']) in classification[INDUTYPE_NM_Combo.get()] :
                    _text = str(i['Name']) + "/" + str(i['local']) + "/" + str(i['category']) + "/" + str(i['address_01']) + "/" + str(i['address_02'] )
                    leftListBox.insert(num, _text)
            else:
                _text = str(i['Name']) + "/" + str(i['local']) + "/" + str(i['category']) + "/" + str(i['address_01']) + "/" + str(i['address_02'] )
                leftListBox.insert(num, _text)

    if INPUT_CMPNM_NM.get() != '':
        if leftListBox.size() == 0:
            messagebox.showinfo(title='알림', message='입력하신 업체는 지역화폐 사용이 불가능하거나\n해당 시/군에 존재하지 않습니다.')

InitScreen()
g_Tk.mainloop()