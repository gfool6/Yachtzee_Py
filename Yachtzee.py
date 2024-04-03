import random
from collections import Counter

class Yacht:
    def __init__(self):
        self.dices = []
        self.choiced_dice = []
        self.rolled = []
        self.dice_max = 5
        self.keys = "1/2/3/4/5/6/Choice/Four of a kind/Full house/S Straight/L Straight/Yacht".split("/")
        self.hands = {key:0 for key in self.keys}
        self.score_board = {key:"-" for key in self.keys+["Bonus"]}

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
        self.hands = {key:0 for key in self.keys}
        
        # 1〜6
        for i in range(6):
            diceNum = i + 1
            self.hands[f"{diceNum}"] = sum([j for j in self.dices if j == diceNum])
        
        # choice
        self.hands["Choice"] = sum(self.dices)
        
        # four of a kind
        if(max(sorted(Counter(self.dices).values()))>= 4):
            self.hands["Four of a kind"] = sum(self.dices)
        
        # full house
        if(sorted(Counter(self.dices).values()) == [2, 3]):
            self.hands["Full house"] = sum(self.dices)
        
        # S straight / L straight
        joined = "".join(map(str, list(set(self.dices))))
        is_LS = any(ls in joined for ls in ["12345","23456"])
        is_SS = is_LS or any(ss in joined for ss in ["1234","2345","3456"])
        if is_LS:
            self.hands["L Straight"] = 30
        if is_SS:
            self.hands["S Straight"] = 15
            
        # Yacht
        if any(self.dices.count(i+1) == 5 for i in reversed(range(6))):
            self.hands["Yacht"] = 50
    
    def score_decide(self, index):
        item = list(self.hands.items())[index]
        self.score_board[item[0]] = f"{item[1]}"
                
    def check_bonus(self):
        if self.score_board["Bonus"] != "-":
            return
        
        sum = 0
        for k in [f"{i+1}" for i in range(6)]:
            if self.score_board[k] == "-":
                continue
            else:
                sum += int(self.score_board[k])
        
        if sum >= 63:
            self.score_board["Bonus"] = "35"
            
        if self.score_board["Bonus"] == "-" and list(self.score_board.values()).count("-") == 1:
            self.score_board["Bonus"] = "0"
            
    def print_score(self):
        for s in self.score_board.items():
            print(s)
            
                        
def title():
    print("input command ▼")
    print("s: start game ▼ \ne: end game ▼")
    title_input = input()
    if title_input == "e":
        exit()
    if title_input == "s":
        print("start!")

def ingame(game: Yacht):
    print("\n----------------------------")
    input("press Enter to Roll ▼")
    game.roll()
    print(game.dices)
    rr_limit = 3
    while rr_limit > 0:
        print("\n----------------------------")
        print("reroll, choice or decide ▼")
        print("input 'd' and Enter. dices decide ▼")
        print("input 'c {num} {num} ....' and Enter. dices choiced and reroll ▼")
        print("input 'r' and Enter. dices not choiced and reroll ▼")
        val = input()
        print("\n----------------------------")
        if val == "r":
            game.reroll(game.dice_max)
            print("reroll:")
            print(game.dices)
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
    print("\n----------------------------")
    num = 1
    for h in game.hands.items():
        if game.score_board[h[0]] == "-":
            print(f"{num} : {h}")
        else:
            print(f"{num} : decided")
        num += 1
        
    print("Please decide hands(number) ▼")
    val = input()
    game.score_decide(int(val)-1)
    game.check_bonus()
    print("\n----------------------------")
    print("current score:")
    game.print_score()
    

yachtGame = Yacht()
game_mode = 0
while "-" in yachtGame.score_board.values():
    if game_mode == 0:
        title()
        game_mode = 1
    if game_mode == 1:
        ingame(yachtGame)
print("\n----------------------------")
print("total score:")
yachtGame.print_score()
print(f'\ntotal points: {sum([int(a) for a in yachtGame.score_board.values() if a != "-"])} / 323')
