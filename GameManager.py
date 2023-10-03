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

def TurnStart():
    turnPlayer.turnfase = Player.TurnFase.START
    turnPlayer.UntapMana += turnPlayer.TapMana
    turnPlayer.TapMana = []
    for card in turnPlayer.BattleZone:
        card.Attackable = True
    turnPlayer.ShowInfo()
    if turnPlayer.turncnt > 1:
        turnPlayer.Draw(1)

def TurnCharge():
    turnPlayer.turnfase = Player.TurnFase.CHARGE
    turnPlayer.ShowInfo()
    while True:
        ipt = input("チャージするものを選んでください.チャージしない場合はEnterしてください.")
        try:
            int_ipt = int(ipt)
        except:
                break
        else:
            target = turnPlayer.GetCardFromZone(int_ipt, turnPlayer.Hand)
            if target:
                turnPlayer.ManaCharge(target)
                return
            else: print("チャージできません")

def TurnUse():
    turnPlayer.turnfase = Player.TurnFase.USE
    turnPlayer.ShowInfo()
    while True:
        ipt = input("使うカードを選んでください.使わない場合Enterしてください.")
        try: int_ipt = int(ipt)
        except: break
        else:
            target = turnPlayer.GetCardFromZone(int_ipt, turnPlayer.Hand)
            if target:
                if target.Cost > len(turnPlayer.UntapMana):
                    print("カードが使えません")
                    continue
                mana = turnPlayer.SelectUseMana(target)
                if  not mana:
                    print("カードが使えません")
                    continue
                if turnPlayer.CheckCivil(target, mana):
                    turnPlayer.SendToBattleZone([target])
                    turnPlayer.Hand.remove(target)
                    turnPlayer.ManaTap(mana)
                    turnPlayer.ShowInfo()
                else: print("カードが使えません")
            else: print("カードが使えません")

def TurnAttack():
    turnPlayer.turnfase = Player.TurnFase.ATTACK
    if turnPlayer.BattleZone == []: return
    turnPlayer.ShowInfo()
    while True:
        ipt = input("アタックするカードを選んでください.アタックしない場合Enterしてください.")
        try: int_ipt = int(ipt)
        except: return
        else:
            target = turnPlayer.GetCardFromZone(int_ipt, turnPlayer.BattleZone)
            if target:
                if target.Attackable:
                    while True:
                        ipt = input("アタック対象を選んでください.Player or 数字")
                        if ipt == "Player":
                            print(f"{target.Breaker}枚ブレイク")
                            target.Attackable = False
                            turnPlayer.ShowInfo()
                            break
                        else:
                            try: int_ipt = int(ipt)
                            except: break
                            else: print(f"{int_ipt}にアタック")
                            target.Attackable = False
                            turnPlayer.ShowInfo()
                            break
                            turnPlayer.ShowInfo()
                else: print("アタックできません")
            else: print("アタックできません")

def TurnEnd():
    turnPlayer.turnfase = Player.TurnFase.END
    turnPlayer.ShowInfo()
    turnPlayer.turnfase = Player.TurnFase.NONE

def TurnCalc():
    global turncnt, isPlayerTurn, turnPlayer
    if isPlayerTurn:
        turnPlayer = player
    else:
        turnPlayer = enemy
    turncnt += 0.5
    turnPlayer.setTurnCnt(turncnt)
    TurnStart()
    TurnCharge()
    TurnUse()
    TurnAttack()
    TurnEnd()

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