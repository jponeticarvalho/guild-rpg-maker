#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import json
import os
from contracts import ContractMaker

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
		self.main_frame = tk.Frame(self.Gerador)
		self.main_frame.configure(height=200, width=200)
		self.guildSelectFrame = ttk.Frame(self.main_frame)
		self.guildSelectFrame.configure(height=600, width=800)
		self.guildNameTxt = tk.Text(self.guildSelectFrame)
		self.guildNameTxt.configure(height=20, width=100)
		self.guildNameTxt.grid(column=0, padx="5 5", row=1, sticky="ew")
		frame5 = ttk.Frame(self.guildSelectFrame)
		frame5.configure(height=200, width=200)
		self.guildNameStr = tk.StringVar(value='Selecione a Guilda')
		__values = ['Selecione a Guilda']
		self.guildSlectOpMenu = MyOptionMenu(
			frame5,
			self.guildNameStr,
			*__values,
			command=self.guildSelectorCallback)
		self.guildSlectOpMenu.setVar(myOptMenuVar=self.guildNameStr)
		self.guildSlectOpMenu.grid(column=0, padx=20, pady="10 5", row=0)
		frame5.grid(column=0, row=0)
		self.guildSelectFrame.pack()
		frame7 = ttk.Frame(self.main_frame)
		frame7.configure(height=200, width=200)
		self.contractText = tk.Text(frame7)
		self.contractText.configure(height=15, width=50)
		self.contractText.grid(
			column=0,
			padx="5 2",
			pady="1 5",
			row=1,
			sticky="nsw")
		self.serviceText = tk.Text(frame7)
		self.serviceText.configure(height=15, width=50)
		self.serviceText.grid(
			column=1,
			padx="2 5",
			pady="1 5",
			row=1,
			sticky="nse")
		frame1 = ttk.Frame(frame7)
		frame1.configure(height=200, width=200)
		self.contractOptMenuVar = tk.StringVar(value='Contratos')
		__values = ['Contratos']
		self.contractOptMenu = MyOptionMenu(
			frame1,
			self.contractOptMenuVar,
			*__values,
			command=self.contractsSelectorCallback)
		self.contractOptMenu.setVar(myOptMenuVar=self.contractOptMenuVar)
		self.contractOptMenu.grid(column=0, padx=20, pady="8 5", row=0)
		self.createContractBtn = tk.Button(frame1)
		self.createContractBtn.configure(text='Gerar Contrato')
		self.createContractBtn.grid(column=1, padx=20, pady="8 5", row=0)
		self.createContractBtn.configure(
			command=self.createContractBtnCallback)
		frame1.grid(column=0, row=0)
		frame3 = ttk.Frame(frame7)
		frame3.configure(height=200, width=200)
		self.servicesOptMenuVar = tk.StringVar(value='Servicos')
		__values = ['Servicos']
		self.serviceOptMenu = MyOptionMenu(
			frame3,
			self.servicesOptMenuVar,
			*__values,
			command=self.servicesSelesctorCallback)
		self.serviceOptMenu.setVar(myOptMenuVar=self.servicesOptMenuVar)
		self.serviceOptMenu.grid(column=0, padx=20, pady="8 5", row=0)
		self.createServiceBtn = tk.Button(frame3)
		self.createServiceBtn.configure(text='Gerar Servico')
		self.createServiceBtn.grid(column=1, padx=20, pady="8 5", row=0)
		self.createServiceBtn.configure(command=self.createServiceBtnCallback)
		frame3.grid(column=1, row=0)
		frame7.pack()
		self.main_frame.grid(column=0, row=1)
		self.Gerador.grid_anchor("center")

		# Main widget
		self.mainwindow = self.Gerador

	def run(self):
		path = "generatedGuild/"
		dir_list =  os.walk(path)

		for j in dir_list:
			subFolders = j[1]
			break
		
		self.guildSlectOpMenu.resetOptions()
		for j in subFolders:
			f = open(path + j + "/" + j + ".json")
			data = json.load(f)
			self.guildSlectOpMenu.addOption (label=data["name"])
						
		self.mainwindow.mainloop()

	def guildSelectorCallback(self, option):
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

		self.guildNameTxt.config(state = tk.NORMAL)
		self.guildNameTxt.delete("1.0", "end")
		if aux == 0:
			return
		elif aux > 1:
			self.guildNameTxt.insert(tk.END, '               !!!!!!!!!!WARNING!!!!!!!!!!\n\r')
			self.guildNameTxt.insert(tk.END, 'ESSA GUILDA É REPETIDA EXISTE MAIS DE UMA COM O MESMO NOME\n\r')
			self.guildNameTxt.insert(tk.END, '               !!!!!!!!!!!!!!!!!!!!!!!!!!!\n\r\n\r')

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
			self.guildNameTxt.insert(tk.END, '{} = {}\n'.format(k,display_info[k]))
		self.guildNameTxt.config(state = tk.DISABLED)

		self.fileName = fileName
		self.fillContractOptMenu(fileName)
		pass

	def fillContractOptMenu(self, fileName):
		##Fill contractselector and service selector
		path = "generatedGuild/" + fileName + "/" + "contracts/"
		subFolders = os.listdir(path)

		self.contractOptMenu.resetOptions()

		for j in subFolders:
			self.contractOptMenu.addOption (label=j)
		pass

	def fillServiceOptMenu(self, fileName):
		pass
		##Fill contractselector and service selector
		path = "generatedGuild/" + fileName + "/" + "services/"
		subFolders = os.listdir(path)

		self.serviceOptMenu.resetOptions()

		for j in subFolders:
			self.serviceOptMenu.addOption (label=j)
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
				display_info["Sub Objetivo "+str(amountOfObjectives)] 	= data["objective"][dataObjective[str(i)]["objectiveKey"]][str(i)]["name"]
		display_info["TipoContrato"] = data["contractType"]["name"]
		display_info["Contratante"] = data["contractors"]["name"]
		for i in range(1, data["clause"]["amount"] + 1):
			display_info["Clausula "+str(i)] = data["clause"][str(i)]["name"]
		for i in range(1, data["preRequirement"]["amount"] + 1):
			display_info["PreRequisito "+str(i)] = data["preRequirement"][str(i)]["name"]
		display_info["Distancia"] = data["distance"]["name"]
		display_info["Dificuldade"] = data["difficulty"]["name"]
		display_info["Valor"] = data["value"]["totalAmount"]
		display_info["Recompensa"] = data["reward"]["totalAmount"]
		display_info["Prazo"] = str(data["dueDate"]["amount"]["value"]) + " Dias"

		for k in display_info:
			self.contractText.insert(tk.END, '{} = {}\n'.format(k,display_info[k]))
		self.contractText.config(state = tk.DISABLED)
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
			if data["name"] == str(self.guildNameStr.get()):
				guildJson = data
		
		result = contractCreator.creatContract(guildJson)

		if result == "error":
			return
		
		fileName = result["guild"]["fileName"]
		self.fillContractOptMenu(fileName)
		pass

	def servicesSelesctorCallback(self, option):
		pass

	def createServiceBtnCallback(self):
		pass


if __name__ == "__main__":
	app = ContractviewerApp()
	app.run()

