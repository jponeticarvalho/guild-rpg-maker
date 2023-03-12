#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import json
import os
from contracts import ContractMaker
from guild import GuildMaker

class MyOptionMenu(tk.OptionMenu):
	def __init__(self, *args, **kw):
		self._command = kw.get("command")
		tk.OptionMenu.__init__(self, *args, **kw)
	def setVar(self, myOptMenuVar):
		self.myOptMenuVar = myOptMenuVar
	def addOption(self, label):
		self["menu"].add_command(label=label,
		command=tk._setit(self.myOptMenuVar, label, self._command))
	def resetOptions(self):
		self['menu'].delete(0,'end') # remove full list

class ContractviewerApp:
	def __init__(self, master=None):
		# build ui
		self.Gerador = tk.Tk() if master is None else tk.Toplevel(master)
		self.Gerador.configure(height=600, padx=10, pady=10, width=800)
		self.Gerador.resizable(False, False)
		notebook1 = ttk.Notebook(self.Gerador)
		notebook1.configure(height=680, width=820)
		self.guildFrame = tk.Frame(notebook1)
		self.guildFrame.configure(height=200, width=200)
		self.guildShowerText = tk.Text(self.guildFrame)
		self.guildShowerText.configure(height=35, width=100)
		self.guildShowerText.grid(column=0, padx=8, pady=5, row=2)
		label2 = tk.Label(self.guildFrame)
		label2.configure(text='powered by twitch.tv/Owneti')
		label2.grid(column=0, row=3)
		frame10 = tk.Frame(self.guildFrame)
		frame10.configure(height=200, width=200)
		frame13 = tk.Frame(frame10)
		frame13.configure(height=200, width=200)
		self.sizeStrVar = tk.StringVar(
			value='Selecione o Tamanho do assentamento')
		__values = ['Selecione o Tamanho do assentamento']
		self.sizeOptMenu = MyOptionMenu(
			frame13, self.sizeStrVar, *__values, command=None)
		self.sizeOptMenu.pack(padx=20, pady=5)
		self.sizeOptMenu.setVar(myOptMenuVar=self.sizeStrVar)
		frame13.grid(column=0, row=0)
		frame15 = tk.Frame(frame10)
		frame15.configure(height=200, width=200)
		self.isHumanSettCheckBoxx = tk.Checkbutton(frame15)
		self.isHumanBoolVar = tk.BooleanVar()
		self.isHumanSettCheckBoxx.configure(
			cursor="arrow",
			text='Assentamento humano?',
			variable=self.isHumanBoolVar)
		self.isHumanSettCheckBoxx.pack(padx=20, pady=5)
		frame15.grid(column=1, row=0)
		frame3 = tk.Frame(frame10)
		frame3.configure(height=200, width=200)
		self.createGuildBtn = tk.Button(frame3)
		self.createGuildBtn.configure(justify="left", text='Gerar Guilda')
		self.createGuildBtn.pack(padx=20, pady=5)
		self.createGuildBtn.configure(command=self.createGuildBtnCallback)
		frame3.grid(column=2, row=0)
		frame10.grid(column=0, pady=5, row=0)
		self.guildOptMenuVar = tk.StringVar(
			value='Selecione uma guilda para vizualização')
		__values = ['Selecione uma guilda para vizualização']
		self.guildSelectOptMenu = MyOptionMenu(
            self.guildFrame,
            self.guildOptMenuVar,
            *__values,
            command=self.guildSelectCallback)
		self.guildSelectOptMenu.grid(column=0, row=1)
		self.guildFrame.pack()
		self.guildSelectOptMenu.setVar(myOptMenuVar=self.guildOptMenuVar)
		notebook1.add(self.guildFrame, text='Gerar Guilda')
		self.contractFrame = tk.Frame(notebook1)
		self.contractFrame.configure(height=200, width=200)
		self.contractGuildSelectFrame = tk.Frame(self.contractFrame)
		self.contractGuildSelectFrame.configure(height=200, width=200)
		frame20 = tk.Frame(self.contractGuildSelectFrame)
		frame20.configure(height=200, width=200)
		self.contGuildNameStr = tk.StringVar(value='Selecione a Guilda')
		__values = ['Selecione a Guilda']
		self.contGuildSelOptMenu = MyOptionMenu(
			frame20,
			self.contGuildNameStr,
			*__values,
			command=self.contractGuildSelectCallback)
		self.contGuildSelOptMenu.grid(column=0, padx=20, pady=5, row=0)
		self.contGuildSelOptMenu.setVar(myOptMenuVar=self.contGuildNameStr)
		frame20.pack(pady=5)
		self.contractGuildSelectFrame.pack(side="top")
		frame21 = tk.Frame(self.contractFrame)
		frame21.configure(height=200, width=200)
		self.contractText = tk.Text(frame21)
		self.contractText.configure(height=35, width=100)
		self.contractText.grid(column=0, padx=8, pady=5, row=1, sticky="nsw")
		frame22 = tk.Frame(frame21)
		frame22.configure(height=200, width=200)
		self.createContractBtn = tk.Button(frame22)
		self.createContractBtn.configure(
			default="normal", text='Gerar Contrato')
		self.createContractBtn.grid(column=1, padx=20, row=0)
		self.createContractBtn.configure(
			command=self.createContractBtnCallback)
		self.contractOptMenuVar = tk.StringVar(value='Contratos')
		__values = ['Contratos']
		self.contractOptMenu = MyOptionMenu(
			frame22,
			self.contractOptMenuVar,
			*__values,
			command=self.contractsSelectorCallback)
		self.contractOptMenu.grid(column=0, padx=20, row=0)
		self.contractOptMenu.setVar(myOptMenuVar=self.contractOptMenuVar)
		frame22.grid(column=0, row=0)
		frame21.pack(side="top")
		label5 = tk.Label(self.contractFrame)
		label5.configure(text='powered by twitch.tv/Owneti')
		label5.pack(side="top")
		self.contractFrame.pack()
		notebook1.add(self.contractFrame, text='Gerar Contrato')
		self.serviceFrame = tk.Frame(notebook1)
		self.serviceFrame.configure(height=200, width=200)
		self.serviceGuildSelectFrame = tk.Frame(self.serviceFrame)
		self.serviceGuildSelectFrame.configure(height=200, width=200)
		frame9 = tk.Frame(self.serviceGuildSelectFrame)
		frame9.configure(height=200, width=200)
		self.servGuildNameStr = tk.StringVar(value='Selecione a Guilda')
		__values = ['Selecione a Guilda']
		self.servGuildSelOptMenu = MyOptionMenu(
			frame9,
			self.servGuildNameStr,
			*__values,
			command=self.serviceGuildSelectCallback)
		self.servGuildSelOptMenu.grid(column=0, padx=20, pady=5, row=0)
		self.servGuildSelOptMenu.setVar(myOptMenuVar=self.servGuildNameStr)
		frame9.pack(pady=5)
		self.serviceGuildSelectFrame.pack(side="top")
		frame14 = tk.Frame(self.serviceFrame)
		frame14.configure(height=200, width=200)
		self.serviceText = tk.Text(frame14)
		self.serviceText.configure(height=35, width=100)
		self.serviceText.grid(column=0, padx=8, pady=5, row=1, sticky="nsw")
		frame12 = tk.Frame(frame14)
		frame12.configure(height=200, width=200)
		self.createServiceBtn = tk.Button(frame12)
		self.createServiceBtn.configure(text='Gerar Serviço')
		self.createServiceBtn.grid(column=1, padx=20, row=0)
		self.createServiceBtn.configure(command=self.createServiceBtnCallback)
		self.seviceOptMenuVar = tk.StringVar(value='Servicos')
		__values = ['Servicos']
		self.serviceOptMenu = MyOptionMenu(
			frame12,
			self.seviceOptMenuVar,
			*__values,
			command=self.contractsSelectorCallback)
		self.serviceOptMenu.grid(column=0, padx=20, row=0)
		self.serviceOptMenu.setVar(myOptMenuVar=self.seviceOptMenuVar)
		frame12.grid(column=0, row=0)
		frame14.pack(side="top")
		label4 = tk.Label(self.serviceFrame)
		label4.configure(text='powered by twitch.tv/Owneti')
		label4.pack(side="top")
		self.serviceFrame.pack()
		notebook1.add(self.serviceFrame, text='Gerar Servico')
		notebook1.grid()
		self.Gerador.grid_anchor("center")

		# Main widget
		self.mainwindow = self.Gerador

	def setup(self):
		if not os.path.exists('generatedGuild'):
			os.mkdir('generatedGuild')

	def run(self):
		self.setup()
		self.updateGuildList()

		#FILL size settlement
		f = open("json4Names/guildSettlementSize.json")
		dataSettlement = json.load(f)

		self.sizeOptMenu.resetOptions()
		for i in dataSettlement:
			self.sizeOptMenu.addOption(label=dataSettlement[str(i)]["name"])

		self.mainwindow.mainloop()

	def updateGuildList(self):
		path = "generatedGuild/"
		dir_list =  os.walk(path)

		for j in dir_list:
			subFolders = j[1]
			break
		
		self.guildSelectOptMenu.resetOptions()
		self.contGuildSelOptMenu.resetOptions()
		self.servGuildSelOptMenu.resetOptions()
		for j in subFolders:
			f = open(path + j + "/" + j + ".json")
			data = json.load(f)
			self.guildSelectOptMenu.addOption(label=data["name"])
			self.contGuildSelOptMenu.addOption(label=data["name"])
			self.servGuildSelOptMenu.addOption(label=data["name"])
		pass

	def createGuildBtnCallback(self):
		f = open ("json4Names/guildSettlementSize.json")
		dataSettlement = json.load(f)

		for i in dataSettlement:
			if dataSettlement[str(i)]["name"] == self.sizeStrVar.get():
				settlement = i
		try:
			settlement = int(settlement)
		except:
			return
		
		guildCreator = GuildMaker()
		result = guildCreator.createGuild(settlement, self.isHumanBoolVar.get())

		if result == "error":
			return

		display_info = json.loads("{}")

		display_info["Nome da Guilda"] = result["name"]
		display_info["Assentamento"] = result["settlementSize"]["name"]
		display_info["Existe"] = result["exist"]
		display_info["BonusDado"] = result["guildDiceBonus"]
		display_info["DadoRolado"] = result["rolledDice"]
		display_info["AssentamentoHumano"] = result["isHuman"]
		if display_info["Existe"] == True:
			display_info["Tamanho"] = result["size"]["name"]
			display_info["Caracteristica"] = result["Characteristic"]["name"]
			display_info["Reputação Governo"] = result["reputation"]["govern"]["name"]
			display_info["Reputacao Populacao"] = result["reputation"]["population"]["name"]
			display_info["Funcionarios"] = result["employees"]["name"]
			display_info["QtdFunc"] = result["employees"]["amount"]["value"]
			display_info["Recursos"] = result["resource"]["name"]
			display_info["QtdMovimento"] = result["goers"]["name"]

		#txt_guild["text"] = json.dumps(result, sort_keys=True, indent=4)
		self.guildShowerText.config(state = tk.NORMAL)
		self.guildShowerText.delete("1.0", "end")
		for k in display_info:
			self.guildShowerText.insert(tk.END, '{} = {}\n'.format(k,display_info[k]))
		self.guildShowerText.config(state = tk.DISABLED)

		self.updateGuildList()
		pass

	def guildSelectCallback(self, option):
		path = "generatedGuild/"
		dir_list = os.walk(path)

		result = json.loads("{}")
		aux = 0 
		fileName = ""

		for j in dir_list:
			subFolders = j[1]
			break

		for j in subFolders:
			f = open(path + j + "/" + j + ".json")
			data = json.load(f)
			if data["name"] == str(option):
				result = data
				fileName = j
				aux += 1

		self.guildShowerText.config(state = tk.NORMAL)
		self.guildShowerText.delete("1.0", "end")
		if aux == 0:
			return
		elif aux > 1:
			self.guildShowerText.insert(tk.END, '               !!!!!!!!!!WARNING!!!!!!!!!!\n\r')
			self.guildShowerText.insert(tk.END, 'ESSA GUILDA É REPETIDA EXISTE MAIS DE UMA COM O MESMO NOME\n\r')
			self.guildShowerText.insert(tk.END, '               !!!!!!!!!!!!!!!!!!!!!!!!!!!\n\r\n\r')

		display_info = json.loads("{}")

		display_info["Nome da Guilda"] = result["name"]
		display_info["Assentamento"] = result["settlementSize"]["name"]
		display_info["Existe"] = result["exist"]
		display_info["BonusDado"] = result["guildDiceBonus"]
		display_info["DadoRolado"] = result["rolledDice"]
		display_info["AssentamentoHumano"] = result["isHuman"]
		if display_info["Existe"] == True:
			display_info["Tamanho"] = result["size"]["name"]
			display_info["Caracteristica"] = result["Characteristic"]["name"]
			display_info["Reputação Governo"] = result["reputation"]["govern"]["name"]
			display_info["Reputacao Populacao"] = result["reputation"]["population"]["name"]
			display_info["Funcionarios"] = result["employees"]["name"]
			display_info["QtdFunc"] = result["employees"]["amount"]["value"]
			display_info["Recursos"] = result["resource"]["name"]
			display_info["QtdMovimento"] = result["goers"]["name"]

		for k in display_info:
			self.guildShowerText.insert(tk.END, '{} = {}\n'.format(k,display_info[k]))
		self.guildShowerText.config(state = tk.DISABLED)
		pass

	def contractGuildSelectCallback(self, option):
		path = "generatedGuild/"
		dir_list =  os.walk(path)

		result = json.loads("{}")
		aux = 0 
		fileName = ""

		for j in dir_list:
			subFolders = j[1]
			break

		for j in subFolders:
			f = open(path + j + "/" + j + ".json")
			data = json.load(f)
			if data["name"] == str(option):
				result = data
				fileName = j
				aux += 1

		self.fileName = fileName
		self.fillContractOptMenu(fileName)
		pass

	def fillContractOptMenu(self, fileName):
		##Fill contractselector and service selector
		path = "generatedGuild/" + fileName + "/" + "contracts/"
		try:
			subFolders = os.listdir(path)
		except:
			self.contractOptMenu.resetOptions()
			return

		self.contractOptMenu.resetOptions()

		for j in subFolders:
			self.contractOptMenu.addOption (label=j)
		pass

	def createContractBtnCallback(self):
		contractCreator = ContractMaker()

		path = "generatedGuild/"
		dir_list =  os.walk(path)

		result = json.loads("{}")

		for j in dir_list:
			subFolders = j[1]
			break

		for j in subFolders:
			f = open(path + j + "/" + j + ".json")
			data = json.load(f)
			if data["name"] == str(self.contGuildNameStr.get()):
				guildJson = data
		
		result = contractCreator.creatContract(guildJson)

		if result == "error":
			return
		
		fileName = result["guild"]["fileName"]
		self.fillContractOptMenu(fileName)
		self.contractsSelectorCallback(result["fileName"])
		pass

	def contractsSelectorCallback(self, option):
		path = "generatedGuild/" + self.fileName + "/" + "contracts/" + option
		f = open (path)
		data = json.load(f)

		self.contractText.config(state = tk.NORMAL)
		self.contractText.delete("1.0", "end")

		display_info = json.loads("{}")

		dataObjective = data["objective"]["generalObjectives"]
		amountOfObjectives = 0
		for i in dataObjective:
			if dataObjective[str(i)]["diceRangeMin"] != 20:
				amountOfObjectives += 1
				display_info["Objetivo "+str(amountOfObjectives)] 		= dataObjective[str(i)]["name"]
				display_info["Sub-Objetivo "+str(amountOfObjectives)] 	= data["objective"][dataObjective[str(i)]["objectiveKey"]][str(i)]["name"]
		display_info["TipoContrato"] = data["contractType"]["name"]
		display_info["Contratante"] = data["contractors"]["name"]
		if display_info["Contratante"] == "Governo":
			display_info["Sub-Contratante"] = data["contractors"]["subClass"]["name"]
		amountOfObjects = 0
		for i in range(1, data["clause"]["amount"] + 1):
			if data["clause"][str(i)]["diceRangeMin"] < 21:
				amountOfObjects += 1
				display_info["Clausula "+str(amountOfObjects)] = data["clause"][str(i)]["name"]
		amountOfObjects = 0
		for i in range(1, data["preRequirement"]["amount"] + 1):
			if data["preRequirement"][str(i)]["diceRangeMin"] < 21:
				amountOfObjects += 1
				display_info["PreRequisito "+str(amountOfObjects)] = data["preRequirement"][str(i)]["name"]
		display_info["Distancia"] = data["distance"]["name"]
		display_info["Localizacao"] = data["fullLocation"]["location"]["name"]
		locationKey = data["fullLocation"]["location"]["locationKey"]
		display_info["Esp. Local"] = data["fullLocation"][locationKey]["name"]
		if data["fullLocation"][locationKey]["hasDistrict"] == True:
			amountOfDistrict = 0
			for i in range (1, data["fullLocation"][locationKey]["district"]["amount"]+1):
				if data["fullLocation"][locationKey]["district"][str(i)]["diceRangeMin"] != 20:
					amountOfDistrict += 1
					display_info["Distrito "+str(amountOfDistrict)] = data["fullLocation"][locationKey]["district"][str(i)]["name"]
		display_info["Dificuldade"] = data["difficulty"]["name"]

		antagonistJson = data["fullAntagonist"]["antagonist"]
		amountOfAntagonist = 0
		for i in antagonistJson:
			if str(i) != "amount" and antagonistJson[str(i)]["diceRangeMin"] != 20:
				amountOfAntagonist += 1
				display_info["Antagonista " + str(amountOfAntagonist)] = antagonistJson[str(i)]["name"]
				antagonistKey = antagonistJson[str(i)]["antagonistKey"]
				display_info["Sub-Antagonista " + str(amountOfAntagonist)] = data["fullAntagonist"][antagonistKey][str(i)]["name"]
		
		display_info["Complicacao"] = data["complications"]["complication"]["name"]
		complicationKey = data["complications"]["complication"]["complicationKey"]
		display_info["Sub-Complicacao"] = data["complications"][complicationKey]["name"]

		display_info["Valor"] = data["value"]["totalAmount"]
		display_info["Recompensa"] = data["reward"]["totalAmount"]
		display_info["Prazo"] = str(data["dueDate"]["amount"]["value"]) + " Dias"

		for k in display_info:
			self.contractText.insert(tk.END, '{} = {}\n'.format(k,display_info[k]))
		self.contractText.config(state = tk.DISABLED)
		pass

	def serviceGuildSelectCallback(self, option):
		pass

	def fillServiceOptMenu(self, fileName):
		pass
		##Fill contractselector and service selector
		path = "generatedGuild/" + fileName + "/" + "services/"
		subFolders = os.listdir(path)

		self.serviceOptMenu.resetOptions()

		for j in subFolders:
			self.serviceOptMenu.addOption(label=j)
		pass

	def createServiceBtnCallback(self):
		pass


if __name__ == "__main__":
	app = ContractviewerApp()
	app.run()
