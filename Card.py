from enum import Enum
import json

class CivilizationType(Enum):
    FIRE = 1
    WATER = 2
    LIGHT = 3
    DARKNESS = 4
    NATURE = 5

class CardType(Enum):
    NULL = 0
    CREATURE = 1
    SPELL = 2
    EVOLUTION_CREATURE = 3
    MUGETU_FIELD = 4

class RaceType(Enum):
    NULL = 0
    DORAGONOIDO = 1
    BI_TOJOKKI = 2
    REKUSUTAZU = 3
    SUPERUYARUZU = 4
    DEMONIO = 5
    ONIHUDAOUKOKU = 6
    DESUPAPETTO = 7
    EIRIANN = 8
    AUTOREIJI = 9
    TI_MUBONNBA = 10
    REDDO_0_KOMANNDO_0_DORAGONN = 11
    DORUSUZAKU = 12
    MAFI_0_GYANGU = 13
    DE_MONN_0_KOMANDDO = 14
    ZENISU = 15
    MADOUGU = 16

class Card:
    def __init__(self, cardID, Name, Civilization, Cost, Race, Text):
        self.cardID = cardID
        self.Name = Name
        self.Type: CardType()
        self.Civilization = Civilization
        self.Cost = Cost
        self.Race = Race
        self.Text = Text

class CreatureCard(Card):
    def __init__(self, cardID, Name, Civilization, Cost, Race, Text, Power, Breaker):
        super().__init__(cardID, Name, Civilization, Cost, Race, Text)
        self.Power = Power
        self.Breaker = Breaker
        self.Attackable = False
        self.Blockable = True
        self.Selectable = True
        self.Type = CardType.CREATURE

class SpellCard(Card):
    def __init(self, cardID, Name, Civilization, Cost, Race, Text, SpellType):
        super().__init(cardID, Name, Civilization, Cost, Race, Text)
        self.Type = CardType.SPELL

class EvolutionCreatureCard(CreatureCard):
    def __init(self, cardID, Name, Civilization, Cost, Race, Text, BaseCreature, Level):
        super().__init(cardID, Name,  Civilization, Cost, Race, Text)
        self.Type = CardType.EVOLUTION_CREATURE
        self.BaseCreature = BaseCreature
        self.Level = Level
