#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.messagebox import askyesno
import os
import json
import shutil
import openai

from contracts import ContractMaker
from services import ServiceMaker
from guild import GuildMaker

defaultConfig       = '{"theme": "dark","gptApiKey": "","gptEnabled": false}'
_themes             = ['dark', 'light']
_model_engine       = "gpt-3.5-turbo"
_config_file_path   = 'globalAppConfig.json'

class ContractviewerApp:
    def __init__(self, master=None):
        # build ui
        self.Gerador = tk.Tk() if master is None else tk.Toplevel(master)
        self.Gerador.configure(height=600, padx=10, pady=10, width=800)
        self.Gerador.resizable(True, True)
        self.notebook1 = ttk.Notebook(self.Gerador)
        self.notebook1.configure(height=680, width=820)
        self.guildFrame = ttk.Frame(self.notebook1)
        self.guildFrame.configure(height=200, width=200)
        self.frame4 = ttk.Frame(self.guildFrame)
        self.frame4.configure(height=200, width=200)
        self.frame3 = ttk.Frame(self.frame4)
        self.frame3.configure(height=200, width=200)
        self.sizeComboBox = ttk.Combobox(self.frame3)
        self.sizeStrVar = tk.StringVar()
        self.sizeComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.sizeStrVar,
            values=['Selecione o Tamanho do assentamento'],
            width=40)
        self.sizeComboBox.pack(expand="true", fill="x", padx=20, side="left")
        self.createGuildBtn = ttk.Button(self.frame3)
        self.createGuildBtn.configure(
            cursor="hand2", text='Gerar Guilda', width=20)
        self.createGuildBtn.pack(
            expand="true", fill="x", padx=20, side="right")
        self.createGuildBtn.configure(command=self.createGuildBtnCb)
        self.isHumanSettCheckbox = ttk.Checkbutton(self.frame3)
        self.isHumanBoolVar = tk.BooleanVar()
        self.isHumanSettCheckbox.configure(
            text='Assentamento humano?',
            variable=self.isHumanBoolVar)
        self.isHumanSettCheckbox.pack(
            expand="true", fill="x", padx=20, side="bottom")
        self.frame3.pack(
            anchor="n",
            expand="true",
            fill="x",
            padx=20,
            pady=10,
            side="top")
        self.guildSelComboBox = ttk.Combobox(self.frame4)
        self.guildSelComboBoxVar = tk.StringVar()
        self.guildSelComboBox.configure(
            state="readonly",
            textvariable=self.guildSelComboBoxVar,
            values=['Selecione uma guilda para vizualização'],
            width=50)
        self.guildSelComboBox.pack(
            anchor="n", expand="false", pady=5, side="top")
        self.guildSelComboBox.bind(
            "<<ComboboxSelected>>",
            self.guildSelectCb,
            add="")
        self.frame4.pack(side="top")
        self.guildShowerText = tk.Text(self.guildFrame)
        self.guildShowerText.configure(height=35, width=100)
        self.guildShowerText.pack(
            anchor="n",
            expand="true",
            fill="both",
            padx=8,
            pady="0 3",
            side="top")
        self.guildFrame.pack(
            anchor="n",
            expand="true",
            fill="both",
            side="top")
        self.guildFrame.pack_propagate(0)
        self.notebook1.add(self.guildFrame, text='Gerar Guilda')
        self.contractFrame = ttk.Frame(self.notebook1)
        self.contractFrame.configure(height=200, width=200)
        self.frame5 = ttk.Frame(self.contractFrame)
        self.frame5.configure(height=200, width=200)
        self.contGuildSelComboBox = ttk.Combobox(self.frame5)
        self.contGuildSelComboBoxVar = tk.StringVar()
        self.contGuildSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.contGuildSelComboBoxVar,
            values=['Selecione uma guilda para vizualização'],
            width=50)
        self.contGuildSelComboBox.pack(padx=20, pady=10)
        self.contGuildSelComboBox.bind(
            "<<ComboboxSelected>>",
            self.contractGuildSelectCb,
            add="")
        self.frame10 = ttk.Frame(self.frame5)
        self.frame10.configure(height=200, width=200)
        self.contractComboBox = ttk.Combobox(self.frame10)
        self.contractComboBoxVar = tk.StringVar()
        self.contractComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.contractComboBoxVar,
            values=['Contratos'],
            width=40)
        self.contractComboBox.grid(column=0, padx=20, row=0)
        self.contractComboBox.bind(
            "<<ComboboxSelected>>",
            self.contractSelectorCb,
            add="")
        self.createContractBtn = ttk.Button(self.frame10)
        self.createContractBtn.configure(
            cursor="hand2", text='Gerar Contrato', width=25)
        self.createContractBtn.grid(column=1, padx=20, row=0)
        self.createContractBtn.configure(command=self.createContractBtnCb)
        self.frame10.pack(pady=5)
        self.frame5.pack(side="top")
        self.contractShowerText = tk.Text(self.contractFrame)
        self.contractShowerText.configure(height=35, width=100)
        self.contractShowerText.pack(
            anchor="n",
            expand="true",
            fill="both",
            padx=8,
            pady="0 3",
            side="top")
        self.contractFrame.pack(
            anchor="n",
            expand="true",
            fill="both",
            side="top")
        self.notebook1.add(self.contractFrame, text='Gerar Contrato')
        self.serviceFrame = ttk.Frame(self.notebook1)
        self.serviceFrame.configure(height=200, width=200)
        self.frame6 = ttk.Frame(self.serviceFrame)
        self.frame6.configure(height=200, width=200)
        self.servGuildSelComboBox = ttk.Combobox(self.frame6)
        self.servGuildSelComboBoxVar = tk.StringVar()
        self.servGuildSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.servGuildSelComboBoxVar,
            values=['Selecione uma guilda para vizualização'],
            width=50)
        self.servGuildSelComboBox.pack(padx=20, pady=10)
        self.servGuildSelComboBox.bind(
            "<<ComboboxSelected>>",
            self.serviceGuildSelectCb,
            add="")
        self.frame13 = ttk.Frame(self.frame6)
        self.frame13.configure(height=200, width=200)
        self.serviceComboBox = ttk.Combobox(self.frame13)
        self.serviceComboBoxVar = tk.StringVar()
        self.serviceComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.serviceComboBoxVar,
            values=['Serviços'],
            width=40)
        self.serviceComboBox.grid(column=0, padx=20, row=0)
        self.serviceComboBox.bind(
            "<<ComboboxSelected>>",
            self.serviceSelectorCb,
            add="")
        self.createServiceBtn = ttk.Button(self.frame13)
        self.createServiceBtn.configure(
            cursor="hand2", text='Gerar Serviço', width=25)
        self.createServiceBtn.grid(column=1, padx=20, row=0)
        self.createServiceBtn.configure(command=self.createServiceBtnCb)
        self.frame13.pack(pady=5)
        self.frame6.pack(side="top")
        self.serviceShowerText = tk.Text(self.serviceFrame)
        self.serviceShowerText.configure(height=35, width=100)
        self.serviceShowerText.pack(
            expand="true",
            fill="both",
            padx=8,
            pady="0 3",
            side="top")
        self.serviceFrame.pack(expand="true", fill="both", side="top")
        self.notebook1.add(self.serviceFrame, text='Gerar Servico')
        self.themeFrame = ttk.Frame(self.notebook1)
        self.themeFrame.configure(height=200, width=200)
        self.apiKeyFrame = ttk.Frame(self.themeFrame)
        self.apiKeyFrame.configure(height=200, width=200)
        self.chatGPTApiKeyLabel = ttk.Label(self.apiKeyFrame)
        self.chatGPTApiKeyLabel.configure(text='ChatGPT API-KEY')
        self.chatGPTApiKeyLabel.pack()
        self.chatGPTApiKeyEntry = ttk.Entry(self.apiKeyFrame)
        self.chatGPTApiKeyVar = tk.StringVar()
        self.chatGPTApiKeyEntry.configure(
            textvariable=self.chatGPTApiKeyVar, width=50)
        self.chatGPTApiKeyEntry.pack()
        self.apiKeyFrame.pack(anchor="center", pady="200 0", side="top")
        self.enableChatGPTBtn = ttk.Checkbutton(self.themeFrame)
        self.enableChatGPTVar = tk.BooleanVar()
        self.enableChatGPTBtn.configure(
            text='Habilitar ChatGPT',
            variable=self.enableChatGPTVar)
        self.enableChatGPTBtn.pack(anchor="center", pady=20, side="top")
        self.themeSelFrame = ttk.Frame(self.themeFrame)
        self.themeSelFrame.configure(height=200, width=200)
        self.label1 = ttk.Label(self.themeSelFrame)
        self.label1.configure(text='Tema')
        self.label1.pack()
        self.themeComboBox = ttk.Combobox(self.themeSelFrame)
        self.themeComboBox.configure(values=['dark', 'light'])
        self.themeComboBox.pack()
        self.themeSelFrame.pack(anchor="center", side="top")
        self.frame12 = ttk.Frame(self.themeFrame)
        self.frame12.configure(height=200, width=200)
        self.frame18 = ttk.Frame(self.frame12)
        self.frame18.configure(height=200, width=200)
        self.deleteNonExistGuildBtn = ttk.Button(self.frame18)
        self.deleteNonExistGuildBtn.configure(
            cursor="hand2", text='Excluir Guildas Inexistente', width=30)
        self.deleteNonExistGuildBtn.pack(pady="5 10")
        self.deleteNonExistGuildBtn.configure(
            command=self.deleteNonExistGuildBtnCb)
        self.frame18.pack()
        self.frame16 = ttk.Frame(self.frame12)
        self.frame16.configure(height=200, width=200)
        self.saveConfigBtn = ttk.Button(self.frame16)
        self.saveConfigBtn.configure(
            cursor="hand2",
            text='Salvar configuraçoes',
            width=30)
        self.saveConfigBtn.grid(column=2, padx="10 20", row=0)
        self.saveConfigBtn.configure(command=self.saveConfigBtnCb)
        self.restoreConfigBtn = ttk.Button(self.frame16)
        self.restoreConfigBtn.configure(
            cursor="hand2", text='Recuperar Configurações', width=30)
        self.restoreConfigBtn.grid(column=0, padx=10, row=0)
        self.restoreConfigBtn.configure(command=self.restoreConfigBtnCb)
        self.frame16.pack()
        self.frame12.pack(pady=20, side="bottom")
        self.themeFrame.pack(
            anchor="center",
            expand="true",
            fill="both",
            side="top")
        self.notebook1.add(self.themeFrame, text='Configuraçoes')
        self.frame14 = ttk.Frame(self.notebook1)
        self.frame14.configure(height=200, width=200)
        self.frame7 = ttk.Frame(self.frame14)
        self.frame7.configure(height=200, width=200)
        self.gptGuildSelComboBox = ttk.Combobox(self.frame7)
        self.gptGuildSelComboBoxVar = tk.StringVar()
        self.gptGuildSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.gptGuildSelComboBoxVar,
            values=['Selecione uma guilda para vizualização'],
            width=50)
        self.gptGuildSelComboBox.pack(padx=20, pady=10)
        self.gptGuildSelComboBox.bind(
            "<<ComboboxSelected>>", self.gptGuildSelectCb, add="")
        self.frame15 = ttk.Frame(self.frame7)
        self.frame15.configure(height=200, width=200)
        self.gptContractSelComboBox = ttk.Combobox(self.frame15)
        self.gptContractSelComboBoxVar = tk.StringVar()
        self.gptContractSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.gptContractSelComboBoxVar,
            values=['Contratos'],
            width=40)
        self.gptContractSelComboBox.grid(column=0, padx=20, row=0)
        self.gptContractSelComboBox.bind(
            "<<ComboboxSelected>>", self.gptContractSelectorCb, add="")
        self.createContractContextBtn = ttk.Button(self.frame15)
        self.createContractContextBtn.configure(
            cursor="hand2", text='Gerar Contexto', width=25)
        self.createContractContextBtn.grid(column=1, padx=20, row=0)
        self.createContractContextBtn.configure(
            command=self.createContractContextBtnCb)
        self.frame15.pack(pady=2)
        self.frame7.pack(side="top")
        self.gptContContextShowerText = tk.Text(self.frame14)
        self.gptContContextShowerText.configure(height=35, width=100)
        self.gptContContextShowerText.pack(
            expand="true", fill="both", side="top")
        self.frame14.pack(expand="true", fill="both", side="top")
        self.notebook1.add(
            self.frame14,
            state="hidden",
            text='Gerar Contrato ChatGPT')
        self.frame1 = ttk.Frame(self.notebook1)
        self.frame1.configure(height=200, width=200)
        self.frame8 = ttk.Frame(self.frame1)
        self.frame8.configure(height=200, width=200)
        self.gptServGuildSelComboBox = ttk.Combobox(self.frame8)
        self.gptServGuildSelComboBoxVar = tk.StringVar()
        self.gptServGuildSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.gptServGuildSelComboBoxVar,
            values=['Selecione uma guilda para vizualização'],
            width=50)
        self.gptServGuildSelComboBox.pack(padx=20, pady=10)
        self.gptServGuildSelComboBox.bind(
            "<<ComboboxSelected>>", self.gptServGuildSelectCb, add="")
        self.frame2 = ttk.Frame(self.frame8)
        self.frame2.configure(height=200, width=200)
        self.gptServiceSelComboBox = ttk.Combobox(self.frame2)
        self.gptServiceSelComboBoxVar = tk.StringVar()
        self.gptServiceSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.gptServiceSelComboBoxVar,
            values=['Servicos'],
            width=40)
        self.gptServiceSelComboBox.grid(column=0, padx=20, row=0)
        self.gptServiceSelComboBox.bind(
            "<<ComboboxSelected>>", self.gptServiceSelectorCb, add="")
        self.createServiceContextBtn = ttk.Button(self.frame2)
        self.createServiceContextBtn.configure(
            cursor="hand2", text='Gerar Contexto', width=25)
        self.createServiceContextBtn.grid(column=1, padx=20, row=0)
        self.createServiceContextBtn.configure(
            command=self.createServiceContextBtnCb)
        self.frame2.pack(pady=5)
        self.frame8.pack(side="top")
        self.gptServContextText = tk.Text(self.frame1)
        self.gptServContextText.configure(height=35, width=100)
        self.gptServContextText.pack(expand="true", fill="both", side="top")
        self.frame1.pack(expand="true", fill="both", side="top")
        self.notebook1.add(
            self.frame1,
            state="hidden",
            text='Gerar Servico ChatGPT')
        self.notebook1.pack(expand="true", fill="both", side="top")
        self.label5 = ttk.Label(self.Gerador)
        self.label5.configure(text='powered by twitch.tv/Owneti')
        self.label5.pack(pady="5 2")

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
        self.fillContractComboBox(fileName)
        pass

    def fillContractComboBox(self, fileName):
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
        updateGptContComboBox = True
        if self.gptGuildSelComboBox.get() == 'Selecione uma guilda para vizualização':
            updateGptContComboBox = False

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
            if updateGptContComboBox and data['name'] == str(self.gptGuildSelComboBox.get()):
                gptGuildJson = data
        
        result = contractCreator.creatContract(guildJson)

        if result == "error":
            return
        
        fileName = result["guild"]["fileName"]
        self.fillContractComboBox(fileName)
        if updateGptContComboBox:
            self.fillGptContractComboBox(gptGuildJson["fileName"])

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
        path = "generatedGuild/"
        dir_list =  os.walk(path)
        fileName = ""

        for j in dir_list:
            subFolders = j[1]
            break

        for j in subFolders:
            with open(path + j + "/" + j + ".json", encoding="utf-8") as f:
                data = json.load(f)
            if data["name"] == str(self.servGuildSelComboBox.get()):
                fileName = j

        self.fileName = fileName
        self.fillServiceComboBox(fileName)
        pass

    def fillServiceComboBox(self, fileName):
        ##Fill contractselector and service selector
        path = "generatedGuild/" + fileName + "/" + "services/"
        try:
            subFolders = os.listdir(path)
        except:
            self.serviceComboBox['values'] = ''
            return
        self.serviceComboBox['values'] = [j for j in subFolders]
        pass

    def serviceSelectorCb(self, event=None):
        path = "generatedGuild/" + self.fileName + "/" + "services/" + self.serviceComboBox.get()
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        self.serviceShowerText.config(state = tk.NORMAL)
        self.serviceShowerText.delete("1.0", "end")

        display_info = json.loads("{}")

        dataObjective = data["objectives"]
        amountOfObjectives = 0
        for i in dataObjective:
            if str(i) != 'amount' and dataObjective[str(i)]["diceRangeMin"] != 20:
                amountOfObjectives += 1
                display_info[f'Objetivo {str(amountOfObjectives)}']  = dataObjective[str(i)]["name"]
                subName = dataObjective[str(i)]['subFileName']
                display_info[f'Sub-Objetivo {(amountOfObjectives)}'] = f'{dataObjective[str(i)][subName]["objective"]["name"]} PARA {dataObjective[str(i)][subName]["for"]["name"]} MAS {dataObjective[str(i)][subName]["but"]["name"]}'
                if dataObjective[str(i)][subName]["objective"]["name"] == 'Trabalho rural':
                    display_info[f'Trabalho Rural {amountOfObjectives}'] = dataObjective[str(i)][subName]["ruralJob"]["name"]


        display_info["Contratante"] = data["contractors"]["name"]
        if display_info["Contratante"] == "Governo":
            display_info["Sub-Contratante"] = data["contractors"]["subClass"]["name"]

        if data['complications']['exist']:
            display_info['Há complicações?'] = 'Sim'
            display_info['Complicação'] = f'{data["complications"]["complication"]["name"]} E {data["complications"]["and"]["name"]}'
        else:
            display_info['Há complicações?'] = 'Nao'

        if data['rivals']['exist']:
            display_info['Há Rivais?'] = 'Sim'
            display_info['Rival'] = f'{data["rivals"]["rival"]["name"]} MAS {data["rivals"]["but"]["name"]}'
        else:
            display_info['Há Rivais?'] = 'Nao'

        if data['addQuests']['exist']:
            display_info['Há Desafio adicional?'] = 'Sim'
            display_info['Desafio adicional'] = f'{data["addQuests"]["addQuest"]["name"]}'
        else:
            display_info['Há Desafio adicional?'] = 'Nao'

        display_info["Dificuldade"] = data["rewardsAndChallenges"]["difficulty"]["name"]
        display_info["Condicoes"] = data["rewardsAndChallenges"]["difficulty"]["requirement"]

        display_info["Nivel de CD"] = data["rewardsAndChallenges"]["rewardAndChallenge"]["cd"]
        display_info["Recompensa"] = f'{data["rewardsAndChallenges"]["rewardAndChallenge"]["value"]} {data["rewardsAndChallenges"]["rewardAndChallenge"]["coin"]}'
        display_info["Taxa de Recorrencia"] = data["rewardsAndChallenges"]["rewardAndChallenge"]["recurrency"]

        successCaseJson = data["rewardsAndChallenges"]["difficulty"]["successCases"]
        for i in successCaseJson:
            display_info[f'Numero de sucessos {successCaseJson[str(i)]["successNumber"]}'] = successCaseJson[str(i)]["status"]

        display_info[" "] = " "
        if data["keywords"]["existRolledDice"] > 0:
            keyNumber = 1
            for i in range(1, data["keywords"]["existRolledDice"]+1):
                display_info["Palavra-chave de Serviço "+str(keyNumber)] = data["keywords"]["keyword"+str(keyNumber)]["name"]
                keyNumber += 1

        for k in display_info:
            self.serviceShowerText.insert(tk.END, '{} = {}\n'.format(k,display_info[k]))
        self.serviceShowerText.config(state = tk.DISABLED)
        pass

    def createServiceBtnCb(self):
        if self.servGuildSelComboBox.get() == 'Selecione uma guilda para vizualização':
            messagebox.showerror('Python Error', 'É necessario selecionar a guilda!')
            return

        serviceGenerator = ServiceMaker()

        path = "generatedGuild/"
        dir_list =  os.walk(path)

        result = json.loads("{}")

        for j in dir_list:
            subFolders = j[1]
            break

        for j in subFolders:
            with open(path + j + "/" + j + ".json", encoding="utf-8") as f:
                data = json.load(f)
            if data["name"] == str(self.servGuildSelComboBox.get()):
                guildJson = data
        
        result = serviceGenerator.createService(guildJson)

        if result == "error":
            return
        
        fileName = result["guild"]["fileName"]
        self.fillServiceComboBox(fileName)

        iterator = 0
        for i in self.serviceComboBox['values']:
            if i == result['fileName']:
                newId = iterator
                break
            iterator += 1
        self.serviceComboBox.current(newId)
        self.serviceSelectorCb()
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
        self.notebook1.tab(5, state=new_state)
        
        self.Gerador.tk.call('set_theme', self.savedConfig["theme"])

        with open(_config_file_path, 'w') as f:
            f.write(json.dumps(self.savedConfig, indent=4))
        pass

    def restoreConfigBtnCb(self):
        answer = askyesno(title='Confirmação',
                    message='Você deseja realmente restaurar as configurações?')
        if not answer:
            return
        with open(_config_file_path, 'w') as f:
            self.savedConfig = json.loads(defaultConfig)
            f.write(json.dumps(self.savedConfig, indent=4))
        self.readSavedConfigs()
        pass

    def deleteNonExistGuildBtnCb(self):
        answer = askyesno(title='Confirmação',
                    message='Você deseja realmente excluir as Guildas ano existentes?')
        if not answer:
            return
        
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
        
        self.updateGuildList()

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
        self.fillGptContractComboBox(fileName)
        pass

    def fillGptContractComboBox(self, fileName):
        ##Fill contractselector and service selector
        path = "generatedGuild/" + fileName + "/" + "contracts/"
        try:
            subFolders = os.listdir(path)
        except:
            self.gptContractSelComboBox['values'] = ''
            return
        self.gptContractSelComboBox['values'] = [j for j in subFolders]
        pass

    def gptContractSelectorCb(self, event=None):
        path = "generatedGuild/" + self.fileName + "/" + "contracts/" + self.gptContractSelComboBox.get()
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
        if self.gptContractSelComboBox.get() == 'Contratos':
            messagebox.showerror('Python Error', 'É necessario selecionar um contrato!')
            return
        
        path = "generatedGuild/" + self.fileName + "/" + "contracts/" + self.gptContractSelComboBox.get()
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
            #gptMsgToSend += '-Palavras-chave para a missao: '
            gptMsgToSend += f'-Para a criacao do contexto da missao utilize as seguintes palavras-chave: '
            for i in range(1, data["keywords"]["existRolledDice"]+1):
                gptMsgToSend += f'{data["keywords"]["keyword"+str(keyNumber)]["name"]}, '
                keyNumber += 1
            gptMsgToSend += '\n'

        if data["keywordsContractor"]["existRolledDice"] > 0:
            keyNumber = 1
            #gptMsgToSend += '-Palavras-chave para o contratante: '
            gptMsgToSend += f'-Para a criacao do contratante utilize as seguintes palavras-chave: '
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

    def gptServGuildSelectCb(self, event=None):
        path = "generatedGuild/"
        dir_list =  os.walk(path)
        fileName = ""

        for j in dir_list:
            subFolders = j[1]
            break

        for j in subFolders:
            with open(path + j + "/" + j + ".json", encoding="utf-8") as f:
                data = json.load(f)
            if data["name"] == str(self.gptServGuildSelComboBox.get()):
                fileName = j

        self.fileName = fileName
        self.fillGptServiceComboBox(fileName)
        pass

    def fillGptServiceComboBox(self, fileName):
        ##Fill contractselector and service selector
        path = "generatedGuild/" + fileName + "/" + "services/"
        try:
            subFolders = os.listdir(path)
        except:
            self.gptServiceSelComboBox['values'] = ''
            return
        self.gptServiceSelComboBox['values'] = [j for j in subFolders]
        pass

    def gptServiceSelectorCb(self, event=None):
        path = "generatedGuild/" + self.fileName + "/" + "services/" + self.gptServiceSelComboBox.get()
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        self.gptServContextText.config(state = tk.NORMAL)
        self.gptServContextText.delete("1.0", "end")

        if data["gptContextGen"]["exist"]:
            self.gptServContextText.insert(tk.END, data["gptContextGen"]["text"])
        else:
             self.gptServContextText.insert(tk.END, "Esse service ainda nao possui um contexto gerado pelo ChatGPT")
        self.gptServContextText.config(state = tk.DISABLED)
        pass

    def createServiceContextBtnCb(self):
        if self.gptServGuildSelComboBox.get() == 'Selecione uma guilda para vizualização':
            messagebox.showerror('Python Error', 'É necessario selecionar a guilda!')
            return
        if self.gptServiceSelComboBox.get() == 'Servicos':
            messagebox.showerror('Python Error', 'É necessario selecionar um servico!')
            return
        
        path = "generatedGuild/" + self.fileName + "/" + "services/" + self.gptServiceSelComboBox.get()
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        self.gptServContextText.config(state = tk.NORMAL)
        self.gptServContextText.delete("1.0", "end")

        gptMsgToSend = 'Crie e contextualize no presente um servico de RPG usando as seguintes informacoes::\n'

        dataObjective = data["objectives"]
        amountOfObjectives = 0
        for i in dataObjective:
            if str(i) != 'amount' and dataObjective[str(i)]["diceRangeMin"] != 20:
                amountOfObjectives += 1
                subName = dataObjective[str(i)]["subFileName"]
                if subName == 'trainObjective' or subName == 'recruitObjective' or subName == 'negociationObjective' or subName == 'buildObjective':
                    gptMsgToSend += f'-Objetivo {amountOfObjectives}: {dataObjective[str(i)]["name"]} {dataObjective[str(i)][subName]["objective"]["name"]} PARA {dataObjective[str(i)][subName]["for"]["name"]} MAS {dataObjective[str(i)][subName]["but"]["name"]}\n'
                elif subName == 'healObjective' or subName == 'extractObjective' or subName == 'serviceObjective':
                    gptMsgToSend += f'-Objetivo {amountOfObjectives}: {dataObjective[str(i)]["name"]} {dataObjective[str(i)][subName]["objective"]["name"]}'
                    if dataObjective[str(i)][subName]["objective"]["name"] == 'Trabalho rural':
                        gptMsgToSend += f' no/na {dataObjective[str(i)][subName]["ruralJob"]["name"]}'
                    gptMsgToSend += f' DE {dataObjective[str(i)][subName]["for"]["name"]} MAS {dataObjective[str(i)][subName]["but"]["name"]}\n'
                elif subName == 'helpObjective':
                    gptMsgToSend += f'-Objetivo {amountOfObjectives}: {dataObjective[str(i)]["name"]} {dataObjective[str(i)][subName]["objective"]["name"]}, EM QUE? {dataObjective[str(i)][subName]["for"]["name"]} MAS {dataObjective[str(i)][subName]["but"]["name"]}\n'
                elif subName == 'religiousObjective':
                    gptMsgToSend += f'-Objetivo {amountOfObjectives}: {dataObjective[str(i)]["name"]} {dataObjective[str(i)][subName]["objective"]["name"]}, O QUE/QUEM? {dataObjective[str(i)][subName]["for"]["name"]} MAS {dataObjective[str(i)][subName]["but"]["name"]}\n'
        
        gptMsgToSend += f'-Contratante: {data["contractors"]["name"]}'
        if data["contractors"]["name"] == "Governo":
            gptMsgToSend += f', {data["contractors"]["subClass"]["name"]}'
        gptMsgToSend += f'\n'

        if data["complications"]["exist"]:
            gptMsgToSend += f'-Complicação: {data["complications"]["complication"]["name"]} E {data["complications"]["and"]["name"]}\n'

        if data['rivals']['exist']:
            gptMsgToSend += f'-Rivais: {data["rivals"]["rival"]["name"]} MAS {data["rivals"]["but"]["name"]}\n'


        if data['addQuests']['exist']:
            gptMsgToSend += f'-Desafio Adicional: {data["addQuests"]["addQuest"]["name"]}\n'

        gptMsgToSend += f'-Dificuldade: {data["rewardsAndChallenges"]["difficulty"]["name"]}\n'

        gptMsgToSend += f'-Condicoes de conclusao: {data["rewardsAndChallenges"]["difficulty"]["requirement"]}\n'

        gptMsgToSend += f'-Nivel de CD: {data["rewardsAndChallenges"]["rewardAndChallenge"]["cd"]}\n'

        gptMsgToSend += f'-Recompensa: {data["rewardsAndChallenges"]["rewardAndChallenge"]["value"]} {data["rewardsAndChallenges"]["rewardAndChallenge"]["coin"]}\n'

        gptMsgToSend += f'-Taxa de Recorrencia: {data["rewardsAndChallenges"]["rewardAndChallenge"]["recurrency"]}\n'

        if data["keywords"]["existRolledDice"] > 0:
            keyNumber = 1
            gptMsgToSend += f'-Para a criacao do context do servico utilize as seguintes palavras-chave: '
            for i in range(1, data["keywords"]["existRolledDice"]+1):
                gptMsgToSend += f'{data["keywords"]["keyword"+str(keyNumber)]["name"]}, '
                keyNumber += 1
            gptMsgToSend += '\n'

        gptResponse = self.sendToGPT(gptMsgToSend)

        data["gptContextGen"]["exist"]  = True
        data["gptContextGen"]["text"]   = gptResponse

        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, indent=4))

        if data["gptContextGen"]["exist"]:
            self.gptServContextText.insert(tk.END, data["gptContextGen"]["text"])
        else:
             self.gptServContextText.insert(tk.END, "Esse servico ainda nao possui um contexto gerado pelo ChatGPT")
        self.gptServContextText.config(state = tk.DISABLED)
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
        if not os.path.isfile(_config_file_path):
            with open(_config_file_path, 'w+') as f:
                f.write(defaultConfig)

    def readSavedConfigs(self):
        with open(_config_file_path) as f:
            self.savedConfig = json.load(f)
        
        if self.savedConfig['gptEnabled']: 
            if self.savedConfig['gptApiKey'] != '':
                new_state = "normal"
            else:
                new_state = "hidden"
        else:
            new_state = "hidden"
        self.notebook1.tab(4, state=new_state)
        self.notebook1.tab(5, state=new_state)
        
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

        self.guildSelComboBox['values']         = [i for i in values]
        self.contGuildSelComboBox['values']     = [i for i in valuesExisted]
        self.servGuildSelComboBox['values']     = [i for i in valuesExisted]
        self.gptGuildSelComboBox['values']      = [i for i in valuesExisted]
        self.gptServGuildSelComboBox['values']  = [i for i in valuesExisted]
        pass

    def on_close(self):
        response=messagebox.askyesno('Exit','Are you sure you want to exit?')
        if response:
            self.Gerador.destroy()
        pass

    def setCurrentComboBox(self):
        self.sizeComboBox.current(0)
        self.contractComboBox.current(0)
        self.sizeComboBox.current(0)
        self.themeComboBox.current(0)
        self.contGuildSelComboBox.current(0)
        self.serviceComboBox.current(0)
        self.guildSelComboBox.current(0)
        self.gptGuildSelComboBox.current(0)
        self.servGuildSelComboBox.current(0)
        self.gptServiceSelComboBox.current(0)
        self.gptContractSelComboBox.current(0)
        self.gptServGuildSelComboBox.current(0)
        pass

    def run(self):
        self.Gerador.protocol('WM_DELETE_WINDOW', self.on_close)
        self.setup()

        self.Gerador.tk.call('source', 'styles/Azure-ttk-theme/azure.tcl')

        self.setCurrentComboBox()
        self.readSavedConfigs()
        self.updateGuildList()

        #FILL size settlement
        with open("json4Names/guildSettlementSize.json", encoding="utf-8") as f:
            data = json.load(f)

        self.sizeComboBox['values'] = [data[str(i)]["name"] for i in data]

        self.mainwindow.mainloop()

def main():
    app = ContractviewerApp()
    app.run()

if __name__ == "__main__":
    main()