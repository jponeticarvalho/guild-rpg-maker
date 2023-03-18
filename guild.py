from common import D4
from common import D6
from common import D8
from common import D10
from common import D12
from common import D20
from common import D100
from common import random
from dice import diceRoll
from randomGuildNameGenerator import nameGen
import json
import time
import os

class GuildMaker:
	dice 						= diceRoll();
	exist 						= False;
	guildDiceBonus 				= 0;
	guildSize 					= 0;
	settlement 					= 0;
	resourceReputationModifier 	= 0;
	goersModifier				= 0;

	guildJson					= json.loads("{}");

	def createGuild(self, settlementSize, isHumanSettlement):

		f = open ("json4Names/guildSettlementSize.json")
		data = json.load(f)
		aux=0
		for i in data:
			if settlementSize == int(i):
				self.settlement = data[str(i)]
				aux = 1
		if aux == 0:
			return "error"
		f.close()


		self.guildJson	= json.loads("{}");
		nameG = nameGen()
		self.guildJson["name"] = nameG.genName()

		self.guildJson["settlementSize"] = self.settlement
		self.defExistGuild				(isHumanSettlement)
		self.defGuildSize				()
		self.defGuildCharacteristic		()
		self.defGuildReputation			()
		self.defGuildEmployees			()
		self.defGuildResources			()
		self.defGuildGoers				()

		#if self.guildJson["exist"] == False:
		#	return self.guildJson

		named_tuple = time.localtime() # get struct_time
		time_string = time.strftime("%m-%d-%Y-%H-%M-%S", named_tuple)
		guildNameStr = "guild" + time_string
		self.guildJson["fileName"] = guildNameStr

		try:
			os.mkdir("generatedGuild/")
		except:
			pass

		guildPath = "generatedGuild/" + guildNameStr + "/"
		try:
			os.mkdir(guildPath)
		except:
			print("[GuildMaker] ERROR when creating the folder returning without the guild")
			return "error"
		
		guildNameStr = guildPath + guildNameStr + ".json"
		with open(guildNameStr, "a+") as f:
			f.write (json.dumps(self.guildJson, indent=4))
			f.close()
		return self.guildJson

	def rollDice (self, diceData):
		diceResult = 0;
		print ("[GuildRollDice] Rolling " + str(diceData["diceAmount"]) + "d" + str(diceData["diceType"]) + "+" + str(diceData["diceBonus"]))
		diceResult = diceResult + self.dice.roll(diceData["diceAmount"], diceData["diceType"])
		diceResult = diceResult + diceData["diceBonus"] + self.guildDiceBonus 
		print ("[GuildRollDice] Dice Result = " + str(diceResult))

		return diceResult

	def rollCreationGuildDice (self):
		return self.rollDice (self.settlement["structureDice"])

	def defExistGuild(self, isHumanSettlement):
		f = open("json4Names/guildSettlementExist.json")
		data = json.load(f)
		print("[Exist?]")
		diceResult = self.rollCreationGuildDice();

		for i in data:
			if isHumanSettlement == data[str(i)]["isHuman"]:
				if diceResult in range(data[str(i)]["existRangeMin"], data[str(i)]["existRangeMax"]+1):
					self.exist = True
					if isHumanSettlement == True:
						if diceResult in range(data[str(i)]["matrixRangeMin"], data[str(i)]["matrixRangeMax"]+1):
							self.guildDiceBonus	= 5

		self.guildJson["exist"] = self.exist
		self.guildJson["guildDiceBonus"] = self.guildDiceBonus
		self.guildJson["rolledDice"] = diceResult
		self.guildJson["isHuman"] = isHumanSettlement

		f.close()

	def defGuildSize (self):
		if self.exist == False:
			return
		f = open("json4Names/guildSize.json")
		data = json.load(f)

		diceResult = self.rollCreationGuildDice();

		for i in data:
			if diceResult in range(data[str(i)]["diceRangeMin"], data[str(i)]["diceRangeMax"]+1):
				self.guildSize = i
				self.guildJson["size"] = data[str(i)]
				self.guildJson["size"]["rolledDice"] = diceResult
		
		f.close()
	
	def defGuildCharacteristic(self):
		if self.exist == False:
			return
		f = open("json4Names/guildCharacteristic.json")
		data = json.load(f)

		diceResult = self.rollCreationGuildDice();

		for i in data:
			if diceResult in range(data[str(i)]["diceRangeMin"], data[str(i)]["diceRangeMax"]+1):
				self.guildCharacteristic = data[str(i)]["name"]
				self.guildJson["Characteristic"] = data[str(i)]
				self.guildJson["Characteristic"]["rolledDice"] = diceResult

		f.close()

	def defGuildReputation (self):
		if self.exist == False:
			return
		f = open("json4Names/guildReputation.json")
		data = json.load(f)

		self.guildJson["reputation"] = json.loads("{}");

		for i in data:
			diceResult = self.rollCreationGuildDice();
			for j in data[i]:
				if diceResult in range(data[i][str(j)]["diceRangeMin"], data[i][str(j)]["diceRangeMax"]+1):
					self.resourceReputationModifier = self.resourceReputationModifier + data[i][str(j)]["resourceModifier"]
					self.guildJson["reputation"][i] = data[i][str(j)]
					self.guildJson["reputation"][i]["rolledDice"] = diceResult

		f.close()

	def defGuildEmployees (self):
		if self.exist == False:
			return
		f = open("json4Names/guildEmployees.json")
		data = json.load(f)

		diceResult = self.rollCreationGuildDice();
		if diceResult <= 0:
			diceResult = 1
		
		for i in data:
			if diceResult in range(data[str(i)]["diceRangeMin"], data[str(i)]["diceRangeMax"]+1):
				self.goersModifier = self.goersModifier + data[str(i)]["goersModifier"]
				self.guildJson["employees"] = data[str(i)]
				self.guildJson["employees"]["rolledDice"] = diceResult

		if self.guildJson["employees"]["amount"]["hasDice"]:
			diceResult = self.dice.roll(self.guildJson["employees"]["amount"]["diceAmount"], self.guildJson["employees"]["amount"]["diceType"]) + self.guildJson["employees"]["amount"]["diceBonus"]
			self.guildJson["employees"]["amount"]["value"] = diceResult
		
		f.close()

	def defGuildResources (self):
		if self.exist == False:
			return
		f = open("json4Names/guildResources.json")
		data = json.load(f)

		diceResult = self.rollCreationGuildDice();
		diceResult = diceResult + self.resourceReputationModifier
		if diceResult <= 0:
			diceResult = 1

		for i in data:
			if diceResult in range (data[str(i)]["diceRangeMin"], data[str(i)]["diceRangeMax"]+1):
				self.goersModifier = self.goersModifier + data[str(i)]["goersModifier"]
				self.guildJson["resource"] = data[str(i)]
				self.guildJson["resource"]["rolledDice"] = diceResult
		
		f.close()

	def defGuildGoers (self):
		if self.exist == False:
			return
		f = open("json4Names/guildGoers.json")
		data = json.load(f)

		#diceResult = self.dice.roll(self.settlement["goersDiceAmount"], self.settlement["goersDiceType"]) +  self.settlement["goersDiceBonus"];
		diceResult = self.rollDice(self.settlement["goersDice"])
		diceResult = diceResult + self.goersModifier
		if diceResult <= 0:
			diceResult = 1
		
		for i in data:
			if diceResult in range (data[str(i)]["diceRangeMin"], data[str(i)]["diceRangeMax"]+1):
				self.guildJson["goers"] = data[str(i)]
				self.guildJson["goers"]["rolledDice"] = diceResult
		
		f.close()
		