import requests
from bs4 import BeautifulSoup

def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.fftcg
    return db

def add_card(db, cardname, cardnum):
    db.cards.insert({"cardname" : cardname, "cardnum" : cardnum, "store": "fftcgsingles.com"})

db = get_db()
response = requests.get("https://fftcgsingles.co.uk/collections/all")
html = response.text
soup = BeautifulSoup(html, 'html.parser')
liTag = soup.find(class_="pagination__text")
pagination = max([int(s) for s in liTag.text.split() if s.isdigit()])
page=2
while(page<= pagination):
	print("page " +str(page))
	response= requests.get("https://fftcgsingles.co.uk/collections/all?page="+str(page))
	html+=response.text
	page+=1
soup=BeautifulSoup(html, 'html.parser')
divTag = soup.find_all(class_="grid-view-item")

for tag in divTag:
	if tag.find('img')['alt'] and "-" in tag.find('img')['alt'] :
		name =tag.find('img')['alt']
		if "FOIL" in name:
			print("this is a foil")
		else:
			print(name)
			name.split(" ", 1)
			add_card(db, name[1], name[0])
			print(tag.find(class_="product-price__price").text)
			print(tag.find('a')['href'])
			print(tag.find('img')['src'])
			if tag.find(class_="product-price__sold-out"):
				print(tag.find(class_="product-price__sold-out"))
