from common import D4
from common import D6
from common import D8
from common import D10
from common import D12
from common import D20
from common import D100
from common import random
from dice import diceRoll
from guild import GuildMaker
import json
import os

class ContractMaker:

	dice = diceRoll()
	contratJson = json.loads("{}")

	_MAX_NUMBER_OF_CLAUSES 				= 10
	_MAX_NUMBER_OF_PRE_REQUIREMENTS 	= 10
	_MAX_NUMBER_OF_OBJECTIVES			= 10
	_MAX_NUMBER_OF_DISTRICTS			= 10
	_MAX_NUMBER_OF_ANTAGONISTS			= 10

	def creatContract(self, guildJson):
		self.guildJson = guildJson

		self.contratJson["guild"] = guildJson #guildJson["name"]

		self.defDueDate			()
		self.defDifficulty		()
		self.defDistance		()
		self.defValeuReward		()
		self.defPreRequirements	()
		self.defClause			()
		self.updateReward		()
		self.defContractor		()
		self.defContractType	()
		self.defObjective		()
		self.defLocation		()
		self.defAntagonist		()
		self.defComplication	()
		self.defAllies			()

		contractPath = "generatedGuild/" + self.guildJson["fileName"] + "/contracts/"
		try:
			os.mkdir(contractPath)
		except:
			print("[ContractMaker] ERROR when creating the folder to the contract returning without the guild")
			#return "error"

		contractNumber = len(os.listdir(contractPath))
		self.contratJson["fileName"] = "contract-" + str(contractNumber) + ".json"
		contractPath = contractPath + "contract-" + str(contractNumber) + ".json"

		with open(contractPath, "w+") as f:
			f.write (json.dumps(self.contratJson, indent=4))
			f.close()

		return self.contratJson
	
	def rollDice (self, diceData):
		diceResult = 0
		print ("[ContractRollDice] Rolling " + str(diceData["diceAmount"]) + "d" + str(diceData["diceType"]) + "+" + str(diceData["diceBonus"]))
		diceResult += self.dice.roll(diceData["diceAmount"], diceData["diceType"])
		diceResult += diceData["diceBonus"] # sede matriz influencia aqui?
		print ("[ContractRollDice] Dice Result = " + str(diceResult))

		return diceResult

	def defDueDate(self):
		f = open("json4Names/ContractServiceValueReward/dueDate.json")
		data = json.load(f)

		diceResult = self.dice.roll(1, 20)

		for i in data:
			if diceResult in range(data[str(i)]["diceRangeMin"], data[str(i)]["diceRangeMax"]+1):
				self.contratJson["dueDate"] = data[str(i)]
				self.contratJson["dueDate"]["rolledDice"] = diceResult
		
		diceResult = 0
		diceResult = self.rollDice(self.contratJson["dueDate"]["amount"]["dueDateDice"])
		diceResult *= int(self.contratJson["dueDate"]["amount"]["diceMultiplier"])

		self.contratJson["dueDate"]["amount"]["value"] += diceResult

		f.close()
		pass
	
	def defDifficulty(self):
		f = open("json4Names/ContractServiceValueReward/contractDifficulty.json")
		data = json.load(f)

		self.contratJson["difficulty"] = self.rollTable(data["difficulty"], data["difficultyDice"])

		f.close()
		pass


	def defDistance(self):
		f = open("json4Names/ContractServiceValueReward/contractDistance.json")
		data = json.load(f)

		self.contratJson["distance"] = self.rollTable(data["distance"], data["distanceDice"])

		f.close()
		pass

	def defValeuReward(self):
		f = open("json4Names/ContractServiceValueReward/valueReward.json")
		data = json.load(f)

		diceResult = self.dice.roll(1,100)
		diceResultValue 	= diceResult
		diceResultReward 	= diceResult

		#modificadores do resultado do dado

		#area proxima deve influencia no contrato mas nao sei como fazer aqui

		diceResultValue		+= self.contratJson["distance"]["valueRewardModifier"]
		diceResultReward 	+= self.contratJson["distance"]["valueRewardModifier"]
		
		diceResultValue		+= self.guildJson["reputation"]["govern"]["rewardModifier"]["valeuMod"]
		diceResultReward	+= self.guildJson["reputation"]["govern"]["rewardModifier"]["rewardMod"]

		diceResultValue		+= self.guildJson["reputation"]["population"]["rewardModifier"]["valeuMod"]
		diceResultReward	+= self.guildJson["reputation"]["population"]["rewardModifier"]["rewardMod"]

		diceResultValue		+= self.guildJson["employees"]["rewardModifier"]["valeuMod"]
		diceResultReward 	+= self.guildJson["employees"]["rewardModifier"]["rewardMod"]

		if diceResultReward > 100:
			diceResultReward = 100
		elif diceResultReward < 1:
			diceResultReward = 1

		if diceResultValue > 100:
			diceResultValue = 100
		elif diceResultValue < 1:
			diceResultValue = 1

		for i in data:
			if diceResultReward in range(data[str(i)]["diceRangeMin"], data[str(i)]["diceRangeMax"]+1):
				self.contratJson["reward"] = data[str(i)]
				self.contratJson["reward"]["rolledDice"] = diceResultReward
			if diceResultValue in range(data[str(i)]["diceRangeMin"], data[str(i)]["diceRangeMax"]+1):
				self.contratJson["value"] = data[str(i)]
				self.contratJson["value"]["rolledDice"] = diceResultValue

		f.close()
		pass
	
	def defPreRequirements(self):
		f = open("json4Names/ContractServiceValueReward/preRequirementsClause.json")
		data = json.load(f)

		for i in data["diceDefinition"]:
			if self.contratJson["value"]["rolledDice"] in range(data["diceDefinition"][str(i)]["diceRangeMin"], data["diceDefinition"][str(i)]["diceRangeMax"]+1):
				self.contratJson["preRequirementClauseDice"] = data["diceDefinition"][str(i)]

		preRequimentAmount = 1
		preRequimentNumber = 1

		self.contratJson["preRequirement"] = json.loads("{}")

		while preRequimentAmount > 0:
			diceResult = self.rollDice(self.contratJson["preRequirementClauseDice"]["dice"])
			if diceResult < 1:
				diceResult = 1

			for i in data["preRequirements"]:
				if diceResult in range(data["preRequirements"][str(i)]["diceRangeMin"], data["preRequirements"][str(i)]["diceRangeMax"]+1):
					self.contratJson["preRequirement"][str(preRequimentNumber)] = data["preRequirements"][str(i)]
					self.contratJson["preRequirement"][str(preRequimentNumber)]["valueUsed"] = self.contratJson["value"]["rolledDice"]
					self.contratJson["preRequirement"][str(preRequimentNumber)]["rolledDice"] = diceResult
			
			preRequimentAmount -= 1
			preRequimentNumber += 1
			

			#TODO verificar um jeito que nao fique tao hardcoded
			if diceResult in range(data["preRequirements"]["21+"]["diceRangeMin"], data["preRequirements"]["21+"]["diceRangeMax"]+1):
				preRequimentAmount += 2

			if preRequimentNumber > self._MAX_NUMBER_OF_PRE_REQUIREMENTS:
				break

		self.contratJson["preRequirement"]["amount"] = preRequimentNumber - 1

		f.close()
		pass

	def defClause(self):
		f = open("json4Names/ContractServiceValueReward/preRequirementsClause.json")
		data = json.load(f)

		for i in data["diceDefinition"]:
			if self.contratJson["value"]["rolledDice"] in range(data["diceDefinition"][str(i)]["diceRangeMin"], data["diceDefinition"][str(i)]["diceRangeMax"]+1):
				self.contratJson["preRequirementClauseDice"] = data["diceDefinition"][str(i)]

		clauseAmount = 1
		clauseNumber = 1

		self.contratJson["clause"] = json.loads("{}")

		self.contratJson["clause"]["rolledDice"] = json.loads("{}")
		while clauseAmount > 0:
			diceResult = self.rollDice(self.contratJson["preRequirementClauseDice"]["dice"])
			if diceResult < 1:
				diceResult = 1
			for i in data["clause"]:
				if diceResult in range(data["clause"][str(i)]["diceRangeMin"], data["clause"][str(i)]["diceRangeMax"]+1):
					self.contratJson["clause"][str(clauseNumber)] = data["clause"][str(i)]
					self.contratJson["clause"][str(clauseNumber)]["valueUsed"] = self.contratJson["value"]["rolledDice"]
					self.contratJson["clause"][str(clauseNumber)]["rolledDice"] = diceResult
			self.contratJson["clause"]["rolledDice"][str(clauseNumber)] = diceResult
			clauseAmount -= 1
			clauseNumber += 1

			#TODO verificar um jeito que nao fique tao hardcoded
			if diceResult in range(data["clause"]["21+"]["diceRangeMin"], data["clause"]["21+"]["diceRangeMax"]+1):
				clauseAmount += 2

			if clauseNumber > self._MAX_NUMBER_OF_CLAUSES:
				break

		self.contratJson["clause"]["amount"] = clauseNumber - 1

		f.close()
		pass

	def updateReward(self):

		f = open("json4Names/ContractServiceValueReward/valueReward.json")
		data = json.load(f)

		diceResultReward 	= self.contratJson["reward"]["rolledDice"] 

		points = 0

		for i in range (1, self.contratJson["clause"]["amount"]+1):
			if (self.contratJson["clause"][str(i)]["diceRangeMin"] != 1 ) and  (self.contratJson["clause"][str(i)]["diceRangeMin"] != 21):
				points+=1

		for i in range (1, self.contratJson["preRequirement"]["amount"]+1):
			if (self.contratJson["preRequirement"][str(i)]["diceRangeMin"] != 1 ) and  (self.contratJson["preRequirement"][str(i)]["diceRangeMin"] != 21):
				points+=1

		diceResultReward += 5 * points

		if diceResultReward > 100:
			diceResultReward = 100
		elif diceResultReward < 1:
			diceResultReward = 1

		for i in data:
			if diceResultReward in range(data[str(i)]["diceRangeMin"], data[str(i)]["diceRangeMax"]+1):
				self.contratJson["reward"] = data[str(i)]
				self.contratJson["reward"]["rolledDice"] = diceResultReward

		self.contratJson["reward"]["totalAmount"] 	= self.contratJson["reward"]["totalAmount"]*self.contratJson["difficulty"]["rewardMultiplier"]
		self.contratJson["value"]["totalAmount"] 	= self.contratJson["value"]["totalAmount"]*self.contratJson["difficulty"]["valueMultiplier"]

		self.contratJson["reward"]["totalAmount"] 	= int(self.contratJson["reward"]["totalAmount"])
		self.contratJson["value"]["totalAmount"]	= int(self.contratJson["value"]["totalAmount"])
		f.close()
		pass

	def defContractor(self):
		f = open("json4Names/ContractServiceValueReward/contractors.json")
		data = json.load(f)

		whoDice =  data["whoDice"]
		whoDice["diceBonus"] += self.guildJson["reputation"]["govern"]["contractorModifier"]
		whoDice["diceBonus"] += self.guildJson["reputation"]["population"]["contractorModifier"]

		self.contratJson["contractors"] = self.rollTable(data["who"], whoDice)

		if self.contratJson["contractors"]["hasSubClass"] == True:
			subClassData = data[str(self.contratJson["contractors"]["subClassName"])]
			subclassDice = self.contratJson["contractors"]["contractorDice"]
			self.contratJson["contractors"]["subClass"] = self.rollTable(subClassData, subclassDice)
		f.close()
		pass

	def defContractType(self):
		f = open("json4Names/ContractServiceValueReward/contractors.json")
		data = json.load(f)

		self.contratJson["contractType"] = self.rollTable(data["contractType"], data["contractTypeDice"])

		f.close()
		pass

	def defObjective(self):
		f = open("json4Names/ContractServiceValueReward/objectives.json")
		fullData = json.load(f)
		objectiveJson = json.loads("{\"generalObjectives\": {}}")

		objectiveAmount = 1
		objectiveNumber = 1

		data = fullData["generalObjectives"]
		while objectiveAmount > 0:
			
			objectiveJson["generalObjectives"][str(objectiveNumber)] = self.rollTable(fullData["generalObjectives"], fullData["objectiveDice"])

			#TODO verificar um jeito que nao fique tao hardcoded
			diceResult	= objectiveJson["generalObjectives"][str(objectiveNumber)]["rolledDice"]
			rangeMin	= fullData["generalObjectives"]["20+"]["diceRangeMin"]
			rangeMax	= fullData["generalObjectives"]["20+"]["diceRangeMax"]+1

			if diceResult in range(rangeMin, rangeMax):
				objectiveAmount += 2
			else:
				objectiveKey	= objectiveJson["generalObjectives"][str(objectiveNumber)]["objectiveKey"]
				objectiveDice	= objectiveJson["generalObjectives"][str(objectiveNumber)]["objectiveDice"]
				
				if objectiveKey not in objectiveJson:
					objectiveJson[objectiveKey] = json.loads("{}")

				objectiveJson[objectiveKey][objectiveNumber] = self.rollTable (fullData[objectiveKey], objectiveDice)

				if objectiveJson[objectiveKey][objectiveNumber]["needLocation"] == True:
					locJson	= self.rollTable (fullData["locationOfObjective"], fullData["locationOfObjectiveDice"])
					objectiveJson[objectiveKey][objectiveNumber]["locationOfObjective"] = locJson

			objectiveAmount -= 1
			objectiveNumber += 1

			if objectiveNumber > self._MAX_NUMBER_OF_OBJECTIVES:
				break

		self.contratJson["objective"] = objectiveJson
		self.contratJson["objective"]["amount"] = objectiveNumber - 1

		f.close()
		pass

	def defLocation(self):
		f = open("json4Names/ContractServiceValueReward/location.json")
		fullData = json.load(f)
		resultJson = json.loads("{}")
	
		resultJson["location"] = self.rollTable(fullData["location"], fullData["locationDice"])

		resultJson["locationImportance"] = self.rollTable(fullData["locationImportance"], fullData["locationImportanceDice"])

		resultJson["peculiarity"] = self.rollTable(fullData["peculiarity"], fullData["peculiarityDice"])

		locationKey = resultJson["location"]["locationKey"]
		locationDice = resultJson["location"]["locationDice"]
		resultJson[locationKey] = self.rollTable(fullData[locationKey], locationDice)

		if resultJson[locationKey]["hasDistrict"]:
			resultJson[locationKey]["district"] = self.rollDistrict()

		self.contratJson["fullLocation"] = resultJson

		f.close()
		pass

	def rollDistrict(self):
		f = open("json4Names/ContractServiceValueReward/location.json")
		fullData = json.load(f)
		districtJson 	= fullData["isDistrict"]
		districtDice	= fullData["isDistrictDice"]
		resultJson		= json.loads("{}")

		districtAmount = 1
		districtNumber = 1
		while districtAmount > 0:
			resultJson[str(districtNumber)] = self.rollTable(districtJson, districtDice)

			#TODO verificar um jeito que nao fique tao hardcoded
			diceResult 	= resultJson[str(districtNumber)]["rolledDice"]
			rangeMin 	= districtJson["20-20"]["diceRangeMin"]
			rangeMax	= districtJson["20-20"]["diceRangeMax"]+1

			if diceResult in range(rangeMin, rangeMax):
				districtAmount += 2

			districtAmount -= 1
			districtNumber += 1

			if districtNumber > self._MAX_NUMBER_OF_DISTRICTS:
				break

		resultJson["amount"] = districtNumber - 1
		f.close()
		return resultJson

	def defAntagonist(self):
		f = open("json4Names/ContractServiceValueReward/antagonist.json")
		fullData = json.load(f)
		resultJson		= json.loads("{\"antagonist\":{}}")

		antagonistAmount = 1
		antagonistNumber = 1
		while antagonistAmount > 0:
			resultJson["antagonist"][str(antagonistNumber)] = self.rollTable(fullData["antagonist"], fullData["antagonistDice"])

			#TODO verificar um jeito que nao fique tao hardcoded
			diceResult 	= resultJson["antagonist"][str(antagonistNumber)]["rolledDice"]
			rangeMin 	= fullData["antagonist"]["20-20"]["diceRangeMin"]
			rangeMax	= fullData["antagonist"]["20-20"]["diceRangeMax"]+1

			if diceResult in range(rangeMin, rangeMax):
				antagonistAmount += 2
			else:
				antagonistKey 	= resultJson["antagonist"][str(antagonistNumber)]["antagonistKey"]
				antagonistDice	= resultJson["antagonist"][str(antagonistNumber)]["antagonistDice"]

				if antagonistKey not in resultJson:
					resultJson[antagonistKey] = json.loads("{}")
				resultJson[antagonistKey][antagonistNumber] = self.rollTable(fullData[antagonistKey], antagonistDice)

			antagonistAmount -= 1
			antagonistNumber += 1

			if antagonistNumber > self._MAX_NUMBER_OF_ANTAGONISTS:
				break

		resultJson["antagonist"]["amount"] = antagonistNumber - 1
		self.contratJson["fullAntagonist"] = resultJson
		f.close()
		pass

	def defComplication(self):
		f = open("json4Names/ContractServiceValueReward/complications.json")
		fullData = json.load(f)
		resultJson		 = json.loads("{}")

		resultJson["complication"] = self.rollTable(fullData["complication"], fullData["complicationDice"])
		
		complicationKey = resultJson["complication"]["complicationKey"]
		resultJson[complicationKey] = self.rollTable(fullData[complicationKey], resultJson["complication"]["complicationDice"])

		self.contratJson["complications"] = resultJson
		f.close()
		pass
	
	def defAllies(self):
		f = open("json4Names/ContractServiceValueReward/allies.json")
		fullData = json.load(f)
		resultJson = json.loads("{}")

		resultJson["exist"] = False

		diceResult 	=  self.rollDice(fullData["haveAlly"]["dice"])
		rangeMin	= fullData["haveAlly"]["existRangeMin"]
		rangeMax	= fullData["haveAlly"]["existRangeMax"]+1

		if diceResult in range(rangeMin, rangeMax):
			resultJson["exist"] = True
		resultJson["existRolledDice"] = diceResult

		if resultJson["exist"] == False:
			self.contratJson["allies"] = resultJson
			return

		resultJson["ally"] = self.rollTable(fullData["ally"], fullData["alliesDice"])

		allyKey = resultJson["ally"]["allyKey"]
		resultJson[allyKey] = self.rollTable(fullData[allyKey], resultJson["ally"]["allyDice"])

		resultJson["whenHowAppear"] = self.rollTable(fullData["whenHowAppear"], fullData["whenHowAppearDice"])

		self.contratJson["allies"] = resultJson
		pass

	def rollTable(self, tableJson, diceToRoll):
		resultJson = json.loads("{}")
		diceResult =  self.rollDice(diceToRoll)
		if diceResult < 1:
			diceResult = 1
		elif diceResult > diceToRoll["diceType"]:
			diceResult = diceToRoll["diceType"]
		for i in tableJson:
			if diceResult in range(tableJson[str(i)]["diceRangeMin"], tableJson[str(i)]["diceRangeMax"]+1):
				resultJson = tableJson[str(i)]
				resultJson["rolledDice"] = diceResult
		return resultJson

	#TODO precisa trazer a tabela de vilao e fazer a logica de rolagem de vilao
	def defVillain(self):
		if self.contratJson["contractType"]["villainNeed"] == False:
			return

		f = open("json4Names/ContractServiceValueReward/villians.json")
		data = json.load(f)
		#TODO check this function, he are not working yet
		diceResult = self.dice.roll(1, 20)

		for i in data["contractType"]:
			if diceResult in range(data["contractType"][str(i)]["diceRangeMin"], data["contractType"][str(i)]["diceRangeMax"]+1):
				self.contratJson["contractType"] = data["contractType"][str(i)]
				self.contratJson["contractType"]["rolledDice"] = diceResult

		f.close()
		pass