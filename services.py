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

        if filename == 'serviceObjective' and resultJson['objective'] == 'Trabalho rural':
            resultJson['ruralJob'] = self.rollTable(data['ruralJob'], data['ruralJobDice'])

        return resultJson
        pass

    def rollRecruitObjective(self):
        with open(f'{self._SERVICE_PATH}objective/recruitObjective.json', encoding="utf-8") as f:
            data = json.load(f)

        resultJson = json.loads('{}')

        resultJson['objective'] = self.rollTable(data['objective'], data['objectiveDice'])
        resultJson['for'] = self.rollTable(data['for'], data['forDice'])
        resultJson['but'] = self.rollTable(data['but'], data['butDice'])

        return resultJson
        pass

    def rollHealObjective(self):
        with open(f'{self._SERVICE_PATH}objective/healObjective.json', encoding="utf-8") as f:
            data = json.load(f)

        resultJson = json.loads('{}')

        resultJson['objective'] = self.rollTable(data['objective'], data['objectiveDice'])
        resultJson['for'] = self.rollTable(data['for'], data['forDice'])
        resultJson['but'] = self.rollTable(data['but'], data['butDice'])

        return resultJson
        pass

    def rollNegociationObjective(self):
        with open(f'{self._SERVICE_PATH}objective/negociationObjective.json', encoding="utf-8") as f:
            data = json.load(f)

        resultJson = json.loads('{}')

        resultJson['objective'] = self.rollTable(data['objective'], data['objectiveDice'])
        resultJson['for'] = self.rollTable(data['for'], data['forDice'])
        resultJson['but'] = self.rollTable(data['but'], data['butDice'])

        return resultJson
        pass

    def rollHelpObjective(self):
        with open(f'{self._SERVICE_PATH}objective/helpObjective.json', encoding="utf-8") as f:
            data = json.load(f)

        resultJson = json.loads('{}')

        resultJson['objective'] = self.rollTable(data['objective'], data['objectiveDice'])
        resultJson['for'] = self.rollTable(data['for'], data['forDice'])
        resultJson['but'] = self.rollTable(data['but'], data['butDice'])

        return resultJson
        pass

    def rollExtractObjective(self):
        with open(f'{self._SERVICE_PATH}objective/extractObjective.json', encoding="utf-8") as f:
            data = json.load(f)

        resultJson = json.loads('{}')

        resultJson['objective'] = self.rollTable(data['objective'], data['objectiveDice'])
        resultJson['for'] = self.rollTable(data['for'], data['forDice'])
        resultJson['but'] = self.rollTable(data['but'], data['butDice'])

        return resultJson
        pass

    def rollBuildObjective(self):
        with open(f'{self._SERVICE_PATH}objective/buildObjective.json', encoding="utf-8") as f:
            data = json.load(f)

        resultJson = json.loads('{}')

        resultJson['objective'] = self.rollTable(data['objective'], data['objectiveDice'])
        resultJson['for'] = self.rollTable(data['for'], data['forDice'])
        resultJson['but'] = self.rollTable(data['but'], data['butDice'])

        return resultJson
        pass

    def rollServiceObjective(self):
        with open(f'{self._SERVICE_PATH}objective/serviceObjective.json', encoding="utf-8") as f:
            data = json.load(f)

        resultJson = json.loads('{}')

        resultJson['objective'] = self.rollTable(data['objective'], data['objectiveDice'])
        resultJson['for'] = self.rollTable(data['for'], data['forDice'])
        resultJson['but'] = self.rollTable(data['but'], data['butDice'])

        return resultJson
        pass

    def rollReligiousObjective(self):
        with open(f'{self._SERVICE_PATH}objective/religiousObjective.json', encoding="utf-8") as f:
            data = json.load(f)

        resultJson = json.loads('{}')

        resultJson['objective'] = self.rollTable(data['objective'], data['objectiveDice'])
        resultJson['for'] = self.rollTable(data['for'], data['forDice'])
        resultJson['but'] = self.rollTable(data['but'], data['butDice'])

        return resultJson
        pass
