import nxppy
import os
from xml.dom import minidom

class NFC:
	def __init__(self,data_file,pi_file):
		self.data=data_file
		self.pi=pi_file
		self.people=self.LoadPeople()
		self.achievements=self.LoadPi()
		
	def Load(self,file,type):
		if os.path.exists(file):
			source=open(file)
			try:
				dom1=minidom.parse(source)
			except:
				impl=minidom.getDOMImplementation()
				dom1=impl.createDocument(None,type,None)
			return dom1
		else:
			impl=minidom.getDOMImplementation()
			doc=impl.createDocument(None, type,None)
			return doc
	def LoadPi(self):
		dom=self.Load(self.pi,"piSyst")
		try:
			pi_tag=dom.getElementsByTagName("pi")[0]
		except:
			self.SavePi()
			dom=self.Load(self.pi,"piSyst")
			pi_tag=dom.getElementsByTagName("pi")[0]
		a_tags=pi_tag.getElementsByTagName("achievement")
		achievements={}
		achievements[pi_tag.getAttribute("ID")]={"question":None,"answers":None}
		for a in a_tags:
			id=a.getAttribute("ID")
			qtag=a.getElementsByTagName("question")[0]
			question=qtag.childNodes[0].data
			atag=a.getElementsByTagName("answer")
			answers=[]
			for a in atag:
				answers.append(a.childNodes[0].data)
			achievements[id]={"question":question,"answers":answers}
		return achievements
		
	def SavePi(self):
		dom=self.Load(self.pi,"piSyst")
		top=dom.documentElement
		if(len(dom.getElementsByTagName("pi"))==0):
			pi=dom.createElement("pi")
			pi.setAttribute("ID","0")
			top.appendChild(pi)
		else:
			pitag=dom.getElementsByTagName("pi")[0]
			for id,a in self.achievements.iteritems():
				if a["question"]!=None:
					a=dom.createElement("achievement")
					a.setAttribute("ID",id)
					q=dom.createElement("question")
					text=dom.createTextNode(a["question"])
					q.appendChild(text)
					a.appendChild(q)
					for answer in a["answers"]:
						ans=dom.createElement("answer")
						txt=dom.createTextNode(txt)
						ans.appendChild(txt)
						a.appendChild(ans)
					pitag.appendChild(a)
		file=open(self.pi,'w')
		dom.writexml(file)
	def AddAchievement(self,id,question,answers):
		if id not in self.achievements.keys():
			self.achievements[id]={"question":question,"answers":answers}
		else:
			print "ERROR! achievement ID already in DB"
	def LoadPeople(self):
		dom=self.Load(self.data,"people")
		#f=open(self.data,'w')
		#print dom.savexml(f)
		people_tags=dom.getElementsByTagName("person")
		people={}
		for p in people_tags:
			id=p.getAttribute("ID")
			name_tag=p.getElementsByTagName("name")[0]
			name=name_tag.childNodes[0].data
			achievements_tags=p.getElementsByTagName("achievement")
			achievements=[]
			for a in achievements_tags:
				i=a.childNodes[0].data
				achievements.append(i)
			people[id]={"name":name,"achievements":achievements}
		return people
			
	
	def Read(self):
		uid=nxppy.read_mifare()
		p=None
		if uid not in self.people:
			name=raw_input('Please enter your name:')
			self.people[uid]={"name":name,"achievements":[]}
		for id, a in self.achievements.iteritems():
			if id not in self.people[uid]["achievements"]:
				if a["question"] is None:
					self.people[uid]["achievements"].append(id)
					print "new pi achievement!"
				else:
					print a["question"]
					ans=[]
					for answer in range(len(a["answers"])):
						u_a=raw_input("Answer 1:")
						ans.append(u_a)
					corrects=0
					for answer in ans:
						for a in a["answers"]:
							if answer==a:
								print answer + " is correct!"	
								corrects+=1
								break
					print "correct answers: ", corrects
					if corrects==len(a["answers"]):
						print "you won achievement ", id
						self.people[uid]["achievements"].append(id)	
		self.WritePeople()
		return self.people[uid]
	def WritePeople(self):
		dom=self.Load(self.data,"people")
		top=dom.documentElement
		for id,p in self.people.iteritems():
			el=dom.createElement("person")
			el.setAttribute("ID",id)
			name=dom.createElement("name")
			name_txt=dom.createTextNode(p["name"])
			name.appendChild(name_txt)
			el.appendChild(name)
			for a in p["achievements"]:
				a_tag=dom.createElement("achievement")
				a_txt=dom.createTextNode(a)
				a_tag.appendChild(a_txt)
				el.appendChild(a_tag)
			top.appendChild(el)
		file=open(self.data,'w')
		dom.writexml(file)
