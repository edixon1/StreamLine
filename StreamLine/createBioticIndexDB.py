import gspread
import sqlite3
import os
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('bioticIndexes-f9a7692e8f9d.json',scope)

gc = gspread.authorize(credentials)

wks = gc.open('NC_Biotic_Indexes').sheet1

#print(wks.get_all_records())

data = wks.get_all_records()
species = []
bioticIndex=[]
for x in data:
	if(len(x['Species'])>0 and len(str(x['BioIndex']))>0):
		species.append(x['Species'])
		bioticIndex.append(x['BioIndex'])




#for x in range(len(species)):
	#print("{},{}".format(species[x],bioticIndex[x]))

conn = sqlite3.connect('bioticIndex.db')
c = conn.cursor()


c.execute('CREATE TABLE IF NOT EXISTS'\
' ncBioticIndexes(species VARCHAR(100),'\
' bioticIndex REAL)')



for x in range(len(species)):
	cur_species=species[x]
	cur_bioticIndex = bioticIndex[x]
	c.execute("INSERT INTO ncBioticIndexes (species, bioticIndex) VALUES (?, ?)",
			(cur_species,cur_bioticIndex))
	conn.commit()
c.close()
conn.close()

#print(c.fetchall())


#wks.append_row(['1st','2nd'])

#print(wks.acell('A2'))