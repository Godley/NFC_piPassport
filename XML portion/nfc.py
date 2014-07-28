import nxppy
import os,json,requests
from xml.dom import minidom

class NFC(object):
	def __init__(self,pifile,peoplefile):
		self.pi=pifile
		self.peoplef=peoplefile


		self.achievements=self.LoadPi()
		self.people=self.LoadPeople()

	def ReadCard(self):
		id=nxppy.read_mifare()
		if id == None:
			return None
		else:
			if id not in self.people.keys():
				print "new ID :", id
				name=raw_input('Please enter your name:')
				self.people[id]={"name":name,"achievements":[]}
			else:
				for aid in self.achievements.keys():
					if aid not in self.people[id]['achievements']:
						if self.achievements[aid]['question']==None:
							self.people[id]['achievements'].append(aid)
							print "Achievement unlocked!"
						else:
							print self.achievements[aid]['question']
							ans=[]
							for a in range(len(self.achievements[aid]['answers'])):
								answer=raw_input('Enter answer:')
								ans.append(answer)
							correct=0
							for an in range(len(ans)):
								found=False
								for answ in self.achievements[aid]['answers']:
									if answ==ans[an]:
										found=True
										break
								if not found:
									print "answer " + str(ans[an]) + " incorrect!"
								else:
									correct+=1
							if correct == len(self.achievements[aid]['answers']):
								print "achievement unlocked!"	
								self.people[id]['achievements'].append(aid)
			self.SavePeople()
			return self.people[id]
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
			for an in atag:
				answers.append(an.childNodes[0].data)
			achievements[id]={"question":question,"answers":answers}
		return achievements

	def SavePi(self):
		dom=self.Load(self.pi,"piSyst")
		top=dom.documentElement
		if(len(dom.getElementsByTagName("pi"))==0):
			pi=dom.createElement("pi")
			id=0
			pi.setAttribute("ID",str(id))
			top.appendChild(pi)
			file=open(self.pi,'w')
			dom.writexml(file)
		else:
			old_achievements=self.LoadPi()
			pitag=dom.getElementsByTagName("pi")[0]
			if old_achievements != self.achievements:
				try:
					os.remove(self.pi)
				except Exception, e:
					print str(e)
					pass
				dom=self.Load(self.pi,"piSyst")
				top=dom.documentElement
				pitag=dom.createElement("pi")
				id=0
				pitag.setAttribute("ID",str(id))
				top.appendChild(pitag)
				for id,a in self.achievements.iteritems():
					if a["question"]!=None:
						ac=dom.createElement("achievement")
						ac.setAttribute("ID",id)
						q=dom.createElement("question")
						text=dom.createTextNode(str(a["question"]))
						q.appendChild(text)
						ac.appendChild(q)
						for answer in a["answers"]:
							ans=dom.createElement("answer")
							txt=dom.createTextNode(str(answer))
							ans.appendChild(txt)
							ac.appendChild(ans)
					pitag.appendChild(ac)
				file=open(self.pi,'w')
				dom.writexml(file)
	
	def LoadPeople(self):
		dom=self.Load(self.peoplef,"People")
		p_tags=dom.getElementsByTagName("person")
		people={}
		for p in p_tags:
			id=p.getAttribute("ID")
			ntag=p.getElementsByTagName("name")[0]
			name=ntag.childNodes[0].data
			atag=p.getElementsByTagName("achievement")
			achievements=[]
			for a in atag:
				if a.childNodes[0].data not in achievements:
					achievements.append(a.childNodes[0].data)
			people[id]={"name":name,"achievements":achievements}
		return people

	def SavePeople(self):
		dom=self.Load(self.peoplef,"People")
		top=dom.documentElement
		old_p=self.LoadPeople()
		people_tags=top.getElementsByTagName("person")
		for id,p in self.people.iteritems():
			if id in old_p.keys():
					for pe in people_tags:
						if pe.getAttribute("ID")==id:
							for achievement in p["achievements"]:
								if achievement not in old_p[id]["achievements"]:
									ac_tag=dom.createElement("achievement")
									ac_text=dom.createTextNode(achievement)
									ac_tag.appendChild(ac_text)
									pe.appendChild(ac_tag)
			else:
				peep=dom.createElement("person")
				peep.setAttribute("ID",id)
				n=dom.createElement("name")
				text=dom.createTextNode(str(p["name"]))
				n.appendChild(text)
				peep.appendChild(n)
				for achievement in p["achievements"]:
					ac=dom.createElement("achievement")
					txt=dom.createTextNode(str(achievement))
					ac.appendChild(txt)
					peep.appendChild(ac)
				top.appendChild(peep)
		file=open(self.peoplef,'w')
		dom.writexml(file)


	def AddAchievement(self,desc,question,answers):
		ids=[int(i) for i in self.achievements.keys()]
		sorted_ids=sorted(ids)
		id=sorted_ids[-1]+1
		self.achievements[str(id)]={"question":question,"answers":answers,"Description":desc}
		self.SavePi()
	
	def UpdateAchievement(self,updated_entry):
		if id in self.achievements.keys():
			self.achievements[id]=updated_entry
		else:
			print "Achievement not found"

	def DeleteAchievement(self,id):
		if id in self.achievements.keys():
			del self.achievements[id]
		else:
			print "Achievement not found"

	def GetAchievement(self, id):
		if id in self.achievements.keys():
			return self.achievements[id]
		else:
			return None
