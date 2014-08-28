from nfc import NFC

self=NFC('pi.xml','http://pi-passport.azurewebsites.net/api/People','http://pi-passport.azurewebsites.net/api/Achievements','http://pi-passport.azurewebsites.net/api/Joins')
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
