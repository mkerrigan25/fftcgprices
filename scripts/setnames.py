import requests, re
from bs4 import BeautifulSoup

def get_db():
    from pymongo import MongoClient
    client = MongoClient('mongodb://fftcgscript:nextat765@ds161022.mlab.com:61022/fftcg')
	#client = MongoClient('localhost:27017')
    db = client.fftcg
    return db

def add_card(db, cardname, cardnum):
    db.cards.update(
    	{"cardnum" : cardnum},
	    	{"$set": 
	    		{"cardname" : cardname, 
	    		"cardnum" : cardnum, 
	    		"stores" : [
	    			{ "_id" : "trollandtoad.com" },
	    			{ "_id" : "fftcgsingles.co.uk" }
	    		]
	    	} 
	    }, upsert=True)

db = get_db()
response = requests.get("http://final-fantasy-card-game.wikia.com/wiki/Opus_I_Collection")
#response = requests.get("http://final-fantasy-card-game.wikia.com/wiki/Opus_II_Collection")
#response = requests.get("http://final-fantasy-card-game.wikia.com/wiki/Opus_III_Collection")

html = response.text
soup = BeautifulSoup(html, 'html.parser')
rows = soup.find_all("tr")

for row in rows:
	if len(row) > 10:
		cols = row.find_all('td')
		if len(cols) > 0:
			print cols[0].string, cols[1].string[:-8]
			add_card(db, cols[1].string[:-8], cols[0].string)