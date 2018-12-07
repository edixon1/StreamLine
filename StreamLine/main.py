# -*- coding: utf-8 -*-
from mainImports import *

#KV File initialization
Builder.load_file('BioticIndexMockup2.kv')

#Google Sheets initialization
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('bioticIndexes-f9a7692e8f9d.json',scope)
gc = gspread.authorize(credentials)
sh = gc.open('NC_Biotic_Indexes')

#SQLite db initialization
conn = sqlite3.connect('bioticIndex.db') 
c = conn.cursor()

#Contains methods in charge of interacting with google sheets
class gSheets():
	def newSiteSheet(self,siteName):  #Create new sheet
		sh.add_worksheet(title=siteName, rows="500", cols="2")

	def containsSheet(self,siteName): #Checks if sheet of a given name exists in google sheets project
		sheetList = sh.worksheets()
		for sheet in sheetList:
			if(sheet.title == siteName):
				return True
		return False

	def calcSampleSiteBioInd(self):  #todo
		siteName = App.get_running_app().siteTableName
		speciesList=[]
		bioIndList=[]
		bioIndDB = c.execute("SELECT bioticIndex FROM {}".format(siteName)).fetchall()
		

	def uploadSiteData(self,species,bioInd,siteName): #Updates/creates sheet for a given site
		if(gSheets().containsSheet(siteName)):
			worksheet = sh.worksheet(siteName)
		else:
			gSheets().newSiteSheet(siteName)
			worksheet = sh.worksheet(siteName)

		cell_list = worksheet.range("A1:A{}".format(len(species)))   #update species column
		for i,cell in enumerate(cell_list):
			cell.value = species[i]
		worksheet.update_cells(cell_list)
		cell_list = worksheet.range("B1:B{}".format(len(bioInd)))   #update biotic index column
		for i,cell in enumerate(cell_list):
			cell.value = bioInd[i]
		worksheet.update_cells(cell_list)



class SiteButton(ListItemButton):
	def setSiteFile(self,tableName):
		App.get_running_app().siteTableName = tableName


class SiteManagerScreen(Screen): 
	def currentSiteTables(self):
		with open('SITE_TABLES.txt') as f:
		    siteTables = f.readlines()
		siteTables = [x.strip() for x in siteTables] 
		return siteTables

	def refreshSiteList(self):
		self.available_sites.adapter.data.clear()
		self.available_sites.adapter.data.extend(self.currentSiteTables())

	def uploadSite(self):
		siteName = App.get_running_app().siteTableName
		speciesList=[]
		bioIndList=[]
		bioIndDB = c.execute("SELECT bioticIndex FROM {}".format(siteName)).fetchall()
		speciesDB = c.execute("SELECT species FROM {}".format(siteName)).fetchall()
		for i in range(len(speciesDB)):
			speciesList.append(speciesDB[i][0])
			bioIndList.append(bioIndDB[i][0])
		gSheets().uploadSiteData(speciesList,bioIndList,siteName)


		popup = Popup(title='Test popup', content=Label(text='Site Uploaded'),
			size_hint=(.3,.4))
		popup.open()

class NewSiteScreen(Screen):
	def newSite(self):
		tableName = self.site_input.text
		self.recordTable(tableName) 
		c.execute('CREATE TABLE IF NOT EXISTS {}(species VARCHAR(100), bioticIndex REAL)'.format(tableName))

	def recordTable(self,tableName):
		App.get_running_app().siteTableName = tableName
		siteFileString = "{}\n".format(tableName)
		f = open("SITE_TABLES.txt",'a')
		f.write(siteFileString)
		f.close()

	def clear_text(self):
		self.site_input.text = ''



class EnterSpeciesScreen(Screen): 
		def WriteSpecies(self):
			userInput = self.species_input.text.split(',')
			species = userInput[0]
			count = int(userInput[1])
			bioInd = c.execute("SELECT bioticIndex FROM"\
				" ncBioticIndexes WHERE species='{}'".format(species))
			bioInd = bioInd.fetchone()[0]*count
			c.execute("INSERT INTO {} (species, "\
				"bioticIndex) VALUES(?, ?)".format(App.get_running_app().siteTableName),(species,bioInd))
			conn.commit()

		def clear_text(self):
			self.species_input.text = ''


screen_manager = ScreenManager(transition=FadeTransition())
screen_manager.add_widget(SiteManagerScreen(name="site_manager"))
screen_manager.add_widget(NewSiteScreen(name="new_site"))
screen_manager.add_widget(EnterSpeciesScreen(name="enter_species"))

class BioticIndexApp(App):
	def build(self):
		return screen_manager

mockup = BioticIndexApp()
mockup.run()

				


	#-----------------To be Implemented------------------------
	# def currentLocation(self):  
	# 	try:
	# 		gps.configure(on_location=self.on_location)
	# 		gps.start()
	# 	except NotImplementedError:
	# 		popup = Popup(title="GPS Error",
	# 			content=Label(text="GPS support is not implemented on your platform")).open()
	# 		Clock.schedule_once(lambda d: popup.dismiss(),3)