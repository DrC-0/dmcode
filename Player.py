from enum import Enum
import random
import json
import Card

class TurnFase(Enum):
    NONE = 0
    START = 1
    CHARGE = 2
    USE = 3
    ATTACK = 4
    END = 5

class Player:
    def __init__(self,name):
        self.name = name
        self.Deck = []
        self.Hand = []
        self.TapMana = []
        self.UntapMana = []
        self.BattleZone = []
        self.GraveZone = []
        self.ShieldZone = []
        self.WatchingZone = []
        self.turnfase = TurnFase.NONE
        self.win = False
        self.turncnt = 0
        #self.deck = deck
    
    def setTurnCnt(self,num):
        self.turncnt = num

    def MakeDeck(self,deckname):
        with open(deck) as f:
            deck_data = json.load(f)
        with open("use_cardlist.json") as f:
            dic_data = json.load(f)
        for value in deck_data().values():
            name = value["name"]
            for data in dic_data:
                print()

    def Shuffle(self, lst):
        random.shuffle(lst)
        return lst

    def SendToDeckBottom(self, lst):
        self.Deck += lst

    def SendToDeckTop(self, lst):
        self.Deck = lst + self.Deck

    def GetDeckTop(self, num):
        return self.Deck[:num]

    def RemoveDeckTop(self, num):
        self.Deck = self.Deck[num:]

    def SendToHand(self, lst):
        self.Hand += lst

    def SendToMana(self, lst):
        for card in lst:
            if len(card.Civilization) == 1:
                self.UntapMana.append(card)
            else: self.TapMana.append(card)

    def SendToBattleZone(self, lst):
        for card in lst:
            if isinstance(card, Card.CreatureCard):
                self.BattleZone.append(card)
            elif isinstance(card, Card.SpellCard):
                print("呪文効果発動")
                self.GraveZone.append(card)
            else:
                self.BattleZone.append(card)

    def SendToGrave(self, lst):
        self.GraveZone += lst

    def SendToSield(self, lst):
        self.ShieldZone += lst

    def SendToWatchingZone(self, lst):
        self.WatchingZone += lst

    def Draw(self, num):
        self.SendToHand(self.GetDeckTop(num))
        self.RemoveDeckTop(num)

    def DeckToMana(self, num):
        self.SendToMana(self.GetDeckTop(num))
        self.RemoveDeckTop(num)

    def DeckToGrave(self, num):
        self.SendToGrave(self.GetDeckTop(num))
        self.RemoveDeckTop(num)

    def DeckToSield(self, num):
        self.SendToSield(self.GetDeckTop(num))
        self.RemoveDeckTop(num)

    def DeckToWatching(self, num):
        self.SendToWatchingZone(self.GetDeckTop(num))
        self.RemoveDeckTop(num)

    def ManaCharge(self, card):
        self.SendToMana([card])
        self.Hand.remove(card)

    def ShieldToWathing(self, num):
        #num番目の盾
        shild = self.ShieldZone[num]
        self.SendToWatchingZone([shild])
        self.ShieldZone.remove(shield)

    def BreakShield(self,lst):
        for i in lst:
            self.ShieldToWathing(i)

    def GetManaInfo(self):
        umanalis = {}
        tmanalis = {}
        for card in self.UntapMana:
            civstr = ",".join(civ for civ in card.Civilization)
            if civstr not in umanalis:
                umanalis[civstr] = 0
            umanalis[civstr] += 1
        for card in self.TapMana:
            civstr = ",".join(civ for civ in card.Civilization)
            if civstr not in tmanalis:
                tmanalis[civstr] = 0
            tmanalis[civstr] += 1
        return [umanalis,tmanalis]

    def ManaTap(self,lis):
        self.TapMana += lis
        for card in lis:
            self.UntapMana.remove(card)
    
    def SelectUseMana(self,card):
        useMana = []
        while len(useMana) < card.Cost:
            mana = self.UntapMana
            for selected in useMana:
                if selected in mana: mana.remove(selected)
            print("-------------------------------------------")
            print(self.GetZoneInfo(mana))
            print("Selected:",self.GetZoneInfo(useMana))
            ipt = input(f"使うマナを選択してください.残り{card.Cost - len(useMana)}枚")
            try: int_ipt = int(ipt)
            except : break
            else: 
                useMana.append(self.GetCardFromZone(int_ipt, self.UntapMana))
        return useMana
    
    def GetCardFromZone(self,num,zone):
        for card in zone:
            if card.cardID == num: return card

    def GetZoneInfo(self,zone):
        return ",".join(str(card.cardID)+":"+card.Name for card in zone)
    
    def CheckCivil(self,card,lis):
        civils = []
        for mana in lis:
            for civ in mana.Civilization:
                if civ not in civils: civils.append(civ)
        return card.Civilization <= civils

    def ShowInfo(self):
        print("-------------------------------------------")
        print("name:" + self.name)
        if (self.turncnt * 2)%2 == 0:
            print(f"先攻{int(self.turncnt)}ターン目")
        else:
            print(f"後攻{int(self.turncnt)}ターン目")
        print(self.turnfase)
        print("Deck:", len(self.Deck))
        if self.turnfase == TurnFase.NONE:
            print("Hand:", len(self.Hand))
        else:
            print("Hand:", self.GetZoneInfo(self.Hand))
        print("Sield:", len(self.ShieldZone))
        mana = self.GetManaInfo()
        print("Mana:")
        print("     Untap:",mana[0])
        print("     Tap:",mana[1])
        print("Grave:", self.GetZoneInfo(self.GraveZone))
        print("BattleZone:", self.GetZoneInfo(self.BattleZone))

    def GameReady(self,deckstr):
        self.Hand = []
        self.TapMana = []
        self.UntapMana = []
        self.BattleZone = []
        self.GraveZone = []
        self.ShieldZone = []
        self.WatchingZone = []
        self.turnfase = TurnFase.NONE
        self.win = False
        #self.TestDeckGene()
        self.makedecklist(deckstr=deckstr)
        self.Deck = self.Shuffle(self.Deck)
        self.DeckToSield(5)
        self.Draw(5)
        self.turncnt = 0

    def TurnStart(self):
        self.turnfase = TurnFase.START
        self.UntapMana += self.TapMana
        self.TapMana = []
        for card in self.BattleZone:
            card.Attackable = True
        self.ShowInfo()
        if self.turncnt > 1:
            self.Draw(1)

    def TurnCharge(self):
        self.turnfase = TurnFase.CHARGE
        self.ShowInfo()
        while True:
            ipt = input("チャージするものを選んでください.チャージしない場合は0を入力してください.")
            try:
                int_ipt = int(ipt)
            except:
                    break
            else:
                if int_ipt == 0: return
                self.ManaCharge(self.GetCardFromZone(int_ipt, self.Hand))
                return

    def TurnUse(self):
        self.turnfase = TurnFase.USE
        self.ShowInfo()
        while True:
            ipt = input("使うカードを選んでください.使わない場合Enterしてください.")
            try: int_ipt = int(ipt)
            except: break
            else:
                target = self.GetCardFromZone(int_ipt, self.Hand)
                if target.Cost > len(self.UntapMana): 
                    print("カードが使えません")
                    continue
                mana = self.SelectUseMana(target)
                if self.CheckCivil(target, mana): 
                    self.SendToBattleZone([target])
                    self.Hand.remove(target)
                    self.ManaTap(mana)
                    self.ShowInfo()
                else: print("カードが使えません")
                

    def TurnAttack(self):
        self.turnfase = TurnFase.ATTACK
        if self.BattleZone == []: return
        self.ShowInfo()
        while True:
            ipt = input("アタックするカードを選んでください.アタックしない場合Enterしてください.")
            try: int_ipt = int(ipt)
            except: break
            else:
                target = self.GetCardFromZone(int_ipt, self.BattleZone)
                if target.Attackable:
                    while True:
                        ipt = input("アタック対象を選んでください.Player or 数字")
                        if ipt == "Player":
                            print(f"{target.Breaker}枚ブレイク")
                        else: 
                            try: int_ipt = int(ipt)
                            except: break
                            else: print(f"{int_ipt}にアタック")
                self.ShowInfo()

    def TurnEnd(self):
        self.turnfase = TurnFase.END
        self.ShowInfo()
        self.turnfase = TurnFase.NONE

    def makedecklist(self,deckstr):
        with open("use_cardlist.json") as f:
            json_data = json.load(f)
        with open(deckstr) as f:
            deck_j = json.load(f)

        for card in deck_j.values():
            for _ in range(card["num"]):
                for card_id, value in json_data.items():
                    if value["name"] == card["name"]:
                        civillist = []
                        for civil in value["civil"]:
                            if civil == "火":
                                civillist.append(Card.CivilizationType.FIRE.name)
                            if civil == "水":
                                civillist.append(Card.CivilizationType.WATER.name)
                            if civil == "自然":
                                civillist.append(Card.CivilizationType.NATURE.name)
                            if civil == "光":
                                civillist.append(Card.CivilizationType.LIGHT.name)
                            if civil == "闇":
                                civillist.append(Card.CivilizationType.DARKNESS.name)

                        cost = int(value["card1"]["cost1"])
                        race = value["card1"]["race1"]
                        text = value["card1"]["ability1"]
                        if value["card1"]["type1"] == "クリーチャー":
                            if "card2 " in value:
                                if value["card2"]["type2"] == "呪文": pass
                            else : 
                                card_obj = Card.CreatureCard(int(card_id), value["name"], civillist, cost, race, text)
                        elif value["card1"]["type1"] == "呪文":
                            card_obj = Card.SpellCard(int(card_id), value["name"], civillist, cost, race, text)
                        self.Deck.append(card_obj)
