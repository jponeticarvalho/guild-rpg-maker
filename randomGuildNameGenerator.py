import json

from dice import diceRoll


class nameGen:
    def genName(self):
        f1 = open('json4Names/randomGuildName.json')
        data1 = json.load(f1)

        dice = diceRoll()

        dice1 = dice.roll(1, 100)
        dice2 = dice.roll(1, 100)
        dice3 = dice.roll(1, 100)
        try:
            name = (
                str(data1[str(dice1)]['localidade'])
                + ' do/da '
                + str(data1[str(dice2)]['objeto'])
                + ' '
                + str(data1[str(dice3)]['qualidade'])
            )
        except Exception:
            print('ue')
        else:
            print('[NemGen] name= ' + name)
            f1.close()
            return name
