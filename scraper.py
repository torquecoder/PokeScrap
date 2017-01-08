#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import sqlite3
import os.path


if os.path.exists("pokedex.db"):
	quit()

print('Loading data....')
conn = sqlite3.connect('pokedex.db')
c = conn.cursor()
c.execute('''CREATE TABLE POKETABLE

	(ENTRY INT PRIMARY KEY NOT NULL,
	NAME TEXT NOT NULL,
	TYPE TEXT NOT NULL,
	TOTAL INT NOT NULL,
	HP INT NOT NULL,
	ATTACK INT NOT NULL,
	DEFENCE INT NOT NULL,
	SPEED INT NOT NULL)''')

url = 'http://pokemondb.net/pokedex/all'
data = requests.get(url).text
soup = BeautifulSoup(data, "lxml")
table_rows = soup.findAll('tr')
del table_rows[0]

for tr in table_rows:

	mega_poke = tr.find('small')

	if not mega_poke:
		entry_number = tr.find('td', attrs = {'class': 'num cell-icon-string'})  
		anchors = tr.findAll('a')

		poke_name = anchors[0].text     # Pokemon name

		entry_number = int(entry_number.text) # Pokemon index

		poke_type = ''

		for types in anchors[1:]:
			poke_type += types.text + ' '

		poke_type = poke_type[:-1]    # Pokemon types

		total = tr.find('td', attrs = {'class': 'num-total'})
		total = int(total.text)    # Pokemon total stat

		stats = tr.findAll('td', attrs = {'class': 'num'})

		hp = int(stats[1].text)
		attack = int(stats[2].text)
		defence = int(stats[3].text)
		speed = int(stats[6].text)


		c.execute("INSERT INTO POKETABLE VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (entry_number, poke_name, poke_type, total, hp, attack, defence, speed))

		#print(entry_number, end=' ')	
		#print(poke_name, end=' ')
		#print(poke_type, end=' ')
		#print(total, end=' ')
		#print(hp, end=' ')
		#print(attack, end=' ')
		#print(defence, end=' ')
		#rint(speed)


conn.commit()
conn.close()	
print('Data loaded ! Now, you can use your personal Pokédex :)')		
