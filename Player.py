from enum import Enum
import random
import json
import re
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

    def setTurnCnt(self,num):
        self.turncnt = num

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

    def RemoveDeckBottom(self,num):
        self.Deck = self.Deck[:-num]

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

    def SendToSield(self, lst):
        self.ShieldZone += lst

    def SendToWatchingZone(self, lst):
        self.WatchingZone += lst

    def Draw(self, num):
        self.AddToZone(self.GetDeckTop(num), self.Hand)
        self.RemoveDeckTop(num)

    def ManaBoost(self, num):
        self.SendToMana(self.GetDeckTop(num))
        self.RemoveDeckTop(num)

    def DeckToSield(self, num):
        self.SendToSield(self.GetDeckTop(num))
        self.RemoveDeckTop(num)

    def ManaCharge(self, lis):
        self.SendToMana(lis)
        self.RemoveFromZone(lis, self.Hand)

    def RemoveFromZone(self,lis,zone):
        for card in lis:
            if card in zone: zone.remove(card)

    def AddToZone(self,lis,zone):
        zone += lis

    def SendCard(self, lis, fromz, toz):
        self.AddToZone(lis,toz)
        self.RemoveFromZone(lis, fromz)


    def ShieldToWathing(self, lis):
        #lisに入ってるnum番目の盾
        shields = []
        for i in lis:
            shield = self.ShieldZone[i]
            shields.append(shield)
        self.SendCard(shields, self.ShieldZone, self.WatchingZone)

    def UsingSTetc(self):
        print("-------------------------------------------")
        print(self.GetZoneInfo(self.WatchingZone))
        ipt = input("使うカードを選んでください.\n")
        while True:
            flg = False
            try : int_ipt = int(ipt)
            except : return
            else: 
                target = self.GetCardFromZone(int_ipt, self.WatchingZone)
                if target:
                    for text in target.Text:
                        if text.split("(")[0] == "Ｓ・トリガー": flg = True
                    if flg:
                        self.SendToBattleZone([target])
                        self.RemoveFromZone([target], self.WatchingZone)
                    else: print("そのカードは使えません.")
                else: print("そのカードは使えません.")

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
            if card in self.UntapMana:
                self.UntapMana.remove(card)

    def SelectUseMana(self,card):
        useMana = []
        while len(useMana) < card.Cost:
            mana = self.UntapMana
            for selected in useMana:
                if selected in mana: mana.remove(selected)
            print("-------------------------------------------")
            print("UntapMana:",self.GetZoneInfo(mana))
            print("Selected:",self.GetZoneInfo(useMana))
            ipt = input(f"使うマナを選択してください.command(left)残り{card.Cost - len(useMana)}枚\n")
            if ipt == "left":
                for i in range(card.Cost - len(useMana)):
                    useMana.append(mana[i])
            try: int_ipt = int(ipt)
            except : continue
            else:
                target = self.GetCardFromZone(int_ipt, self.UntapMana)
                if target:
                    useMana.append(target)
                else: continue
        return useMana

    def GetCardFromZone(self,num,zone):
        for card in zone:
            if card.cardID == num: return card
        return False

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
        print("Deck:", len(self.Deck),"枚")
        print("Hand:", len(self.Hand),"枚")
        if self.turnfase != TurnFase.NONE:
            print("     ", self.GetZoneInfo(self.Hand))
        print("Sield:", len(self.ShieldZone),"枚")
        mana = self.GetManaInfo()
        print("Mana:",len(self.UntapMana)+len(self.TapMana),"枚")
        print("     Untap:",mana[0])
        print("     Tap:",mana[1])
        print("Grave:", len(self.GraveZone),"枚")
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
                                for brkstr in text:
                                    if not brkstr: breaker = 1
                                    elif brkstr == "W・ブレイカー": breaker = 2
                                    elif brkstr == "T・ブレイカー": breaker = 3
                                    elif brkstr == "Q・ブレイカー": breaker = 4
                                    elif brkstr == "ワールド・ブレイカー": breaker = 5
                                    elif brkstr == "G・ブレイカー": breaker =  6
                                    elif brkstr == "パワード・ブレイカー": breaker = 7
                                    else: breaker = 1
                                card_obj = Card.CreatureCard(int(card_id), value["name"], civillist, cost, race, text, value["card1"]["power1"],breaker)
                        elif value["card1"]["type1"] == "呪文":
                            card_obj = Card.SpellCard(int(card_id), value["name"], civillist, cost, race, text)
                        self.Deck.append(card_obj)
