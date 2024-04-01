import random

class Yacht:
    def __init__(self):
        self.dices = []
        self.choiced_dice = []
        self.rolled = []
        self.dice_max = 5
        self.hands = {
            "1":0, 
            "2":0, 
            "3":0, 
            "4":0, 
            "5":0, 
            "6":0, 
            "Choice":0,
            "Four of a kind":0, 
            "Full house":0, 
            "S Straight":0,
            "L Straight":0, 
            "Yacht":0
        }
        self.score_board = {
            "1":"-", 
            "2":"-", 
            "3":"-", 
            "4":"-", 
            "5":"-",
            "6":"-",
            "Bonus":"-",
            "Choice":"-",
            "Four of a kind":"-", 
            "Full house":"-", 
            "S Straight":"-",
            "L Straight":"-",
            "Yacht":"-"
        }

    def roll(self):
        self.choiced_dice = []
        self.rolled = [random.randint(1,6) for i in range(self.dice_max)]
        self.dices = self.rolled
        self.dices.sort()
    
    def reroll(self, rolls:int):
        self.rolled = [random.randint(1,6) for i in range(rolls)]
        self.dices = self.choiced_dice + self.rolled
        self.dices.sort()

    def choice(self, indexes):
        self.choiced_dice = [self.dices[a] for a in indexes]
        
    def check(self):
        self.dices.sort()
        self.hands = {
            "1":0, 
            "2":0, 
            "3":0, 
            "4":0, 
            "5":0, 
            "6":0, 
            "Choice":0,
            "Four of a kind":0, 
            "Full house":0, 
            "S Straight":0,
            "L Straight":0, 
            "Yacht":0
        }
        
        # 1〜6
        for i in range(6):
            diceNum = i + 1
            self.hands[f"{diceNum}"] = sum([j for j in self.dices if j == diceNum])
        
        # choice
        self.hands["Choice"] = sum(self.dices)
        
        # four of a kind
        for i in reversed(range(6)):
            diceNum = i + 1
            if self.dices.count(diceNum) >= 4:
                self.hands["Four of a kind"] = sum(self.dices)
                break
        
        # full house
        for i in reversed(range(6)):
            diceNumThree = i + 1
            if self.dices.count(diceNumThree) == 3:
                for i in reversed(range(6)):
                    diceNumTwo = i + 1
                    if self.dices.count(diceNumTwo) == 2:
                        self.hands["Full house"] = sum(self.dices)
                        break
                break
        
        # S straight / L straight
        joined = "".join(map(str, list(set(self.dices))))
        is_LS = "12345" in joined or "23456" in joined
        is_SS = is_LS or ("1234" in joined or "2345" in joined or "3456" in joined)
        if is_LS:
            self.hands["L Straight"] = 30
        if is_SS:
            self.hands["S Straight"] = 15
            
        # Yacht
        for i in reversed(range(6)):
            diceNum = i + 1
            if self.dices.count(diceNum) == 5:
                self.hands["Yacht"] = 50
                
    def check_bonus(self):
        if self.score_board["Bonus"] != "-":
            return
        
        sum = 0
        for k in [f"{i}" for i in range(6)]:
            if self.score_board[k] == "-":
                continue
            else:
                sum += int(self.score_board[k])
        
        if sum >= 63:
            self.score_board["Bonus"] = "35"
                        
def title():
    print("input command ▼")
    print("s: start game ▼ \ne: end game ▼")
    title_input = input()
    if title_input == "e":
        exit()
    if title_input == "s":
        print("start!")

def ingame(game: Yacht):
    input("press Enter to Roll ▼")
    game.roll()
    print(game.dices)
    rr_limit = 3
    while rr_limit > 0:
        print("----------------------------")
        print("reroll, choice or decide ▼")
        print("input 'd' and Enter. dices decide ▼")
        print("input 'c {num} {num} ....' and Enter. dices choiced and reroll ▼")
        print("input 'r' and Enter. dices not choiced and reroll ▼")
        val = input()
        if val == "r":
            game.reroll()
            print("reroll: " + game.rolled)
            rr_limit -= 1
        if val == "d":
            break
        if "c" in val:
            game.choice([int(i)-1 for i in val.split(" ")[1:]])
            print("choiced:")
            print(game.choiced_dice)
            game.reroll(game.dice_max - len(game.choiced_dice))
            print("reroll:")
            print(game.dices)
            rr_limit -= 1
            
    game.check()
    print("----------------------------")
    num = 1
    for h in yachtGame.hands.items():
        print(f"{num} : {h}")
        num += 1
        
    print("Please decide hands(number) ▼")
    val = input()
    item = list(game.hands.items())[int(val)-1]
    game.score_board[item[0]] = f"{item[1]}"
    game.check_bonus()
    print("----------------------------")
    print("current score:")
    for s in yachtGame.score_board.items():
        print(s)
                
yachtGame = Yacht()
game_mode = 0
while len(yachtGame.score_board) < 13:
    if game_mode == 0:
        title()
        game_mode = 1
    if game_mode == 1:
        ingame(yachtGame)

print("----------------------------")
print("finish!")
print("score:")
for s in yachtGame.score_board.items():
    print(s)
