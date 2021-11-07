import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

## Sample Code to Print to File

# f = open('output3.txt', 'w')
# for i in links:
# 	print(i, file=f)
# f.close()

## Define a Function to get the links for all 60 matches of the IPL Season from the given IPL Season URL

def get_links_for_season_matches(url): # Takes input of master url of the IPL season
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')
	results = soup.find(id = 'series-matches') # Get the content under id series-matches. This gives us 60 objects containing info about all the matches
	cl = results.find_all('div', class_='cb-col-60 cb-col cb-srs-mtchs-tm') # This class contains the links for individual matches
	links = []
	match_desc = []

	for i in range(len(cl)):
		link = cl[i].find_all('a')
		links.append('https://www.cricbuzz.com/cricket-full-commentary' + link[0]['href'][15:])
		match_desc.append(link[0]['title'].partition(" Live")[0])

	return links, match_desc

## Define a Function to get the commentary text for all the deliveries in a match 

def get_comm(url): # Takes input of master url of full commentary of the match
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--incognito')
	options.add_argument('--headless') # define options for chrome webdriver

	driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver_win32\chromedriver.exe', chrome_options=options)
	driver.get(url)
	time.sleep(3) # wait for page to load completely

	btns = driver.find_elements(By.XPATH, "//a[contains(text(), 'Inns')]") # find the js buttons for first and second innings

	comm_inns_1 = []
	comm_inns_2 = []
	comm_inns_text_1 = []
	comm_inns_text_2 = []

	for i in range(len(btns)):
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable(btns[i])).click() # click the js buttons identified above after waiting for the button to be clickable
		time.sleep(3)
		pg_src = driver.page_source
		soup = BeautifulSoup(pg_src, 'html.parser') 

		if i == 0:
			res = soup.find_all('div', {'class':'cb-col cb-col-100 ng-scope'}) # Get all commentary sized 
			for j in range(len(res)):
				if len(res[j].find_all('div', {'class':'cb-col cb-col-8 text-bold ng-scope'})) != 0:
					comm_inns_1.append(res[j])
			for i in comm_inns_1:
				comm_inns_text_1.append(i.text)
			comm_inns_text_1.reverse()
		elif i == 1:
			res = soup.find_all('div', {'class':'cb-col cb-col-100 ng-scope'})
			for j in range(len(res)):
				if len(res[j].find_all('div', {'class':'cb-col cb-col-8 text-bold ng-scope'})) != 0:
					comm_inns_2.append(res[j])
			for i in comm_inns_2:
				comm_inns_text_2.append(i.text)
			comm_inns_text_2.reverse()

	comm_inns_text = comm_inns_text_1 + comm_inns_text_2
	driver.close()

	return comm_inns_text