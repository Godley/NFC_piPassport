from nfc import NFC

class UI(object):
	def __init__(self,pi,people):
		self.NFC=NFC(pi,people)
		self.CRUD={1:self.View,2:self.Create,3:self.Update,4:self.Delete,5:self.Quit}
	
	

	def Menu(self):
		print "Welcome to xyz admin."
		print "1. View Achievements"
		print "2. Add Achievements"
		print "3. Update Achievements"
		print "4. Remove Achievements"
		print "5. Quit"
		valid=False
		while not valid:
			input=raw_input('Enter an option:')
			validate=self.ValidateChoice(input)
			if validate == True:
				valid=True
			else:
				print validate
		self.CRUD[int(input)]()

	def View(self):
		input=raw_input('Display all achievements? (y/n)')
		if input.lower()=='y':
			entries=self.NFC.achievements
			for id, a in entries:
				print "ID: ", id
				for id, entry in a:
					print id, ": ", entry
		else:
			id=self.ProcessEntry('Achievement ID')
			entry=self.NFC.GetAchievement(id)
			if entry is None:
				print "Achievement not found"
				else:
					for id, e in entry:
						print id, " : ", e


	def Create(self):
		id=self.ProcessEntry('number of achievements')
		for i in range(id):
			desc=raw_input('Achievement description:')
			question=raw_input('Question:')
			vint=False
			ansint=self.ProcessEntry('number of answers')
			answers=[]
			for i in range(ansint):
				answer=raw_input('Enter answer '+i+':')
				answers.append(answer)
			self.NFC.AddAchievement(desc,question,answers)

	def Update(self):
		id=self.ProcessEntry('Achievement ID')
		entry=self.NFC.GetAchievement(id)
		new_e={}
		if entry is not None:
			for id in entry.keys():
				update=raw_input('Enter update for '+id+': ')
				new_e[id]=update
			self.NFC.UpdateAchievement(entry)
			print "Update successful!"
		else:
			print "Update failed"
				
	def Delete(self):
		id=self.ProcessEntry('Achievement ID')
		entry=self.NFC.GetAchievement(id)
		for id, e in entry.iteritems():
			print id, ":", e
		yn=raw_input('Confirm delete? (y/n)')
		if yn.lower()=='y' or yn.lower()=="yes":
			self.NFC.DeleteAchievement(id)
		else:
			return None

	def Quit(self):
		return None

	def ValidateChoice(self,item):
		inte=self.ValidateInt(item)
		if not inte:
			return "Entry not an integer"

		if int(item) not in self.CRUD.keys():
			return str(item)+ " not in list"
		else:
			return True
	
	def ValidateInt(self,item):
		try:
			val=int(item)
			return True
		except:
			return False
	def ProcessEntry(self,string):
		valid=False
		while not valid:
			id=raw_input('Please enter a valid ' +string+ ': ')
			valid=self.ValidateInt(id)
			if not valid:
				print "Invalid number"
		return int(id)

self=UI('pi.xml','http://pipassport.azurewebsites.net/api/People','http://pipassport.azurewebsites.net/api/Achievements','http://pipassport.azurewebsites.net/api/Links')
self.Menu()