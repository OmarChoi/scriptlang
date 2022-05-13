from tkinter import *

Turn = "red"

class Cell(Canvas):
    def __init__(self, parent, row, col, width = 20, height = 20):
        Canvas.__init__(self, parent, width = width, height = height, \
            bg = "blue", borderwidth = 2)
        self.color = "white"
        self.row = row
        self.col = col
        self.create_oval(4, 4, 20, 20, fill = "white", tags="oval")
        self.bind("<Button-1>", self.clicked)

    def clicked(self, event): 
        global Turn
        if self.color == "white" and Turn != None:
            self.color = Turn
            self.setColor(self.color)

    def setColor(self, color):
        global Turn
        self.delete("oval")         
        self.color = color
        self.create_oval(4, 4, 20, 20, fill = self.color, tags="oval")           
        checkstatus(self.color)   
        if Turn != None:
            Turn = "red" if (Turn == "yellow") else "yellow"
        
#코멘트 변경, 종료
def checkstatus(color):
    global Turn
    if iswon(color):
        button["text"] = Turn + " 승리!"
        Turn = None
    elif isfull():
        button["text"] = "승자 없음"
        Turn = None  

#white가 있다면 false, white가 없으면 true 변환
def isfull():
    for i in range(6):
        for j in range(7):   
             if cells[i][j].color == "white":
                return False
    return True

#사목완성 판정
def iswon(color):
    #가로 : ㅡ
    for i in range(6):
        for j in range(4):
            if cells[i][j].color == color and cells[i][j + 1].color == color and cells[i][j + 2].color == color and cells[i][j + 3].color == color:
                    return True

    #세로 : ㅣ
    for j in range(7):
        for i in range(3):
            if cells[i][j].color == color and cells[i + 1][j].color == color and cells[i + 2][j].color == color and cells[i + 3][j].color == color:
                 return True

    for i in range(3):
        for j in range(4):
            #우방향하향 대각 : \
            if cells[i][j].color == color and cells[i + 1][j + 1].color == color and cells[i + 2][j + 2].color == color and cells[i + 3][j + 3].color == color:
                return True

            #좌방향하향 대각 : /
            if cells[i][j + 3].color == color and cells[i + 1][j + 2].color == color and cells[i + 2][j + 1].color == color and cells[i + 3][j].color == color:
                return True

    return False

#새로 시작
def restart():
    pass

window = Tk() 
window.title("Connect Four") 

frame1 = Frame(window)
frame1.pack()

cells = []
for i in range(6):
    cells.append([])
    for j in range(7):       
        cells[i].append(Cell(frame1, 0, 0, width = 20, height = 20))
        cells[i][j].grid(row = i, column = j)

button = Button(window, text = "새로 시작")
button["text"] = "새로 시작"
button["command"] = restart

button.pack()

window.mainloop()
