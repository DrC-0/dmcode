from enum import Enum
import Player
from Battledeckmaker import makelist
import random

turncnt = 0.5
isPlayerTurn = False
win_flg = False
player = Player.Player("player")
enemy = Player.Player("enemy")
turnPlayer = None
dic_name = 'card_info_dic2.1.json'
deck1_name = 'Akatan.json'
deck2_name = 'Aoma.json'
file_name = "use_cardlist"

def GameStart():
    player.GameReady(deck1_name)
    enemy.GameReady(deck2_name)
    isPlayerTurn = bool(random.getrandbits(1))

def TurnCalc():
    global turncnt, isPlayerTurn, turnPlayer
    if isPlayerTurn:
        turnPlayer = player
    else:
        turnPlayer = enemy
    turncnt += 0.5
    turnPlayer.setTurnCnt(turncnt)
    turnPlayer.TurnStart()
    turnPlayer.TurnCharge()
    turnPlayer.TurnUse()
    turnPlayer.TurnAttack()
    turnPlayer.TurnEnd()

def ChangeTurn():
    global isPlayerTurn
    isPlayerTurn = not isPlayerTurn
    TurnCalc()
    if(player.win or enemy.win):
        global win_flg
        win_flg = True

def main():
    makelist(dic_name,deck1_name,deck2_name,file_name)
    GameStart()
    TurnCalc()
    while(win_flg == False):
        ChangeTurn()
    
if __name__ == "__main__":    
    main()