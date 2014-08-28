import nxppy
import os,json,requests
from xml.dom import minidom
class NFC(object):
	def __init__(self,pifile,people_url,pi_url,link_url):
		self.pi=pifile
		self.pi_url=pi_url
		self.people_api=people_url
		self.link_api=link_url

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
					if int(aid) not in self.people[id]['achievements']:
						if self.achievements[aid]['question']==None:
							self.people[id]['achievements'].append(aid)
							print "Achievement unlocked!"
						else:
							print "Achievement available: answer the following question to win "+self.achievements[aid]["Description"]+":"
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
									print "answer "+ans[an]+" incorrect!"
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
			
		a_q=requests.get(self.pi_url)
		a_data=a_q.json()
		a_dict={}
		for a in a_data:
			a_dict[a["ID"]]={"Description":a["Description"]}
		pid=pi_tag.getAttribute("ID")
		a_tags=pi_tag.getElementsByTagName("achievement")
		achievements={}
		if int(pid) in a_dict.keys():
			achievements[pid]={"question":None,"answers":None,"Description":a_dict[int(pid)]["Description"]}
		else:
			desc=raw_input("Please enter a description for this pi:")
			post=requests.post(self.pi_url,data=json.dumps({"Description":desc}),headers={"Content-type":"application/json"})
			id=str(int(post.json()["ID"])-1)
			
			achievements[id]={"question":None,"answers":None,"Description":desc}
			pi_tag.setAttribute("ID",str(id))
			file=open(self.pi,'w')
			dom.writexml(file)
		a_q=requests.get(self.pi_url)
		a_data=a_q.json()
		a_dict={}
		for a in a_data:
			a_dict[a["ID"]]={"Description":a["Description"]}
		for a in a_tags:
			id=a.getAttribute("ID")
			qtag=a.getElementsByTagName("question")[0]
			question=qtag.childNodes[0].data
			atag=a.getElementsByTagName("answer")
			answers=[]
			for an in atag:
				answers.append(an.childNodes[0].data)
			achievements[id]={"question":question,"answers":answers,"Description":a_dict[id]["Description"]}
			
		return achievements

	def SavePi(self):
		achievement_q=requests.get(self.pi_url)
		a_data=achievement_q.json()
		a_dict={}
		for entry in a_data:
			a_dict[entry["ID"]]={"Description":entry["Description"]}
		dom=self.Load(self.pi,"piSyst")
		top=dom.documentElement
		if(len(dom.getElementsByTagName("pi"))==0):
			st=raw_input('Please enter a description for this pi:')
			tag=dom.createElement("pi")
			keys=[int(item) for item in a_dict.keys()]
			if len(keys)!=0:
				print "hey1"
				tag.setAttribute("ID",str(max(keys)+1))
			else:
				print "hey"
				tag.setAttribute("ID",str(0))
			request=requests.post(self.pi_url,data=json.dumps({"Description":st}),headers={"Content-type":"application/json"})
			id=request.json()['ID']
			tag.setAttribute("ID",str(int(id)))
			top.appendChild(tag)
		else:
			pitag=dom.getElementsByTagName("pi")[0]
			for id,a in self.achievements.iteritems():								
				if a["question"]!=None:
					ac=dom.createElement("achievement")
					ac.setAttribute("ID",str(id))
					q=dom.createElement("question")
					text=dom.createTextNode(str(a["question"]))
					q.appendChild(text)
					ac.appendChild(q)
					for answer in a["answers"]:
						ans=dom.createElement("answer")
						txt=dom.createTextNode(str(answer))
						ans.appendChild(txt)
						ac.appendChild(ans)
					if id not in a_dict.keys():
						request=requests.post(self.pi_url,data=json.dumps({"Description":a["Description"]}),headers={"Content-type":"application/json"})
						new_id=request.json()["ID"]
						if int(new_id) != id:
							ac.setAttribute("ID",new_id)
					pitag.appendChild(ac)
			for id in a_dict.keys():
				if id not in self.achievements.keys():
					r=requests.delete(os.path.join(self.pi_url,id),headers={"Content-type":"application/json"})
		file=open(self.pi,'w')
		dom.writexml(file)
	
	def LoadPeople(self):
		get=requests.get(self.people_api)
		data=None
		people={}
		try:
			data=get.json()
			for item in data:
				people[item["ID"]]={"name":item["Name"],"achievements":[]}
		except:
			return people
		try:
			get=requests.get(self.link_api)
			j=get.json()
			for item in j:
				if item["UID"] in people.keys():
					if item["AID"] not in people[item["UID"]]['achievements']:
						people[item["UID"]]["achievements"].append(item["AID"])
			return people
		except:
			return people

	def SavePeople(self):
		h={"Content-type":"application/json"}
		link=requests.get(self.link_api)
		linkdata=link.json()
		ld={}
		for item in linkdata:
			if item["UID"] not in ld.keys():
				ld[item["UID"]]=[]
				ld[item["UID"]].append(item["AID"])
			else:
				ld[item["UID"]].append(item["AID"])
		for id,p in self.people.iteritems():
			request=requests.get(os.path.join(self.people_api,id))
			try:
				js=request.json()
				data={"Name":p["name"]}
				r=requests.put(os.path.join(self.people_api,id),data=json.dumps(data),headers=h)
			except:
				data={"ID":id,"Name":p["name"]}
				r=requests.post(self.people_api,data=json.dumps(data),headers=h)
			if id not in ld.keys():
				for a in p["achievements"]:
					data={"AID":a,"UID":id}
					pr=requests.post(self.link_api,data=json.dumps(data),headers=h)
			else:
				for a in p["achievements"]:
					if a not in ld[id]:
						data={"AID":a,"UID":id}
						pr=requests.post(self.link_api,data=json.dumps(data),headers=h)


	def AddAchievement(self,desc,question,answers):
		id=self.achievements.keys()[-1]+1
		self.achievements[id]={"question":question,"answers":answers,"Description":desc}
		self.SavePi()
	
	def UpdateAchievement(self,updated_entry):
		if id in self.achievements.keys():
			self.achievements[id]=updated_entry
			self.SavePi()
		else:
			print "Achievement not found"
		
	def DeleteAchievement(self,id):
		if id in self.achievements.keys():
			del self.achievements[id]
			self.SavePi()
		else:
			print "Achievement not found"

	def GetAchievement(self, id):
		if id in self.achievements.keys():
			return self.achievements[id]
		else:
			return None
