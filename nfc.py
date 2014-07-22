import nxppy
import os
from xml.dom import minidom
import urllib
import urllib2
import os
import requests
import json

class NFC:
	def __init__(self,data_file,pi_file):
		self.ach_api='http://pipassport.azurewebsites.net/api/Achievements'
		self.people_api='http://pipassport.azurewebsites.net/api/People'
		self.link_api='http://pipassport.azurewebistes.net/api/Links'
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
				data={'ID':id,'Description':a['description']}
				header={'content-type':'application/json'}
				req=requests.post(self.achievements_api,json.dump(data),header}
		file=open(self.pi,'w')
		dom.writexml(file)
	def AddAchievement(self,question,answers,description):
		req=requests.get(self.achievements_api)
		try:
			ach=req.json()
			id=len(ach)-1
			
		except:
			id=0
		self.achievements[id]={"question":question,"answers":answers,"description":description}
		self.SavePi()
	def LoadPeople(self):
		req=requests.get(self.people_api)
		try:
			people_array=req.json()
			people = {}
			for p in people_array:
				people[p['ID']]={'name':p['Name'],'achievements':[]}
		except:
			people={}
		try:
			req2=requests.get(self.link_api)
			link_array=req2.json()
			for l in link_array:
				people[l['UID']]['achievements'].append(l['AID'])
		except:
			return people
		return people
			
	
	def Read(self):
		uid=nxppy.read_mifare()
		p=None
		if uid is None:
			return None
		if uid not in self.people:
			print "new ID :", uid
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
		for id,p in self.people.iteritems():
			values={'ID':id,'Name':p['name']}
			headers={'content-type':'application/json'}
			req=requests.post(os.path.join(self.people_api),data=json.dumps(values),headers=headers)
			print requests.get(self.people_api).json()
		
