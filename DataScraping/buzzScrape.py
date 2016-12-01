#!/usr/bin/python
import csv
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
import sys

def dic2csv(dicti):
        with open('testfile3.csv', 'w') as f:
                w = csv.DictWriter(f,dicti[0].keys())
                w.writeheader()
                w.writerows(dicti)

BASE_URL = "https://www.buzzfeed.com"

def get_archive_links(archive_link):
	html = urlopen(archive_link).read()
	soup = BeautifulSoup(html, "lxml")
	archive = soup.find("div", "month")
	archiveLinks = [BASE_URL + a["href"] for a in archive.findAll("a")]
	return archiveLinks

def get_article_links(section_url):
	html = urlopen(section_url).read()
	soup = BeautifulSoup(html, "lxml")
	article = soup.find("ul", "flow")
	articleLinks = [BASE_URL + li.a["href"] for li in article.findAll("li")]
	return articleLinks

def get_article_headline(headline_url, date):
	html = urlopen(headline_url).read()
	soup = BeautifulSoup(html, "lxml")
	headline = soup.find("title").string
	category = soup.find("meta", property="article:section")["content"]
	site_name = soup.find("meta", property="og:site_name")["content"]
	return {"headline": headline,
		"headline_url": headline_url,
		"article_category": category,
		"site_name": site_name,
		"date": date}

data = []
if len(sys.argv) >= 3:
	maxArticles = int(sys.argv[2])
else:
	maxArticles = 10000
artCount = 0
for i in range(1,13):
	archives = get_archive_links("https://www.buzzfeed.com/archive/"+sys.argv[1]+"/"+str(i))
	for archive in archives:
		articles = get_article_links(archive)
		for article in articles:
			try:
				headline = get_article_headline(article,archive[33:len(archive)])
				data.append(headline)
			except urllib.error.HTTPError:
				dic2csv(data)
				print("oh no there was a http error fuck")
			artCount = artCount + 1
			if(artCount % 10 == 0):
				print(str(artCount*100/maxArticles)+"%")
			if(artCount % 1000 == 0):
				dic2csv(data)
		print(str(artCount)+" many articles have been scraped, out of a max of "+str(maxArticles))
	if artCount  >= maxArticles:
		break
dic2csv(data)
