from nfc import NFC

self=NFC('people.xml','pi.xml')
person=self.Read()
if person != None:
	print "Hello " + person["name"]
	print "you have collected ",len(person["achievements"])," achievements"
	for a in person["achievements"]:
		print a

