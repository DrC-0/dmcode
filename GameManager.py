from enum import Enum
import Player
from Battledeckmaker import makelist
import random

turncnt = 0.5
win_flg = False
player = Player.Player("player")
enemy = Player.Player("enemy")
TurnPlayer = None
notTurnPlayer = None
dic_name = 'card_info_dic2.1.json'
deck1_name = 'Akatan.json'
deck2_name = 'Aoma.json'
file_name = "use_cardlist"

def GameReady():
    global TurnPlayer, notTurnPlayer
    player.GameReady(deck1_name)
    enemy.GameReady(deck2_name)
    TurnPlayer = player
    notTurnPlayer = enemy
    if bool(random.getrandbits(1)):
        PlayerChange()

def PlayerChange():
    global TurnPlayer, notTurnPlayer
    x = TurnPlayer
    TurnPlayer = notTurnPlayer
    notTurnPlayer = x

def TurnStart():
    TurnPlayer.turnfase = Player.TurnFase.START
    TurnPlayer.UntapMana += TurnPlayer.TapMana
    TurnPlayer.TapMana = []
    for card in TurnPlayer.BattleZone:
        card.Attackable = True
    TurnPlayer.ShowInfo()
    if TurnPlayer.turncnt > 1:
        TurnPlayer.Draw(1)

def TurnCharge():
    TurnPlayer.turnfase = Player.TurnFase.CHARGE
    TurnPlayer.ShowInfo()
    while True:
        ipt = input("チャージするものを選んでください.チャージしない場合はEnterしてください.\n")
        try:
            int_ipt = int(ipt)
        except:
                break
        else:
            target = TurnPlayer.GetCardFromZone(int_ipt, TurnPlayer.Hand)
            if target:
                TurnPlayer.ManaCharge([target])
                return
            else: print("チャージできません")

def TurnUse():
    TurnPlayer.turnfase = Player.TurnFase.USE
    TurnPlayer.ShowInfo()
    while True:
        ipt = input("使うカードを選んでください.使わない場合Enterしてください.\n")
        try: int_ipt = int(ipt)
        except: break
        else:
            target = TurnPlayer.GetCardFromZone(int_ipt, TurnPlayer.Hand)
            if target:
                if target.Cost > len(TurnPlayer.UntapMana):
                    print("カードが使えません")
                    continue
                mana = TurnPlayer.SelectUseMana(target)
                if  not mana:
                    print("カードが使えません")
                    continue
                if TurnPlayer.CheckCivil(target, mana):
                    TurnPlayer.SendToBattleZone([target])
                    TurnPlayer.Hand.remove(target)
                    TurnPlayer.ManaTap(mana)
                    TurnPlayer.ShowInfo()
                else: print("カードが使えません")
            else: print("カードが使えません")

def TurnAttack():
    TurnPlayer.turnfase = Player.TurnFase.ATTACK
    if TurnPlayer.BattleZone == []: return
    TurnPlayer.ShowInfo()
    while True:
        ipt = input("アタックするカードを選んでください.アタックしない場合Enterしてください.\n")
        try: int_ipt = int(ipt)
        except: return
        else:
            target = TurnPlayer.GetCardFromZone(int_ipt, TurnPlayer.BattleZone)
            if target:
                if target.Attackable:
                    while True:
                        notTurnPlayer.ShowInfo()
                        ipt = input("アタック対象を選んでください.Player or 数字\n")
                        if ipt == "Player":
                            if len(notTurnPlayer.ShieldZone) < 1:print("win")
                            else:
                                print(f"{target.Breaker}枚ブレイク")
                                BreakShield(notTurnPlayer, target.Breaker)
                        else:
                            try: int_ipt = int(ipt)
                            except: break
                            else: 
                                atked = notTurnPlayer.GetCardFromZone(int_ipt, notTurnPlayer.BattleZone)
                                if atked:
                                    print(f"{int_ipt}にアタック")
                                    Battle(target, TurnPlayer, atked, notTurnPlayer)
                        target.Attackable = False
                        del TurnPlayer.BattleZone[:1]
                        TurnPlayer.BattleZone.append(target)
                        TurnPlayer.ShowInfo()
                        break
                else: print("アタックできません")
            else: print("アタックできません")

def TurnEnd():
    TurnPlayer.turnfase = Player.TurnFase.END
    TurnPlayer.ShowInfo()
    TurnPlayer.turnfase = Player.TurnFase.NONE

def Battle(atker,owner1, atkeder, owner2):
    if atker.Power > atkeder.Power:
        owner2.SendCard([atkeder],owner2.BattleZone,owner2.BattleZone)
    elif atker.Power == atkeder.Power:
        owner2.SendCard([atkeder],owner2.BattleZone,owner2.BattleZone)
        owner1.SendCard([atker],owner1.BattleZone,owner1.BattleZone)
    else:
        owner1.SendCard([atker],owner1.BattleZone,owner1.BattleZone)

def BreakShield(player, num):
    shieldnum = len(player.ShieldZone)
    breaklist = []
    max_break = num
    if shieldnum < num: max_break = shieldnum
    while len(breaklist) < max_break:
        ipt = input(f"ブレイクするシールドを選択してください.0~{shieldnum - 1}\n")
        try : int_ipt = int(ipt)
        except :continue
        else: 
            if int_ipt < shieldnum and int_ipt not in breaklist : breaklist.append(int_ipt)
            else: print("そのシールドは選べません")
    player.ShieldToWathing(breaklist)
    player.UsingSTetc()

def TurnCalc():
    global turncnt,TurnPlayer
    turncnt += 0.5
    TurnPlayer.setTurnCnt(turncnt)
    TurnStart()
    TurnCharge()
    TurnUse()
    TurnAttack()
    TurnEnd()

def ChangeTurn():
    PlayerChange()
    TurnCalc()
    if(player.win or enemy.win):
        global win_flg
        win_flg = True

def main():
    #makelist(dic_name,deck1_name,deck2_name,file_name)
    GameReady()
    while(win_flg == False):
        ChangeTurn()

if __name__ == "__main__":
    main()