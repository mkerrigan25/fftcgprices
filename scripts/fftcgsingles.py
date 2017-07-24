import requests
from bs4 import BeautifulSoup


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
	print(tag.find(class_="h4 grid-view-item__title").text)
	print(tag.find(class_="product-price__price").text)
	print(tag.find('a')['href'])
	print(tag.find('img')['src'])