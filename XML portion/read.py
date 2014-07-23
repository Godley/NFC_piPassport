from nfc import NFC

self=NFC('pi.xml','people.xml')
person=self.ReadCard()
if person != None:
	print "Hello " + person["name"]
	print "you have collected ",len(person["achievements"])," achievements"	
	for a in person["achievements"]:
		print "ID: ", a
		achievement=self.GetAchievement(a)
		if "Description" in achievement.keys():
			print "Description: ", achievement['Description']
