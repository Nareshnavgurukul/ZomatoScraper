from bs4 import BeautifulSoup
import requests,os,json
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.zomato.com/ncr")
response = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()
soup = BeautifulSoup(response,"lxml")
Task1 = soup.find("div",{"class":"ui segment row"})
all_a = Task1.find_all("a")


def locaLitiesURL():
	URLS = []
	for a in all_a:
		url = a["href"]
		URLS.append(url)#getting urls of Localities
	return(URLS)
allURL = locaLitiesURL()

#Task 1
def locRest():
	if os.path.exists("Task1/zomato.json"):
		with open("Task1/zomato.json","r") as file:
			read = file.read()
			Localities = json.loads(read)
			return Localities

	Localities = {}
	for a in (all_a):
		nameLoca = a.get_text()
		name  = nameLoca.split()[:-2]#list of all a tag content 
		cmlname = " ".join(name)
		Localities[cmlname] = {"Total restaurant":a.find("span").get_text()[1:-1]}#removing "()"
	with open("Task1/zomato.json","w") as file:
		read = json.dumps(Localities)
		file.write(read)
		file.close()
	return(Localities)
locRest()
# Task 2

ef task2(all_url):
	for url in all_url:#urls of Localities
		nameoflocal = url[27:-12]
		filename = nameoflocal
		if os.path.exists("Task2/"+filename+".json"):
			with open("Task2/"+filename+".json","r") as file:
				read = file.read()
				Localities = json.loads(read)
				print(Localities)

		
		List = []
		driver = webdriver.Chrome()#------------->
		driver.get(url)
		response = driver.execute_script("return document.documentElement.outerHTML")
		driver.quit()
		soup = BeautifulSoup(response,"lxml")
		see_all = soup.findAll("a",class_="zred")#getting all url of all see more option
		for each_see in see_all:#running loop on all see more url and working on all url inside the each see more
			see_all_a = each_see["href"]#url after click on see more
			driver = webdriver.Chrome()#-------------->
			driver.get(see_all_a)
			response = driver.execute_script("return document.documentElement.outerHTML")
			driver.quit()
			soup = BeautifulSoup(response,"lxml")

			contents = soup.findAll("article")#it have restaurant,Locality, reviews and Overall_rating

			Price_range = soup.find("span",class_="col-s-11 col-m-12 pl0").get_text().strip()#rupee 800
						
			for i in contents:#here I'm getting details of one div name content
				for y in i.findAll('div'):
					if y.get('data-res-id') != None:
						Id = y.get("data-res-id")
				restaurant = i.find("a",class_="hover_feedback").get_text().strip()
				Locality = i.find("a",class_="search_result_subzone").get_text()
				views = i.find("div",class_="bold").get_text()
				Overall_rating = i.find("span",class_="fontsize5").get_text()[:-6]

				dic = {}
				dic["ID"] = Id
				dic["OverallRating"] = Overall_rating.strip()
				dic["Reviews"] = views.strip()
				dic["locality"] = Locality
				dic["Restaurant"] = restaurant
				dic["Price"] = Price_range.strip()
				List.append(dic)
			with open("Task2/"+filename+".json","w") as file:
				read = json.dumps(List)
				file.write(read)
				file.close()
			

task2(allURL)

	


