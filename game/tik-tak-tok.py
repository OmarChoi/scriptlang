from ast import Delete
from cgitb import text
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import font
from setuptools import Command

g_Tk = Tk()
g_Tk.title("Tic-Tac-Toe")

currentToken = 'X'
statusLabel = ''
GameEnd = 0
images = {'O' : PhotoImage(file= "o.gif"), \
        'X' : PhotoImage(file= "x.gif"), \
        '' : PhotoImage(file= "empty.gif")}

label = [None] * 9
label_fill = [None] * 9
message = []
FrameFirstLine = Frame(g_Tk)
FrameFirstLine.pack(side="top", fill="both")
FrameSecondLine = Frame(g_Tk)
FrameSecondLine.pack(side="top", fill="both")
FrmaeThirdLine = Frame(g_Tk)
FrmaeThirdLine.pack(side="top", fill="both")
FrmaeFourthLine = Frame(g_Tk,pady=10)
FrmaeFourthLine.pack(side="top", fill="both", expand= True)

class Cell(Label):
        def __init__(self):
                super().__init__()
                self.image = images[""]
                for i in range(0,9):
                        if i < 3:
                                label[i]=Label(FrameFirstLine, image = images[""])
                                label[i].bind("<Button-1>", lambda e, n=i: self.onClick(e, n))
                                label[i].pack(side= "left", fill= "x")
                        elif i < 6:
                                label[i]=Label(FrameSecondLine, image = images[""])
                                label[i].bind("<Button-1>", lambda e, n=i: self.onClick(e, n))
                                label[i].pack(side= "left", fill= "x") 
                        elif i < 9:
                                label[i]=Label(FrmaeThirdLine, image = images[""])
                                label[i].bind("<Button-1>", lambda e, n=i: self.onClick(e, n))
                                label[i].pack(side= "left", fill= "x") 
                global currentToken
                global message
                fontTitle = font.Font(g_Tk, size = 7)
                message=Text(FrmaeFourthLine,font= fontTitle, width= 20, height= 0)
                message.insert("current", "{}차례".format(currentToken))
                message.pack(anchor="center", fill= "x") 

        def onClick(self, e, n):
                global currentToken
                global GameEnd
                global message

                if GameEnd == 1:
                        return

                if label_fill[n] == None:
                        if currentToken == 'X':
                                label[n].configure(image = images["X"])
                                label_fill[n] = 0
                                print("{}번째 칸 {}으로 변경".format(n, label_fill[n]))
                                currentToken = 'O'
                                self.checkWin()
                        else:
                                label[n].configure(image = images["O"])
                                label_fill[n] = 1
                                print("{}번째 칸 {}으로 변경".format(n, label_fill[n]))
                                currentToken = 'X'
                                self.checkWin()
                if GameEnd == 0:           
                        message.delete("1.0","end")
                        message.insert("current", "{}차례".format(currentToken))

        def checkWin(self):
                global GameEnd
                global message
                for i in range(0,7,3):
                        if label_fill[i] == label_fill[i + 1] and label_fill[i] == label_fill[i + 2]:
                                if label_fill[i] == 0:
                                        GameEnd = 1
                                        message.delete("1.0","end")
                                        message.insert("current", "X 승리! 게임이 끝났습니다.")

                                elif label_fill[i] == 1:
                                        GameEnd = 1
                                        message.delete("1.0","end")
                                        message.insert("current", "O 승리! 게임이 끝났습니다.")

                for i in range(0,2):
                        if label_fill[i] == label_fill[i + 3] and label_fill[i] == label_fill[i + 6]:
                                if label_fill[i] == 0:
                                        GameEnd = 1
                                        message.delete("1.0","end")
                                        message.insert("current", "X 승리! 게임이 끝났습니다.")
                                elif label_fill[i] == 1:
                                        GameEnd = 1
                                        message.delete("1.0","end")
                                        message.insert("current", "O 승리! 게임이 끝났습니다.")
                
                if label_fill[0] == label_fill[4] and label_fill[0] == label_fill[8]:
                        if label_fill[4] == 0:
                                GameEnd = 1
                                message.delete("1.0","end")
                                message.insert("current", "X 승리! 게임이 끝났습니다.")
                        elif label_fill[4] == 1:
                                GameEnd = 1
                                message.delete("1.0","end")
                                message.insert("current", "O 승리! 게임이 끝났습니다.")
                        return
                
                if label_fill[2] == label_fill[4] and label_fill[2] == label_fill[6]:
                        if label_fill[4] == 0:
                                GameEnd = 1
                                message.delete("1.0","end")
                                message.insert("current", "X 승리! 게임이 끝났습니다.")
                        elif label_fill[4] == 1:
                                GameEnd = 1
                                message.delete("1.0","end")
                                message.insert("current", "O 승리! 게임이 끝났습니다.")
                        return
                count = 0
                for i in range(0,9):
                        if label_fill[i] == None:
                                count = count + 1


                if count == 0:
                        GameEnd = 1
                        message.delete("1.0","end")
                        message.insert("current", "비김! 게임이 끝났습니다.")


Cell()
g_Tk.mainloop()