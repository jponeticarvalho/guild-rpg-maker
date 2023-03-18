#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import os
import json
import shutil
import openai

from contracts import ContractMaker
from guild import GuildMaker

defaultConfig   = '{"theme": "dark","gptApiKey": "","gptEnabled": false}'
_themes         = ['dark', 'light']
_model_engine    = "gpt-3.5-turbo"

class ContractviewerApp:
    def __init__(self, master=None):
        # build ui
        self.Gerador = tk.Tk() if master is None else tk.Toplevel(master)
        self.Gerador.configure(height=600, padx=10, pady=10, width=800)
        self.Gerador.resizable(False, False)
        self.notebook1 = ttk.Notebook(self.Gerador)
        self.notebook1.configure(height=680, width=820)
        self.guildFrame = ttk.Frame(self.notebook1)
        self.guildFrame.configure(height=200, width=200)
        frame3 = ttk.Frame(self.guildFrame)
        frame3.configure(height=200, width=200)
        self.sizeComboBox = ttk.Combobox(frame3)
        self.sizeStrVar = tk.StringVar()
        self.sizeComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.sizeStrVar,
            values=['Selecione o Tamanho do assentamento'],
            width=40)
        self.sizeComboBox.current(0)
        self.sizeComboBox.grid(column=0, padx=20, pady=5, row=0)
        self.isHumanSettCheckbox = ttk.Checkbutton(frame3)
        self.isHumanBoolVar = tk.BooleanVar()
        self.isHumanSettCheckbox.configure(
            text='Assentamento humano?',
            variable=self.isHumanBoolVar)
        self.isHumanSettCheckbox.grid(column=1, padx=20, pady=5, row=0)
        self.createGuildBtn = ttk.Button(frame3)
        self.createGuildBtn.configure(text='Gerar Guilda', width=20)
        self.createGuildBtn.grid(column=2, padx=20, pady=5, row=0)
        self.createGuildBtn.configure(command=self.createGuildBtnCb)
        frame3.grid(column=0, pady=5, row=0)
        self.guildSelComboBox = ttk.Combobox(self.guildFrame)
        self.guildSelComboBoxVar = tk.StringVar()
        self.guildSelComboBox.configure(
            state="readonly",
            textvariable=self.guildSelComboBoxVar,
            values=['Selecione uma guilda para vizualização'],
            width=50)
        self.guildSelComboBox.current(0)
        self.guildSelComboBox.grid(column=0, pady=5, row=1)
        self.guildSelComboBox.bind(
            "<<ComboboxSelected>>",
            self.guildSelectCb,
            add="")
        self.guildShowerText = tk.Text(self.guildFrame)
        self.guildShowerText.configure(height=35, width=100)
        self.guildShowerText.grid(column=0, padx=8, pady="0 3", row=2)
        label3 = ttk.Label(self.guildFrame)
        label3.configure(text='powered by twitch.tv/Owneti')
        label3.grid(column=0, row=4)
        self.guildFrame.pack(side="top")
        self.notebook1.add(self.guildFrame, text='Gerar Guilda')
        self.contractFrame = ttk.Frame(self.notebook1)
        self.contractFrame.configure(height=200, width=200)
        self.contGuildSelComboBox = ttk.Combobox(self.contractFrame)
        self.contGuildSelComboBoxVar = tk.StringVar()
        self.contGuildSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.contGuildSelComboBoxVar,
            values=['Selecione uma guilda para vizualização'],
            width=50)
        self.contGuildSelComboBox.current(0)
        self.contGuildSelComboBox.grid(column=0, padx=20, pady=10, row=0)
        self.contGuildSelComboBox.bind(
            "<<ComboboxSelected>>",
            self.contractGuildSelectCb,
            add="")
        frame10 = ttk.Frame(self.contractFrame)
        frame10.configure(height=200, width=200)
        self.contractComboBox = ttk.Combobox(frame10)
        self.contractComboBoxVar = tk.StringVar()
        self.contractComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.contractComboBoxVar,
            values=['Contratos'],
            width=40)
        self.contractComboBox.current(0)
        self.contractComboBox.grid(column=0, padx=20, row=0)
        self.contractComboBox.bind(
            "<<ComboboxSelected>>",
            self.contractSelectorCb,
            add="")
        self.createContractBtn = ttk.Button(frame10)
        self.createContractBtn.configure(text='Gerar Contrato', width=25)
        self.createContractBtn.grid(column=1, padx=20, row=0)
        self.createContractBtn.configure(command=self.createContractBtnCb)
        frame10.grid(column=0, pady=5, row=1)
        self.contractShowerText = tk.Text(self.contractFrame)
        self.contractShowerText.configure(height=35, width=100)
        self.contractShowerText.grid(column=0, padx=8, pady="0 3", row=2)
        label7 = ttk.Label(self.contractFrame)
        label7.configure(text='powered by twitch.tv/Owneti')
        label7.grid(column=0, row=3)
        self.contractFrame.pack(side="top")
        self.notebook1.add(self.contractFrame, text='Gerar Contrato')
        self.serviceFrame = ttk.Frame(self.notebook1)
        self.serviceFrame.configure(height=200, width=200)
        self.servGuildSelComboBox = ttk.Combobox(self.serviceFrame)
        self.servGuildSelComboBoxVar = tk.StringVar()
        self.servGuildSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.servGuildSelComboBoxVar,
            values=['Selecione uma guilda para vizualização'],
            width=50)
        self.servGuildSelComboBox.current(0)
        self.servGuildSelComboBox.grid(column=0, padx=20, pady=10, row=0)
        self.servGuildSelComboBox.bind(
            "<<ComboboxSelected>>",
            self.serviceGuildSelectCb,
            add="")
        frame13 = ttk.Frame(self.serviceFrame)
        frame13.configure(height=200, width=200)
        self.serviceComboBox = ttk.Combobox(frame13)
        self.serviceComboBoxVar = tk.StringVar()
        self.serviceComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.serviceComboBoxVar,
            values=['Serviços'],
            width=40)
        self.serviceComboBox.current(0)
        self.serviceComboBox.grid(column=0, padx=20, row=0)
        self.serviceComboBox.bind(
            "<<ComboboxSelected>>",
            self.serviceSelectorCb,
            add="")
        self.createServiceBtn = ttk.Button(frame13)
        self.createServiceBtn.configure(text='Gerar Serviço', width=25)
        self.createServiceBtn.grid(column=1, padx=20, row=0)
        self.createServiceBtn.configure(command=self.createServiceBtnCb)
        frame13.grid(column=0, pady=5, row=1)
        self.serviceShowerText = tk.Text(self.serviceFrame)
        self.serviceShowerText.configure(height=35, width=100)
        self.serviceShowerText.grid(column=0, padx=8, pady="0 3", row=2)
        label9 = ttk.Label(self.serviceFrame)
        label9.configure(text='powered by twitch.tv/Owneti')
        label9.grid(column=0, row=3)
        self.serviceFrame.pack(side="top")
        self.notebook1.add(self.serviceFrame, text='Gerar Servico')
        self.themeFrame = ttk.Frame(self.notebook1)
        self.themeFrame.configure(height=200, width=200)
        self.chatGPTApiKeyEntry = ttk.Entry(self.themeFrame)
        self.chatGPTApiKeyVar = tk.StringVar()
        self.chatGPTApiKeyEntry.configure(
            textvariable=self.chatGPTApiKeyVar, width=50)
        self.chatGPTApiKeyEntry.grid(column=0, pady="5 10", row=2)
        self.chatGPTApiKeyLabel = ttk.Label(self.themeFrame)
        self.chatGPTApiKeyLabel.configure(text='ChatGPT API-KEY')
        self.chatGPTApiKeyLabel.grid(column=0, row=1)
        self.enableChatGPTBtn = ttk.Checkbutton(self.themeFrame)
        self.enableChatGPTVar = tk.BooleanVar()
        self.enableChatGPTBtn.configure(
            text='Habilitar ChatGPT',
            variable=self.enableChatGPTVar)
        self.enableChatGPTBtn.grid(column=0, pady=10, row=3)
        self.themeComboBox = ttk.Combobox(self.themeFrame)
        self.themeComboBox.configure(values=['dark', 'light'])
        self.themeComboBox.current(0)
        self.themeComboBox.grid(column=0, pady="5 10", row=5)
        label1 = ttk.Label(self.themeFrame)
        label1.configure(text='Tema')
        label1.grid(column=0, pady="10 5", row=4)
        frame16 = ttk.Frame(self.themeFrame)
        frame16.configure(height=200, width=200)
        self.saveConfigBtn = ttk.Button(frame16)
        self.saveConfigBtn.configure(text='Salvar configuraçoes', width=30)
        self.saveConfigBtn.grid(column=2, padx="10 20", row=0)
        self.saveConfigBtn.configure(command=self.saveConfigBtnCb)
        self.restoreConfigBtn = ttk.Button(frame16)
        self.restoreConfigBtn.configure(
            text='Recuperar Configurações', width=30)
        self.restoreConfigBtn.grid(column=0, padx=10, row=0)
        self.restoreConfigBtn.configure(command=self.restoreConfigBtnCb)
        frame16.grid(column=0, pady=10, row=7)
        frame18 = ttk.Frame(self.themeFrame)
        frame18.configure(height=200, width=200)
        self.deleteNonExistGuildBtn = ttk.Button(frame18)
        self.deleteNonExistGuildBtn.configure(
            text='Excluir Guildas Inexistente', width=30)
        self.deleteNonExistGuildBtn.pack(pady="5 10")
        self.deleteNonExistGuildBtn.configure(
            command=self.deleteNonExistGuildBtnCb)
        frame18.grid(column=0, row=6)
        self.themeFrame.pack(anchor="center", side="top")
        self.themeFrame.grid_anchor("center")
        self.notebook1.add(self.themeFrame, text='Configuraçoes')
        self.frame14 = ttk.Frame(self.notebook1)
        self.frame14.configure(height=200, width=200)
        self.gptGuildSelComboBox = ttk.Combobox(self.frame14)
        self.gptGuildSelComboBoxVar = tk.StringVar()
        self.gptGuildSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.gptGuildSelComboBoxVar,
            values=['Selecione uma guilda para vizualização'],
            width=50)
        self.gptGuildSelComboBox.current(0)
        self.gptGuildSelComboBox.grid(column=0, padx=20, pady=10, row=0)
        self.gptGuildSelComboBox.bind(
            "<<ComboboxSelected>>",
            self.gptGuildSelectCb,
            add="")
        frame15 = ttk.Frame(self.frame14)
        frame15.configure(height=200, width=200)
        self.gptContractoSelComboBox = ttk.Combobox(frame15)
        self.gptContractoSelComboBoxVar = tk.StringVar()
        self.gptContractoSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.gptContractoSelComboBoxVar,
            values=['Contratos'],
            width=40)
        self.gptContractoSelComboBox.current(0)
        self.gptContractoSelComboBox.grid(column=0, padx=20, row=0)
        self.gptContractoSelComboBox.bind(
            "<<ComboboxSelected>>", self.gptContractSelectorCb, add="")
        self.createContractContextBtn = ttk.Button(frame15)
        self.createContractContextBtn.configure(
            text='Gerar Contexto', width=25)
        self.createContractContextBtn.grid(column=1, padx=20, row=0)
        self.createContractContextBtn.configure(
            command=self.createContractContextBtnCb)
        frame15.grid(column=0, pady=5, row=1)
        self.gptContContextShowerText = tk.Text(self.frame14)
        self.gptContContextShowerText.configure(height=35, width=100)
        self.gptContContextShowerText.grid(column=0, padx=8, pady="0 3", row=2)
        label10 = ttk.Label(self.frame14)
        label10.configure(text='powered by twitch.tv/Owneti')
        label10.grid(column=0, row=3)
        self.frame14.pack(side="top")
        self.notebook1.add(
            self.frame14,
            state="hidden",
            text='Gerar Contrato ChatGPT')
        self.notebook1.grid()
        self.Gerador.grid_anchor("center")

        # Main widget
        self.mainwindow = self.Gerador

    def createGuildBtnCb(self):
        if self.sizeComboBox.get() == 'Selecione o Tamanho do assentamento':
            messagebox.showerror('Python Error', 'É necessario selecionar o tamanho do assentamento!')
            return

        with open("json4Names/guildSettlementSize.json", encoding="utf-8") as f:
            data = json.load(f)

        for i in data:
            if data[str(i)]["name"] == self.sizeStrVar.get():
                settlement = i
        try:
            settlement = int(settlement)
        except:
            return
        
        guildCreator = GuildMaker()
        result = guildCreator.createGuild(settlement, self.isHumanBoolVar.get())

        if result == "error":
            return

        self.updateGuildList()
        iterator = 0
        for i in self.guildSelComboBox['values']:
            if i == result['name']:
                newId = iterator
                break
            iterator += 1
        self.guildSelComboBox.current(newId)
        self.guildSelectCb()
        pass

    def guildSelectCb(self, event=None):
        path = "generatedGuild/"
        dir_list = os.walk(path)

        result = json.loads("{}")
        aux = 0 
        fileName = ""

        for j in dir_list:
            subFolders = j[1]
            break

        for j in subFolders:
            with open(path + j + "/" + j + ".json", encoding="utf-8") as f:
                data = json.load(f)
            if data["name"] == str(self.guildSelComboBox.get()):
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

    def contractGuildSelectCb(self, event=None):
        path = "generatedGuild/"
        dir_list =  os.walk(path)
        fileName = ""

        for j in dir_list:
            subFolders = j[1]
            break

        for j in subFolders:
            with open(path + j + "/" + j + ".json", encoding="utf-8") as f:
                data = json.load(f)
            if data["name"] == str(self.contGuildSelComboBox.get()):
                fileName = j

        self.fileName = fileName
        self.fillContractOptMenu(fileName)
        pass

    def fillContractOptMenu(self, fileName):
        ##Fill contractselector and service selector
        path = "generatedGuild/" + fileName + "/" + "contracts/"
        try:
            subFolders = os.listdir(path)
        except:
            self.contractComboBox['values'] = ''
            return
        self.contractComboBox['values'] = [j for j in subFolders]
        pass

    def contractSelectorCb(self, event=None):
        path = "generatedGuild/" + self.fileName + "/" + "contracts/" + self.contractComboBox.get()
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        self.contractShowerText.config(state = tk.NORMAL)
        self.contractShowerText.delete("1.0", "end")

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
        display_info["Importancia da local"] = data["fullLocation"]["locationImportance"]["name"]
        display_info["Peculiaridade do local"] = data["fullLocation"]["peculiarity"]["name"]
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

        if data["allies"]["exist"]:
            display_info["Havera Aliados?"] = "Sim"
            display_info["Aliado"] = data["allies"]["ally"]["name"]
            allyKey = data["allies"]["ally"]["allyKey"]
            display_info["Especificacao de Aliado"] = data["allies"][allyKey]["name"]
            display_info["Quando/Como aparecera"] = data["allies"]["whenHowAppear"]["name"]
        else:
            display_info["Havera Aliados?"] = "Nao"

        if data["extraRewards"]["exist"]:
            display_info["Havera Recompensa extra?"] = "Sim"
            display_info["Recompensa Extra"] = data["extraRewards"]["extraReward"]["name"]
            rewardKey = data["extraRewards"]["extraReward"]["rewardKey"]
            display_info["Especificacao de R. extra"] = data["extraRewards"][rewardKey]["name"]
        else:
            display_info["Havera Recompensa extra?"] = "Nao"

        if data["turnarounds"]["exist"]:
            display_info["Havera Reviravolta?"] = "Sim"
            display_info["Quem?"] = data["turnarounds"]["who"]["name"]
            display_info["Na Verdade..."] = data["turnarounds"]["inTrue"]["name"]
            display_info["Mas..."] = data["turnarounds"]["but"]["name"]
            display_info["E..."] = data["turnarounds"]["and1"]["name"]
            display_info["E...."] = data["turnarounds"]["and2"]["name"]

            if data["turnarounds"]["existConsequence"]:
                display_info["Havera consequencias mais severas?"] = "Sim"
                display_info["Os contratados.."] = data["turnarounds"]["theContractors"]["name"]
                display_info["E...."] = data["turnarounds"]["and3"]["name"]
            else:
                display_info["Havera consequencias mais severas?"] = "Nao"
        else:
            display_info["Havera Reviravolta?"] = "Nao"

        if data["biluteteias"]["exist"]:
            display_info["Tem contratante inusitado?"] = "Sim"
            display_info["Contratante inusitado"] = data["biluteteias"]["biluteteia"]["name"]
        else:
            display_info["Tem contratante inusitado?"] = "Nao"

        display_info["Valor"] = str(data["value"]["totalAmount"])+" XP(experiencia)"
        display_info["Recompensa"] = str(data["reward"]["totalAmount"])+" PO(Peças de Ouro)"
        display_info["Prazo"] = str(data["dueDate"]["amount"]["value"]) + " Dias"

        display_info[" "] = " "
        if data["keywords"]["existRolledDice"] > 0:
            keyNumber = 1
            for i in range(1, data["keywords"]["existRolledDice"]+1):
                display_info["Palavra-chave de Contrato "+str(keyNumber)] = data["keywords"]["keyword"+str(keyNumber)]["name"]
                keyNumber += 1

        if data["keywordsContractor"]["existRolledDice"] > 0:
            keyNumber = 1
            for i in range(1, data["keywordsContractor"]["existRolledDice"]+1):
                display_info["Palavra-chave de Contratante "+str(keyNumber)] = data["keywordsContractor"]["contractorKeyword"+str(keyNumber)]["name"]
                keyNumber += 1

        for k in display_info:
            self.contractShowerText.insert(tk.END, '{} = {}\n'.format(k,display_info[k]))
        self.contractShowerText.config(state = tk.DISABLED)
        pass

    def createContractBtnCb(self):
        if self.contGuildSelComboBox.get() == 'Selecione uma guilda para vizualização':
            messagebox.showerror('Python Error', 'É necessario selecionar a guilda!')
            return

        contractCreator = ContractMaker()

        path = "generatedGuild/"
        dir_list =  os.walk(path)

        result = json.loads("{}")

        for j in dir_list:
            subFolders = j[1]
            break

        for j in subFolders:
            with open(path + j + "/" + j + ".json", encoding="utf-8") as f:
                data = json.load(f)
            if data["name"] == str(self.contGuildSelComboBox.get()):
                guildJson = data
        
        result = contractCreator.creatContract(guildJson)

        if result == "error":
            return
        
        fileName = result["guild"]["fileName"]
        self.fillContractOptMenu(fileName)

        iterator = 0
        for i in self.contractComboBox['values']:
            if i == result['fileName']:
                newId = iterator
                break
            iterator += 1
        self.contractComboBox.current(newId)
        self.contractSelectorCb()
        pass

    def serviceGuildSelectCb(self, event=None):
        pass

    def serviceSelectorCb(self, event=None):
        pass

    def createServiceBtnCb(self):
        pass

    def saveConfigBtnCb(self):
        self.savedConfig['gptEnabled'] = self.enableChatGPTVar.get()
        self.savedConfig['gptApiKey'] = self.chatGPTApiKeyEntry.get()
        self.savedConfig["theme"] = self.themeComboBox.get()

        if self.savedConfig['gptEnabled']: 
            if self.chatGPTApiKeyEntry.get() != '':
                new_state = "normal"
            else:
                messagebox.showerror('Python Error', 'É necessario configurar uma API-KEY para habiltiar o ChatGPT!')
                new_state = "hidden"
        else:
            new_state = "hidden"
        self.notebook1.tab(4, state=new_state)
        
        self.Gerador.tk.call('set_theme', self.savedConfig["theme"])

        with open("config.json", 'w') as f:
            f.write(json.dumps(self.savedConfig, indent=4))
        pass

    def restoreConfigBtnCb(self):
        with open("config.json", 'w') as f:
            self.savedConfig = json.loads(defaultConfig)
            f.write(json.dumps(self.savedConfig, indent=4))
        self.readSavedConfigs()
        pass

    def deleteNonExistGuildBtnCb(self):
        path = "generatedGuild/"
        dir_list =  os.walk(path)

        for j in dir_list:
            subFolders = j[1]
            break

        values = set()
        for j in subFolders:
            with open(path + j + "/" + j + ".json", encoding="utf-8") as f:
                data = json.load(f)
            if not data["exist"]:
                values.add(path + j)

        for i in values:
            shutil.rmtree(i)
        
        pass

    def gptGuildSelectCb(self, event=None):
        path = "generatedGuild/"
        dir_list =  os.walk(path)

        fileName = ""

        for j in dir_list:
            subFolders = j[1]
            break

        for j in subFolders:
            with open(path + j + "/" + j + ".json", encoding="utf-8") as f:
                data = json.load(f)
            if data["name"] == str(self.gptGuildSelComboBox.get()):
                fileName = j

        self.fileName = fileName
        self.fillGptContractOptMenu(fileName)
        pass

    def fillGptContractOptMenu(self, fileName):
        ##Fill contractselector and service selector
        path = "generatedGuild/" + fileName + "/" + "contracts/"
        try:
            subFolders = os.listdir(path)
        except:
            self.gptContractoSelComboBox['values'] = ''
            return
        self.gptContractoSelComboBox['values'] = [j for j in subFolders]
        pass

    def gptContractSelectorCb(self, event=None):
        path = "generatedGuild/" + self.fileName + "/" + "contracts/" + self.gptContractoSelComboBox.get()
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        self.gptContContextShowerText.config(state = tk.NORMAL)
        self.gptContContextShowerText.delete("1.0", "end")

        if data["gptContextGen"]["exist"]:
            self.gptContContextShowerText.insert(tk.END, data["gptContextGen"]["text"])
        else:
             self.gptContContextShowerText.insert(tk.END, "Esse contrato ainda nao possui um contexto gerado pelo ChatGPT")
        self.gptContContextShowerText.config(state = tk.DISABLED)
        pass

    def createContractContextBtnCb(self):
        if self.gptGuildSelComboBox.get() == 'Selecione uma guilda para vizualização':
            messagebox.showerror('Python Error', 'É necessario selecionar a guilda!')
            return
        if self.gptContractoSelComboBox.get() == 'Contratos':
            messagebox.showerror('Python Error', 'É necessario selecionar um contrato!')
            return
        
        path = "generatedGuild/" + self.fileName + "/" + "contracts/" + self.gptContractoSelComboBox.get()
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        self.gptContContextShowerText.config(state = tk.NORMAL)
        self.gptContContextShowerText.delete("1.0", "end")

        gptMsgToSend = 'Crie e contextualize no presente uma missao de RPG usando seguintes informacoes:\n'

        dataObjective = data["objective"]["generalObjectives"]
        amountOfObjectives = 0
        for i in dataObjective:
            if dataObjective[str(i)]["diceRangeMin"] != 20:
                amountOfObjectives += 1
                gptMsgToSend += f'-Objetivo {amountOfObjectives} : {dataObjective[str(i)]["name"]}, tendo em foco " {data["objective"][dataObjective[str(i)]["objectiveKey"]][str(i)]["name"]}"\n'
        
        gptMsgToSend += f'-Contratante: {data["contractors"]["name"]}'
        if data["contractors"]["name"] == "Governo":
            gptMsgToSend += f', {data["contractors"]["subClass"]["name"]}'
        gptMsgToSend += f'\n'

        amountOfObjects = 0
        for i in range(1, data["clause"]["amount"] + 1):
            if data["clause"][str(i)]["diceRangeMin"] < 21:
                amountOfObjects += 1
                gptMsgToSend += f'-Clausula {amountOfObjects}: {data["clause"][str(i)]["name"]}\n'
        
        amountOfObjects = 0
        for i in range(1, data["preRequirement"]["amount"] + 1):
            if data["preRequirement"][str(i)]["diceRangeMin"] < 21:
                amountOfObjects += 1
                gptMsgToSend += f'-PreRequisito {amountOfObjects}: {data["preRequirement"][str(i)]["name"]}\n'
        
        gptMsgToSend += f'-Distancia da missao: {data["distance"]["name"]}\n'

        locationKey = data["fullLocation"]["location"]["locationKey"]
        gptMsgToSend += f'-Localização: {data["fullLocation"][locationKey]["name"]} de uma/um {data["fullLocation"]["location"]["name"]}\n'
        if data["fullLocation"][locationKey]["hasDistrict"] == True:
            amountOfDistrict = 0
            gptMsgToSend += "-O(s) distrito(s) é(são): \n"
            for i in range (1, data["fullLocation"][locationKey]["district"]["amount"]+1):
                if data["fullLocation"][locationKey]["district"][str(i)]["diceRangeMin"] != 20:
                    amountOfDistrict += 1
                    gptMsgToSend += f'-Distrito {amountOfDistrict}: {data["fullLocation"][locationKey]["district"][str(i)]["name"]}\n'
        gptMsgToSend += f'-Peculiaridade do local: {data["fullLocation"]["peculiarity"]["name"]}\n'
        gptMsgToSend += f'-Importancia do local: {data["fullLocation"]["locationImportance"]["name"]}\n'

        gptMsgToSend += f'-Dificuldade da missao: {data["difficulty"]["name"]}\n'

        antagonistJson = data["fullAntagonist"]["antagonist"]
        amountOfAntagonist = 0
        gptMsgToSend += f'-Antagonista(s): \n'
        for i in antagonistJson:
            if str(i) != "amount" and antagonistJson[str(i)]["diceRangeMin"] != 20:
                amountOfAntagonist += 1
                antagonistKey = antagonistJson[str(i)]["antagonistKey"]
                gptMsgToSend += f'-Antagonista {amountOfAntagonist}: {antagonistJson[str(i)]["name"]}, {data["fullAntagonist"][antagonistKey][str(i)]["name"]}\n'
        
        complicationKey = data["complications"]["complication"]["complicationKey"]
        gptMsgToSend += f'-Complicações: {data["complications"][complicationKey]["name"]}\n'

        if data["allies"]["exist"]:
            allyKey = data["allies"]["ally"]["allyKey"]
            gptMsgToSend += f'-Aliado: {data["allies"]["ally"]["name"]}, {data["allies"][allyKey]["name"]}\n'
            gptMsgToSend += f'-Quando/como o aliado aparecerá: {data["allies"]["whenHowAppear"]["name"]}\n'

        if data["extraRewards"]["exist"]:
            rewardKey = data["extraRewards"]["extraReward"]["rewardKey"]
            gptMsgToSend += f'-Recompensa extra: {data["extraRewards"]["extraReward"]["name"]}, {data["extraRewards"][rewardKey]["name"]}\n'

        if data["turnarounds"]["exist"]:
            gptMsgToSend += f'-Reviravoltas: {data["turnarounds"]["who"]["name"]}'
            gptMsgToSend += f',na verdade {data["turnarounds"]["inTrue"]["name"]}'
            gptMsgToSend += f',mas {data["turnarounds"]["but"]["name"]}'
            gptMsgToSend += f',e {data["turnarounds"]["and1"]["name"]}, e {data["turnarounds"]["and2"]["name"]}\n'

            if data["turnarounds"]["existConsequence"]:
                gptMsgToSend += f'-Consequencias mais severas: "Os contratados {data["turnarounds"]["theContractors"]["name"]}'
                gptMsgToSend += f',e {data["turnarounds"]["and3"]["name"]}"\n'

        if data["biluteteias"]["exist"]:
            gptMsgToSend += f'-Contratante inusitado: {data["biluteteias"]["biluteteia"]["name"]}\n'

        gptMsgToSend += f'-Valor: {data["value"]["totalAmount"]} XP(experiencia)\n'
        gptMsgToSend += f'-Recompensa: {data["reward"]["totalAmount"]} PO(Peças de Ouro)\n'
        gptMsgToSend += f'-Prazo: {data["dueDate"]["amount"]["value"]} Dias\n'

        if data["keywords"]["existRolledDice"] > 0:
            keyNumber = 1
            gptMsgToSend += '-Palavras-chave para a missao: '
            for i in range(1, data["keywords"]["existRolledDice"]+1):
                gptMsgToSend += f'{data["keywords"]["keyword"+str(keyNumber)]["name"]}, '
                keyNumber += 1
            gptMsgToSend += '\n'

        if data["keywordsContractor"]["existRolledDice"] > 0:
            keyNumber = 1
            gptMsgToSend += '-Palavras-chave para o contratante: '
            for i in range(1, data["keywordsContractor"]["existRolledDice"]+1):
                gptMsgToSend += f'{data["keywordsContractor"]["contractorKeyword"+str(keyNumber)]["name"]}, '
                keyNumber += 1
            gptMsgToSend += '\n'

        gptResponse = self.sendToGPT(gptMsgToSend)

        data["gptContextGen"]["exist"]  = True
        data["gptContextGen"]["text"]   = gptResponse

        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, indent=4))

        if data["gptContextGen"]["exist"]:
            self.gptContContextShowerText.insert(tk.END, data["gptContextGen"]["text"])
        else:
             self.gptContContextShowerText.insert(tk.END, "Esse contrato ainda nao possui um contexto gerado pelo ChatGPT")
        self.gptContContextShowerText.config(state = tk.DISABLED)

        pass

    def sendToGPT(self, data):
        msg = [{"role": "user", "content": data}]

        # Generate a response
        openai.api_key = self.savedConfig['gptApiKey']
        completion = openai.ChatCompletion.create(
            model=_model_engine,
            messages=msg
        )

        return completion.choices[0].message.content

    def setup(self):
        if not os.path.exists('generatedGuild'):
            os.mkdir('generatedGuild')
        if not os.path.isfile('config.json'):
            with open('config.json', 'w+') as f:
                f.write(defaultConfig)

    def readSavedConfigs(self):
        with open("config.json") as f:
            self.savedConfig = json.load(f)
        
        if self.savedConfig['gptEnabled']: 
            if self.savedConfig['gptApiKey'] != '':
                new_state = "normal"
            else:
                new_state = "hidden"
        else:
            new_state = "hidden"
        self.notebook1.tab(4, state=new_state)
        
        #Update the interface
        self.Gerador.tk.call('set_theme', self.savedConfig["theme"])

        self.chatGPTApiKeyEntry.delete("0", "end")
        self.chatGPTApiKeyEntry.insert("0", self.savedConfig['gptApiKey'])

        self.enableChatGPTVar.set(self.savedConfig["gptEnabled"])

        iterator = 0
        for i in _themes:
            if self.savedConfig["theme"] == i:
                self.themeComboBox.current(iterator)
                break
            iterator += 1

        pass

    def updateGuildList(self):
        path = "generatedGuild/"
        dir_list =  os.walk(path)

        for j in dir_list:
            subFolders = j[1]
            break

        values = set()
        valuesExisted = set()
        for j in subFolders:
            with open(path + j + "/" + j + ".json", encoding="utf-8") as f:
                data = json.load(f)
            values.add(data["name"])
            if data["exist"]:
                valuesExisted.add(data["name"])

        self.guildSelComboBox['values']     = [i for i in values]
        self.contGuildSelComboBox['values'] = [i for i in valuesExisted]
        self.servGuildSelComboBox['values'] = [i for i in valuesExisted]
        self.gptGuildSelComboBox['values']  = [i for i in valuesExisted]
        pass

    def run(self):
        self.setup()

        self.Gerador.tk.call('source', 'azure.tcl')

        self.readSavedConfigs()

        self.updateGuildList()

        #FILL size settlement
        with open("json4Names/guildSettlementSize.json", encoding="utf-8") as f:
            data = json.load(f)

        self.sizeComboBox['values'] = [data[str(i)]["name"] for i in data]

        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = ContractviewerApp()
    app.run()
