import requests, re
from bs4 import BeautifulSoup

def get_db():
    from pymongo import MongoClient
    client = MongoClient('mongodb://fftcgscript:nextat765@ds161022.mlab.com:61022/fftcg')
    #client = MongoClient('localhost:27017')
    db = client.fftcg
    return db

def add_card(db, cardnum, price, link, instock, foil=False):
	cardtype = "nonfoil"
	if foil:
		cardtype = "foil"
	db.cards.find_and_modify({"cardnum": cardnum, "stores": {"$elemMatch": {"_id": "trollandtoad.com"}}},{"$set": {"stores.$."+cardtype+".price" : price, "stores.$."+cardtype+".link": link, "stores.$."+cardtype+".instock": instock}} )

db = get_db()
response = requests.get("http://www.trollandtoad.com/Force-of-Will-and-Other-CCGs/10283.html?orderBy=Alphabetical+A-Z&filterKeywords=&sois=Yes&minPrice=&maxPrice=&pageLimiter=10000&showImage=Yes")
html = response.text
soup = BeautifulSoup(html, 'html.parser')
divTag = soup.find_all(class_="cat_result_wrapper")

for tag in divTag:
	imgTag = tag.find(class_="cat_result_image_wrapper")
	title = imgTag.find('img')['alt']
	if len(title.split(" - ")) > 1:
		cardname, cardnum, rarity = title.split(" - ")
		if cardnum[-1].isdigit():
			cardnum = cardnum + rarity[0]
		try:
			cardnum = re.findall(r'[0-9]-[0-9]{3}[A-Z]', cardnum)[0]
		except IndexError:
			cardnum = re.findall(r'[A-Z]{2}-[0-9]{3}', cardnum)[0]
		print cardnum
		if "Foil" in title.split(" - ")[2]:
			add_card(db, cardnum, tag.find(class_="price_text").text, imgTag.find('a')['href'], tag.find(class_="quantity_text").text > 0, True)
		else:
			add_card(db, cardnum, tag.find(class_="price_text").text, imgTag.find('a')['href'], tag.find(class_="quantity_text").text > 0)
			#print(imgTag.find('img')['alt'])
			#print(imgTag.find('a')['href'])
			#print(imgTag.find('img')['src'])
			#print(tag.find(class_="quantity_text").text)
			#print(tag.find(class_="price_text").text)
		