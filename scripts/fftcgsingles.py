import requests
import os
import urllib.request
from bs4 import BeautifulSoup

def get_db():
    from pymongo import MongoClient
    client = #db stuff
    db = client.fftcg
    return db

def add_card(db, cardname, cardnum, price, link, instock, foil=False):
	cardname= cardname.replace("FOIL", "")
	cardtype = "nonfoil"
	if foil:
		cardtype = "foil"
	if db.cards.find({"cardnum":cardnum}).count() ==0:
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
	
	db.cards.update({"cardnum": cardnum, "stores": {"$elemMatch": {"_id": "fftcgsingles.co.uk"}}},{"$set": {"stores.$."+cardtype+".price" : price, "stores.$."+cardtype+".link": link, "stores.$."+cardtype+".instock": instock}}, upsert=True )
db = get_db()
response = requests.get("https://fftcgsingles.co.uk/collections/all")
html = response.text
soup = BeautifulSoup(html, 'html.parser')
liTag = soup.find(class_="pagination__text")
pagination = max([int(s) for s in liTag.text.split() if s.isdigit()])
page=2
while(page<= pagination):
	response= requests.get("https://fftcgsingles.co.uk/collections/all?page="+str(page))
	html+=response.text
	page+=1
soup=BeautifulSoup(html, 'html.parser')
divTag = soup.find_all(class_="grid-view-item")

for tag in divTag:
	if tag.find('img')['alt'] and "-" in tag.find('img')['alt'] :
		name =tag.find('img')['alt']
		foil = False
		if "FOIL" in name:
			foil = True
		instock = True
		if tag.find(class_="product-price__sold-out"):
			instock = False
		name=name.split(" ", 1)
		
		filename=os.path.join("static/images/",name[0]+".jpg")
		if not os.path.exists(filename):
			imgUrl = tag.find('img')['src']
			urllib.request.urlretrieve("https:"+imgUrl, filename)
		
		add_card(db, name[1], name[0], tag.find(class_="product-price__price").text, tag.find('a')['href'], instock, foil)
		#print(tag.find(class_="product-price__price").text)
		#print(tag.find('a')['href'])
		#print(tag.find('img')['src'])
