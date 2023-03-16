import json

import contracts

contractCreator = contracts.Contract()

f = open('generatedGuild/guild02-26-2023-21-55-35.json')
data = json.load(f)

myJson = [
    json.loads('{}'),
    json.loads('{}'),
    json.loads('{}'),
    json.loads('{}'),
    json.loads('{}'),
    json.loads('{}'),
    json.loads('{}'),
    json.loads('{}'),
    json.loads('{}'),
    json.loads('{}'),
]

for j in range(0, 20):
    for i in range(0, 10):
        myJson[i] = contractCreator.creatContract(data)

print(myJson)
