import common
from dice import diceRoll
import json
import guild
import time
from randomGuildNameGenerator import nameGen
from tkinter import *
import tkinter as tk

a='''
Criar um esquema de seed,ou seja, com um valor de seed é possivel obter sempre o mesmo resultado da geração de guilda
'''

f = open ("json4Names/guildSettlementSize.json")
dataSettlement = json.load(f)
settlement_selected = ''

class MyOptionMenu(tk.OptionMenu):
	def __init__(self, *args, **kw):
		self._command = kw.get("command")
		tk.OptionMenu.__init__(self, *args, **kw)
	def addOption(self, label):
		self["menu"].add_command(label=label,
		command=tk._setit(text_input_txt, label, self._command))

def geraGuilda():
	dice = diceRoll()

	guildCreator = guild.GuildMaker()
	diceResult = dice.roll(1,common.D6)%5
	if diceResult == 0:
		diceResult = 5

	#settlement = input_txt.get(1.0, "end-1c")
	for i in dataSettlement:
		if dataSettlement[str(i)]["name"] == text_input_txt.get():
			settlement = i
	try:
		settlement = int(settlement)
	except:
		return
	
	result = guildCreator.createGuild(settlement, isHuman.get())

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
	txt_guild.config(state = NORMAL)
	txt_guild.delete("1.0", "end")
	for k in display_info:
		txt_guild.insert(END, '{} = {}\n'.format(k,display_info[k]))
	txt_guild.config(state = DISABLED)

if __name__ == "__main__":
	window = Tk()
	window.title("Gerador de guilda")
	window.geometry('800x600')

	isHuman = BooleanVar()

	#text_input_txt = Label(window, text="Tamanho do assentamento 1-8")
	text_input_txt = StringVar()
	text_input_txt.set("Selecione o tamanho do assentamento")
	#text_input_txt.grid (column=0, row=0, padx=10, pady=10)
	#text_input_txt.pack()

	drop = MyOptionMenu(window, text_input_txt, "Selecione o tamanho do assentamento")

	for i in dataSettlement:
		drop.addOption (label=dataSettlement[str(i)]["name"])
	drop.pack()
	#input_txt = Text(window, height=1, width=5)
	#input_txt.grid(column=0, row=1, padx=10, pady=10)
	#input_txt.pack()

	input_human_checkbox = Checkbutton(window, text="Assentamento Humano?", variable=isHuman, onvalue=True, offvalue=False)
	#input_human_checkbox.grid (column=3, row=1, padx=10, pady=10)
	input_human_checkbox.pack()

	text_button = Label(window, text="Clique no botao e gere a guilda")
	#text_button.grid (column=1, row=2, padx=10, pady=10)
	text_button.pack()

	button_button = Button(window, text="Gerar", command=geraGuilda)
	#button_button.grid(column=1, row=3, padx=10, pady=10)
	button_button.pack()

	txt_guild = Text(window)
	#txt_guild.grid (column=0, row=4, padx=10, pady=10)
	txt_guild.pack()

	window.mainloop()