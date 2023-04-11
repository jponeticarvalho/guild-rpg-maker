import random
import json
import os

from dice import diceRoll
from guild import GuildMaker

class ServiceMaker:
    
    dice = diceRoll()
    serviceJson = json.loads("{}")

    _COMMON_PATH = 'json4Names/ContractServiceValueReward/'
    _SERVICE_PATH = f'{_COMMON_PATH}services/'
    
    def createService(self, guildJson):
        self.guildJson = guildJson

        self.defContractor          ()
        self.defObjective           ()
        self.defComplication        ()
        self.defRival               ()
        self.defAditionalQuest      ()
        self.defKeyWords            ()
        self.defRewardAndChallenge  ()

        self.serviceJson["guild"] = guildJson #guildJson["name"]
        
        servicePath = "generatedGuild/" + self.guildJson["fileName"] + "/services/"
        try:
            os.mkdir(servicePath)
        except:
            print("[ContractMaker] ERROR when creating the folder to the service returning without the guild")
            #return "error"

        self.serviceJson["gptContextGen"] = json.loads("{}")
        self.serviceJson["gptContextGen"]["exist"] = False

        contractNumber = len(os.listdir(servicePath))
        self.serviceJson["fileName"] = "service-" + str(contractNumber) + ".json"
        servicePath = servicePath + "service-" + str(contractNumber) + ".json"

        with open(servicePath, "w+") as f:
            f.write (json.dumps(self.serviceJson, indent=4))

        return self.serviceJson

    def rollDice (self, diceData):
        diceResult = 0
        print (f'[ContractRollDice] Rolling {str(diceData["diceAmount"])}d{str(diceData["diceType"])}+{str(diceData["diceBonus"])}')
        diceResult += self.dice.roll(diceData["diceAmount"], diceData["diceType"])
        diceResult += diceData["diceBonus"] # sede matriz influencia aqui?
        print (f'[ContractRollDice] Dice Result = {str(diceResult)}')
        return diceResult
    
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
    
    def defContractor(self):
        with open(f'{self._SERVICE_PATH}contractors.json', encoding="utf-8") as f:
            data = json.load(f)

        whoDice =  data["whoDice"]
        whoDice["diceBonus"] += self.guildJson["reputation"]["govern"]["serviceContractorMod"]
        whoDice["diceBonus"] += self.guildJson["reputation"]["population"]["serviceContractorMod"]

        self.serviceJson["contractors"] = self.rollTable(data["who"], whoDice)

        if self.serviceJson["contractors"]["hasSubClass"] == True:
            subClassData = data[str(self.serviceJson["contractors"]["subClassName"])]
            subclassDice = self.serviceJson["contractors"]["contractorDice"]
            self.serviceJson["contractors"]["subClass"] = self.rollTable(subClassData, subclassDice)
        pass

    def defObjective(self):
        with open(f'{self._SERVICE_PATH}objective/objective.json', encoding="utf-8") as f:
            data = json.load(f)

        resultJson = json.loads('{}')

        amountOfObj = 0
        numberOfObj = 1
        while numberOfObj > 0:
            amountOfObj += 1
            resultJson[f'objective{amountOfObj}'] = self.rollTable(data["objective"], data['objectiveDice'])

            if resultJson[f'objective{amountOfObj}']['subFileName'] == '2roll':
                numberOfObj+=2
            else:
                subFileName = resultJson[f'objective{amountOfObj}']['subFileName']
                resultJson[f'objective{amountOfObj}'][subFileName] = self.rollSubObjective(subFileName)

            numberOfObj-=1

        resultJson['amount'] = amountOfObj-1

        self.serviceJson['objectives'] = resultJson
        pass

    def rollSubObjective(self, filename):
        with open(f'{self._SERVICE_PATH}objective/{filename}.json', encoding="utf-8") as f:
            data = json.load(f)

        resultJson = json.loads('{}')

        resultJson['objective'] = self.rollTable(data['objective'], data['objectiveDice'])
        resultJson['for'] = self.rollTable(data['for'], data['forDice'])
        resultJson['but'] = self.rollTable(data['but'], data['butDice'])

        if filename == 'serviceObjective' and resultJson['objective']['name'] == 'Trabalho rural':
            resultJson['ruralJob'] = self.rollTable(data['ruralJob'], data['ruralJobDice'])

        return resultJson

    def defComplication(self):
        with open(f'{self._SERVICE_PATH}complications.json', encoding="utf-8") as f:
            fullData = json.load(f)
        resultJson = json.loads("{}")

        resultJson["exist"] = False

        diceResult 	=  self.rollDice(fullData["haveComplication"]["dice"])
        rangeMin	= fullData["haveComplication"]["existRangeMin"]
        rangeMax	= fullData["haveComplication"]["existRangeMax"]+1

        if diceResult in range(rangeMin, rangeMax):
            resultJson["exist"] = True
        resultJson["existRolledDice"] = diceResult

        if resultJson["exist"] == False:
            self.serviceJson["complications"] = resultJson
            return

        resultJson["complication"] = self.rollTable(fullData["complication"], fullData["complicationDice"])
        resultJson["and"] = self.rollTable(fullData["and"], fullData["andDice"])

        self.serviceJson["complications"] = resultJson
        pass

    def defRival(self):
        with open(f'{self._SERVICE_PATH}rivals.json', encoding="utf-8") as f:
            fullData = json.load(f)
        resultJson = json.loads("{}")

        resultJson["exist"] = False

        diceResult 	=  self.rollDice(fullData["haveRival"]["dice"])
        rangeMin	= fullData["haveRival"]["existRangeMin"]
        rangeMax	= fullData["haveRival"]["existRangeMax"]+1

        if diceResult in range(rangeMin, rangeMax):
            resultJson["exist"] = True
        resultJson["existRolledDice"] = diceResult

        if resultJson["exist"] == False:
            self.serviceJson["rivals"] = resultJson
            return

        resultJson["rival"] = self.rollTable(fullData["rival"], fullData["rivalDice"])
        resultJson["but"] = self.rollTable(fullData["but"], fullData["butDice"])

        self.serviceJson["rivals"] = resultJson
        pass

    def defAditionalQuest(self):
        with open(f'{self._SERVICE_PATH}aditionalQuest.json', encoding="utf-8") as f:
            fullData = json.load(f)
        resultJson = json.loads("{}")

        resultJson["exist"] = False

        diceResult 	=  self.rollDice(fullData["haveAddQuest"]["dice"])
        rangeMin	= fullData["haveAddQuest"]["existRangeMin"]
        rangeMax	= fullData["haveAddQuest"]["existRangeMax"]+1

        if diceResult in range(rangeMin, rangeMax):
            resultJson["exist"] = True
        resultJson["existRolledDice"] = diceResult

        if resultJson["exist"] == False:
            self.serviceJson["addQuests"] = resultJson
            return

        resultJson["addQuest"] = self.rollTable(fullData["addQuest"], fullData["addQuestDice"])
        self.serviceJson["addQuests"] = resultJson
        pass

    def defKeyWords(self):
        with open(f'{self._SERVICE_PATH}keywordsService.json', encoding="utf-8") as f:
            fullData = json.load(f)
        resultJson = json.loads("{}")

        resultJson["exist"] = True

        diceResult = self.rollDice(fullData["keywordServiceDice"])
        resultJson["existRolledDice"] = diceResult
        if diceResult == 0:
            resultJson["exist"] = False
            self.serviceJson["keywords"] = resultJson
            return

        tables = random.sample(range(1, fullData["numberOfTable"]+1), diceResult)

        keywordNumber = 1
        for i in tables:
            resultJson["keyword"+str(keywordNumber)] = self.rollTable(fullData[str(i)]["table"], fullData[str(i)]["dice"])
            resultJson["keyword"+str(keywordNumber)]["originTable"] = i
            keywordNumber += 1
        
        self.serviceJson["keywords"] = resultJson
        pass

    def defRewardAndChallenge(self):
        with open(f'{self._SERVICE_PATH}rewardAndChallenge.json', encoding="utf-8") as f:
            fullData = json.load(f)
        resultJson = json.loads("{}")

        resultJson["rewardAndChallenge"] = self.rollTable(fullData["rewardAndChallenge"], fullData["rewardAndChallengeDice"])
        resultJson["rewardAndChallenge"]["value"] = self.rollDice(resultJson["rewardAndChallenge"]["rewardDice"])
        resultJson["rewardAndChallenge"]["value"] *= resultJson["rewardAndChallenge"]["diceMultiplier"] 

        resultJson["difficulty"] = self.rollTable(fullData["difficulty"], fullData["difficultyDice"])

        self.serviceJson["rewardsAndChallenges"] = resultJson
        pass