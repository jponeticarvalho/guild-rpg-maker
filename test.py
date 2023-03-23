#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class ContractviewerApp:
    def __init__(self, master=None):
        # build ui
        self.Gerador = tk.Tk() if master is None else tk.Toplevel(master)
        self.Gerador.configure(height=600, padx=10, pady=10, width=800)
        self.Gerador.resizable(False, False)
        notebook1 = ttk.Notebook(self.Gerador)
        notebook1.configure(height=680, width=820)
        self.guildFrame = ttk.Frame(notebook1)
        self.guildFrame.configure(height=200, width=200)
        frame3 = ttk.Frame(self.guildFrame)
        frame3.configure(height=200, width=200)
        self.sizeComboBox = ttk.Combobox(frame3)
        self.sizeStrVar = tk.StringVar()
        self.sizeComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.sizeStrVar,
            values='Selecione o Tamanho do assentamento',
            width=40)
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
            values='Selecione uma guilda para vizualização',
            width=50)
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
        notebook1.add(self.guildFrame, text='Gerar Guilda')
        self.contractFrame = ttk.Frame(notebook1)
        self.contractFrame.configure(height=200, width=200)
        self.contGuildSelComboBox = ttk.Combobox(self.contractFrame)
        self.contGuildSelComboBoxVar = tk.StringVar()
        self.contGuildSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.contGuildSelComboBoxVar,
            values='Selecione uma guilda para vizualização',
            width=50)
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
            values='Contratos',
            width=40)
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
        notebook1.add(self.contractFrame, text='Gerar Contrato')
        self.serviceFrame = ttk.Frame(notebook1)
        self.serviceFrame.configure(height=200, width=200)
        self.servGuildSelComboBox = ttk.Combobox(self.serviceFrame)
        self.servGuildSelComboBoxVar = tk.StringVar()
        self.servGuildSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.servGuildSelComboBoxVar,
            values='Selecione uma guilda para vizualização',
            width=50)
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
            values='Serviços',
            width=40)
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
        notebook1.add(self.serviceFrame, text='Gerar Servico')
        self.themeFrame = ttk.Frame(notebook1)
        self.themeFrame.configure(height=200, width=200)
        self.chatGPTApiKeyEntry = ttk.Entry(self.themeFrame)
        self.chatGPTApiKeyVar = tk.StringVar(value='asdasd')
        self.chatGPTApiKeyEntry.configure(
            textvariable=self.chatGPTApiKeyVar, width=50)
        _text_ = 'asdasd'
        self.chatGPTApiKeyEntry.delete("0", "end")
        self.chatGPTApiKeyEntry.insert("0", _text_)
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
        self.themeComboBox.configure(values='dark light')
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
        notebook1.add(self.themeFrame, text='Configuraçoes')
        self.frame14 = ttk.Frame(notebook1)
        self.frame14.configure(height=200, width=200)
        self.gptGuildSelComboBox = ttk.Combobox(self.frame14)
        self.gptGuildSelComboBoxVar = tk.StringVar()
        self.gptGuildSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.gptGuildSelComboBoxVar,
            values='Selecione uma guilda para vizualização',
            width=50)
        self.gptGuildSelComboBox.grid(column=0, padx=20, pady=10, row=0)
        self.gptGuildSelComboBox.bind(
            "<<ComboboxSelected>>", self.gptGuildSelectCb, add="")
        frame15 = ttk.Frame(self.frame14)
        frame15.configure(height=200, width=200)
        self.gptContractSelComboBox = ttk.Combobox(frame15)
        self.gptContractSelComboBoxVar = tk.StringVar()
        self.gptContractSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.gptContractSelComboBoxVar,
            values='Contratos',
            width=40)
        self.gptContractSelComboBox.grid(column=0, padx=20, row=0)
        self.gptContractSelComboBox.bind(
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
        notebook1.add(
            self.frame14,
            state="hidden",
            text='Gerar Contrato ChatGPT')
        self.frame1 = ttk.Frame(notebook1)
        self.frame1.configure(height=200, width=200)
        self.gptServGuildSelComboBox = ttk.Combobox(self.frame1)
        self.gptServGuildSelComboBoxVar = tk.StringVar()
        self.gptServGuildSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.gptServGuildSelComboBoxVar,
            values='Selecione uma guilda para vizualização',
            width=50)
        self.gptServGuildSelComboBox.grid(column=0, padx=20, pady=10, row=0)
        self.gptServGuildSelComboBox.bind(
            "<<ComboboxSelected>>", self.gptServGuildSelectCb, add="")
        frame2 = ttk.Frame(self.frame1)
        frame2.configure(height=200, width=200)
        self.gptServiceSelComboBox = ttk.Combobox(frame2)
        self.gptServiceSelComboBoxVar = tk.StringVar()
        self.gptServiceSelComboBox.configure(
            height=10,
            state="readonly",
            textvariable=self.gptServiceSelComboBoxVar,
            values='Contratos',
            width=40)
        self.gptServiceSelComboBox.grid(column=0, padx=20, row=0)
        self.gptServiceSelComboBox.bind(
            "<<ComboboxSelected>>", self.gptServiceSelectorCb, add="")
        self.createServiceContextBtn = ttk.Button(frame2)
        self.createServiceContextBtn.configure(text='Gerar Contexto', width=25)
        self.createServiceContextBtn.grid(column=1, padx=20, row=0)
        self.createServiceContextBtn.configure(
            command=self.createServiceContextBtnCb)
        frame2.grid(column=0, pady=5, row=1)
        self.gptServContextText = tk.Text(self.frame1)
        self.gptServContextText.configure(height=35, width=100)
        self.gptServContextText.grid(column=0, padx=8, pady="0 3", row=2)
        label2 = ttk.Label(self.frame1)
        label2.configure(text='powered by twitch.tv/Owneti')
        label2.grid(column=0, row=3)
        self.frame1.pack(side="top")
        notebook1.add(
            self.frame1,
            state="hidden",
            text='Gerar Servico ChatGPT')
        notebook1.grid()
        self.Gerador.grid_anchor("center")

        # Main widget
        self.mainwindow = self.Gerador

    def run(self):
        self.mainwindow.mainloop()

    def createGuildBtnCb(self):
        pass

    def guildSelectCb(self, event=None):
        pass

    def contractGuildSelectCb(self, event=None):
        pass

    def contractSelectorCb(self, event=None):
        pass

    def createContractBtnCb(self):
        pass

    def serviceGuildSelectCb(self, event=None):
        pass

    def serviceSelectorCb(self, event=None):
        pass

    def createServiceBtnCb(self):
        pass

    def saveConfigBtnCb(self):
        pass

    def restoreConfigBtnCb(self):
        pass

    def deleteNonExistGuildBtnCb(self):
        pass

    def gptGuildSelectCb(self, event=None):
        pass

    def gptContractSelectorCb(self, event=None):
        pass

    def createContractContextBtnCb(self):
        pass

    def gptServGuildSelectCb(self, event=None):
        pass

    def gptServiceSelectorCb(self, event=None):
        pass

    def createServiceContextBtnCb(self):
        pass


if __name__ == "__main__":
    app = ContractviewerApp()
    app.run()
