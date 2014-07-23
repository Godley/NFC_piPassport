from nfc import NFC

self=NFC('pi.xml','http://pipassport.azurewebsites.net/api/People','http://pipassport.azurewebsites.net/api/Achievements','http://pipassport.azurewebsites.net/api/Links')
person=self.Read()
if person != None:
	print "Hello " + person["name"]
	print "you have collected ",len(person["achievements"])," achievements"	
	for a in person["achievements"]:
		print "ID: ", a
		achievement=NFC.GetAchievement(ID)
		if "Description" in achievement.keys():
			print "Description: ", achievement['Description']