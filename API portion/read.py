from nfc import NFC

self=NFC('pi.xml','http://pipassport.azurewebsites.net/api/People','http://pipassport.azurewebsites.net/api/Achievements','http://pipassport.azurewebsites.net/api/Links')
person=self.ReadCard()
if person != None:
	print "Hello " + person["name"]
	print "you have collected ",len(person["achievements"])," achievements"	
	for a in person["achievements"]:
		print "ID: ", a
		achievement=self.GetAchievement(a)
		if achievement is not None:
			if "Description" in achievement.keys():
				print "Description: ", achievement['Description']
