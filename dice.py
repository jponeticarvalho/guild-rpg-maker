import random

class diceRoll:
	def roll(self, amountDice, dice):
		result = 0;
		print ("[DiceRoll] Rolling " + str(amountDice) + "d" + str(dice))
		for i in range(0,amountDice):
			aux = random.randint(1, dice)
			print ("[DiceRoll] Dice N" + str(i) + " 1d" + str(dice) + ": " + str(aux))
			result = result + aux;

		print ("[DiceRoll] result = " + str(result))
		return result