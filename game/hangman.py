import math
import random
from tkinter import *
from turtle import color # Import tkinter

    
wrongCount = 0
class Hangman:
    def __init__(self):
        self.draw()

    def draw(self):
        global wrongCount

        # 인자 : (x1,y1)=topleft, (x2,y2)=bottomright, start=오른쪽이 0도(반시계방향), extent=start부터 몇도까지인지
        #    style='pieslice'|'chord'|'arc'
        if wrongCount > -1:
            canvas.create_arc(20, 200, 100, 240, start = 0, extent = 180, style='chord', tags = "hangman") # Draw the base
            canvas.create_line(60, 200, 60, 20, tags = "hangman")  # Draw the pole
            canvas.create_line(60, 20, 160, 20, tags = "hangman") # Draw the hanger
        
        if wrongCount > 0:
            radius = 20 # 반지름
            # 머리 위에 짝대기  (0)
            canvas.create_line(160, 20, 160, 40, tags = "hangman") # Draw the hanger

        if wrongCount > 1:
            # Draw the circle
            # 머리  (1)
            canvas.create_oval(140, 40, 180, 80, tags = "hangman") # Draw the hanger

        if wrongCount > 2:
            # Draw the left arm (중심(160,60)에서 45도 움직인 지점의 x좌표는 cos로, y좌표는 sin으로 얻기)
            # 왼쪽 팔   (2)
            x1 = 160 - radius * math.cos(math.radians(45))
            y1 = 60 + radius * math.sin(math.radians(45))
            x2 = 160 - (radius+60) * math.cos(math.radians(45))
            y2 = 60 + (radius+60) * math.sin(math.radians(45))
            canvas.create_line(x1, y1, x2, y2, tags = "hangman")
        if wrongCount > 3:
            # 오른쪽 팔 (3)
            x1 = 160 - radius * math.cos(math.radians(135))
            y1 = 60 + radius * math.sin(math.radians(135))
            x2 = 160 - (radius+60) * math.cos(math.radians(135))
            y2 = 60 + (radius+60) * math.sin(math.radians(135))
            canvas.create_line(x1, y1, x2, y2, tags = "hangman")
        if wrongCount > 4:
            # 몸통  (4)
            canvas.create_line(160, 80, 160, 140, tags = "hangman") # Draw the hanger

        if wrongCount > 5:
            # 왼쪽 다리 (5)
            x2 = 160 - 60 * math.cos(math.radians(45))
            y2 = 140 + 60 * math.sin(math.radians(45))
            canvas.create_line(160, 140, x2, y2, tags = "hangman")

        if wrongCount > 6:
            # 오른쪽 다리 (6)
            x2 = 160 - 60 * math.cos(math.radians(135))
            y2 = 140 + 60 * math.sin(math.radians(135))
            
            canvas.create_line(160, 140, x2, y2, tags = "hangman")
            canvas.delete("answer")
            canvas.delete("wronganswer")
            canvas.create_text(200, 190, text= "정답 : " + "".join(answer),fill="black", tags="answer")
            canvas.create_text(200, 210, text= "게임을 계속하려면 ENTER를 누르세요", tags="wronganswer")
        
        elif '*' not in answer2:
            canvas.delete("answer")
            canvas.delete("wronganswer")
            canvas.create_text(200, 190, text= "".join(answer2) + " 맞았습니다.",fill="black", tags="answer")
            canvas.create_text(200, 210, text= "게임을 계속하려면 ENTER를 누르세요", tags="wronganswer")

        else:
            canvas.delete("answer")
            canvas.delete("wronganswer")
            canvas.create_text(200, 190, text= "정답 : " + "".join(answer2),fill="black", tags="answer")
            canvas.create_text(200, 210, text= "틀린글자 : " + "".join(wrongWords), tags="wronganswer")

# Initialize words, get the words from a file
infile = open("hangman.txt", "r")
words = infile.read().split()
answer = words[random.randrange(0,len(words))]
answer2 = ["*"] * len(answer)
wrongWords = []
window = Tk() # Create a window
window.title("행맨") # Set a title

def restart():
    global hangman
    global wrongCount
    global answer
    global answer2
    canvas.delete("answer")
    canvas.delete("wronganswer")
    canvas.delete("hangman")
    answer = words[random.randrange(0,len(words))]
    answer2 = ["*"] * len(answer)
    wrongWords.clear()
    wrongCount = 0
    hangman.draw()

def processKeyEvent(event):  
    global hangman
    global wrongCount
    if event.char >= 'a' and event.char <= 'z' and event.char not in wrongWords:
        findPos = answer.find(event.char)
        if  findPos == -1:
                wrongWords.append(event.char)
                wrongCount += 1
                hangman.draw()
                return
        for i in range(len(answer)):
            findPos = answer.find(event.char, i, len(answer))
            if findPos != -1:
                i = findPos
                answer2[i] = event.char   
                hangman.draw()
    elif event.keycode == 13 and ('*' not in answer2 or wrongCount > 6):
        restart()

width = 400
height = 280    
# 선, 다각형, 원등을 그리기 위한 캔버스를 생성
canvas = Canvas(window, bg = "white", width = width, height = height)
canvas.pack()

hangman = Hangman()

# Bind with <Key> event
canvas.bind("<Key>", processKeyEvent)
# key 입력 받기 위해 canvas가 focus 가지도록 함.
canvas.focus_set()

window.mainloop() # Create an event loop
