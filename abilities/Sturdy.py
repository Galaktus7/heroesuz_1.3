import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../db.py
import special_abilities


class Sturdy(special_abilities.Ability):
    name ="Ikki Hayotlik"
    info = 'Maksimum jonni 1 taga ko`paytiradi. Qon yo`qotishga chidamlilik ortadi.'
    RangeOnly = False
    MeleeOnly = False
    TeamOnly = False
    def aquare(self, user):
        user.maxhp += 1
        user.hp += 1

special_abilities.abilities.append(Sturdy)
