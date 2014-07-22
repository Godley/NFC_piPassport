from nfc import NFC
import random
class Manage(object):
	def __init__(self):
		self.data=NFC('people.xml','pi.xml')
		self.achievements=self.data.achievements
	
	def View(self):
		for id,a in self.achievements.iteritems():
			print "ID: ", id
			print "Question: ", a["question"]
			if a["answers"]!=None:
				for answer in a["answers"]:
					print "Answer: ",answer
	def ViewOne(self,id):
		if id in self.achievements.keys():
			print "ID: ", id
			print "Question: ", self.achievements[id]["question"]
			for answer in self.achievements[id]["answers"]:
				print "Answer: ",answer
			return True
		else:	
			print "achievement not found"
			return False	

	def Edit(self,id,new_q,answers):
		if id in self.achievements.keys():
			self.achievements[id]["question"]=new_q
			self.achievements[id]["answers"]=answers
			print "updated"
		else:
			print "achievement not found"
	def Delete(self,id):
		if id in self.achievements.keys():
			self.achievements.pop(id,0)
		else:
			print "achievement not found"

	def Add(self,question,answers,desc):
		self.data.AddAchievement(question,answers,desc)
 

class UI(object):
	def __init__(self):
		self.mng=Manage()

	def AddAch(self):
		a_count=raw_input('Enter number of achievements:')
		count=int(a_count)
		for i in range(count):
			desc=raw_input('Enter description:')
			q=raw_input('Enter question:')
			an_count=raw_input('Enter number of answers:')
			c=int(an_count)
			answers=[]
			for i in range(c):
				an=raw_input('Enter Answer:')
				answers.append(an)
			self.mng.Add(q,answers,desc)		
			
	def View(self):
		self.mng.View()
	def Delete(self):
		id=int(raw_input('Enter ID:'))
		self.mng.Delete(id)
	def Edit(self):
		id=int(raw_input('Enter ID:'))
		res=self.mng.ViewOne(id)
		if res:
			desc=raw_input('New description:')
			q=raw_input('New question:')
			ans=int(raw_input('number of answers:'))
			answers=[]
			for a in range(ans):
				answer=raw_input('answer:')
				answers.append(answer)
			self.mng.Edit(id,q,answers)
	def Menu(self):
		inp=-1
		while self.InvalidInput(inp):
			print "welcome to pi pass admin"
			print "1. View achievements"
			print "2. Add achievements"
			print "3. Edit achievements"
			print "4. Delete achievements"
			print "5. Quit"
			inp=int(raw_input('Enter choice:'))
			if inp==5:	
				break
			else:
				cats={1:self.View,2:self.AddAch,3:self.Edit,4:self.Delete}
				cats[inp]()
	def InvalidInput(self,input):
		if 0<input<6:
			return False
		else:
			return True

self=UI()
self.Menu()

