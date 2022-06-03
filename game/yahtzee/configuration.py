from dice import *

class Configuration:

    configs = [
        "Categoty", "Ones", "Twos", "threes", "Fours", "Fives", "Sixes",
        "Upper Scores", "Upper Bonus(35)",
        "3 of a kind", "4 of a kind", "Full House(25)",
        "Small Straight(30)", "Large Straight(40)", "Yahtzee(50)", "Chance",
        "Lower Scores", "Total"
    ]

    @staticmethod
    def getConfigs():       # 정적 메소드 (객체 없이 사용 가능)
        return Configuration.configs

    # row에 따라 주사위 점수를 계산하여 반환. 
    # 예를 들어, row가 0이면 "Ones"가, 2이면 "Threes"가 채점되어야 함을 의미. 
    # row가 득점위치가 아닌 곳(즉, UpperScore, UpperBonus, LowerScore, Total 등)을 나타내는 경우 -1을 반환.
    @staticmethod
    def score(row, dices):       # 정적 메소드 (객체 없이 사용 가능)
        global configs
        Score = 0
        count={}
        for i in dices:
            try: count[i.getRoll()] += 1
            except: count[i.getRoll()]=1

        if row >= 0 and row <= 5:
            try: Score = count[row + 1] * ( row + 1 )
            except: pass
        elif row == 8:
            for n, cnt in count.items():
                if cnt == 3:
                    for n, cnt in count.items():
                        Score += n * cnt
                    break
        elif row == 9:
            for n, cnt in count.items():
                if cnt == 4:
                    for n, cnt in count.items():
                        Score += n * cnt
                    break 
        elif row == 10:
            tempCount = list(count.values())
            tempCount.sort()
            if len(count) == 2:
                if tempCount == [2, 3]:
                    Score = 25
        elif row == 11:
            temp = list(count.keys())
            temp.sort()
            tempstr = ''
            for i in temp:
                tempstr += str(i)
            if '1234' in tempstr or '2345'in tempstr or '3456'in tempstr:
                Score = 30  
        elif row == 12:
            if len(count) == 5:
                Score = 40
        elif row == 13:
            if len(count) == 1:
                Score = 50
        elif row == 14:
            for n, cnt in count.items():
                Score += n * cnt
        else:
            Score = -1

        return Score
