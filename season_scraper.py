#!/usr/bin/python
# encoding: utf-8

from bs4 import BeautifulSoup
from urllib2 import urlopen
import numpy as np
import time
import os, datetime

def make_soup(url):
	html = urlopen(url).read()
	soup = BeautifulSoup(html, "lxml", from_encoding="iso-8859-1")
	table = soup.find("table",id="serietabell")
	content = table.find_all("td",nowrap="nowrap")
	return content

def get_match_dates(content):
	match_dates = []
	for i in range(0,len(content),7):
		match_dates.append(content[i].text+":00")
	return match_dates

def get_match_ids(content):
	match_ids = []
	for i in range(1,len(content),7):
		if content[i].text != "":
			match_ids.append(content[i].text)
		else: 
			match_ids.append('0')
	return match_ids

def get_team_names(content):
	teamA = []
	teamB = []
	for i in range(2,len(content),7):
		uniA = content[i].text.split("-")[0]
		uniB = content[i].text.split("-")[1]
		strippedA = uniA.strip()
		strippedB = uniB.strip()
		teamA.append(strippedA.encode("utf-8"))
		teamB.append(strippedB.encode("utf-8"))
	return teamA, teamB

def get_team_urls_ids(content):
	A_urls = []
	B_urls = []
	A_ids = []
	B_ids = []
	for i in range(2,len(content),7):
		urls = content[i].find_all("a")
		A_urls.append(urls[0].get("href"))
		B_urls.append(urls[1].get("href"))
		A_ids.append(urls[0].get("href").split("teamID=")[1])
		B_ids.append(urls[1].get("href").split("teamID=")[1])
	return A_urls, B_urls, A_ids, B_ids

def get_score(content):
	scoreA = []
	scoreB = []
	for i in range(3,len(content),7):
		scores = content[i].text.split("-")
		scoreA.append(scores[0].strip().encode("utf-8"))
		scoreB.append(scores[1].strip().encode("utf-8"))
	return scoreA, scoreB

def get_audience(content):
	audience = []
	for i in range(4,len(content),7):
		if content[i].text == "":
			audience.append("0")
		else:
			audience.append(content[i].text.encode("utf-8"))
	return audience

def get_ref(content):
	ref = []
	for i in range(5,len(content),7):
		if content[i].text == "":
			ref.append("NA")
		else:
			ref.append(content[i].text.encode("utf-8"))
	return ref

def get_match_report(content):
	match_report_url = []
	match_report_id = []
	for i in range(6,len(content),7):
		if content[i].text == "":
			match_report_url.append("NA")
			match_report_id.append("0")
		else:
			url = content[i].find("a").get("href")
			match_report_url.append(url)
			match_report_id.append(url.split("report")[1].split(".html")[0])
	return match_report_url, match_report_id

def write_to_file(file_name,df):
	head_row = "match_date|match_id|teamA|teamB|teamA_id|teamB_id|teamA_url|teamB_url|scoreA|scoreB|audience|ref|match_report_url|match_report_id|serie|serie_url"
	with open(file_name, "w") as text_file:
		text_file.write(head_row)
		text_file.write("\n")
		for i in range(len(df[0])):
			for j in range(len(df)):
				text_file.write(df[j][i])
				if j < len(df)-1:
					text_file.write("|")
			if i < len(df[0])-1:
				text_file.write("\n")

def main():
	# Create output dir
	mydir = os.path.join(os.getcwd(), "output-"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
	os.makedirs(mydir)
	# Define pages to scrape
	gamesectionDICT = {
		'elitserien1314.csv': 'http://elitrapport.se/schema.asp?gamesectionID=10105',
		'kvartsfinal1314.csv': 'http://elitrapport.se/schema.asp?gamesectionID=10168',
		'semifinal1314.csv': 'http://elitrapport.se/schema.asp?gamesectionID=10172',
		#'final1314.csv': 'http://elitrapport.se/schema.asp?gamesectionID=10173',
		'elitserie_kvalA1314.csv': 'http://elitrapport.se/schema.asp?gamesectionID=10175',
		'elitserie_kvalA1314.csv': 'http://elitrapport.se/schema.asp?gamesectionID=10176',
		'allsvenskan_norr1314.csv': 'http://elitrapport.se/schema.asp?gamesectionID=10109',
		'allsvenskan_sodra1314.csv': 'http://elitrapport.se/schema.asp?gamesectionID=10110',
	}
	# Start scraping
	for fname, url in gamesectionDICT.iteritems():
		print "\n###\n\n   Starting to scrape "+str(url)+" ..."
		time.sleep(1)
		# Get the html information
		content = make_soup(url)
		# Parse information
		match_dates = get_match_dates(content)
		match_ids = get_match_ids(content)
		teamA, teamB = get_team_names(content)
		A_urls, B_urls, A_ids, B_ids = get_team_urls_ids(content)
		scoreA, scoreB = get_score(content)
		audience = get_audience(content)
		ref = get_ref(content)
		match_report_url, match_report_id = get_match_report(content)
		# Scrape info
		N = len(match_dates)
		serie = fname.split(".csv")[0]
		serie_url = url
		serie_list = [serie for k in range(N)]
		serie_url_list = [serie_url for k in range(N)]
		# Gather all results
		df = (
			match_dates,
			match_ids,
			teamA,
			teamB,
			A_ids,
			B_ids,
			A_urls,
			B_urls,
			scoreA,
			scoreB,
			audience,
			ref,
			match_report_url,
			match_report_id,
			serie_list,
			serie_url_list
			)
		print "   "+str(N)+" matches scraped ...\n   Storing results in " + str(mydir)+"/"+str(fname) + " ..."
		# Write result to file
		write_to_file(mydir+"/"+fname,df)
	# Merge results
	ii = 0;
	for fname, url in gamesectionDICT.iteritems():
		temp = np.genfromtxt(mydir+"/"+fname, delimiter='|', dtype="object", skip_header=1, autostrip=True)
		if ii < 1:
			merged_data = temp;
		else:
			merged_data = np.concatenate((merged_data, temp))
		ii = ii + 1;
	# Save data frame
	np.savetxt(mydir+"/merged.csv", merged_data, delimiter="|", fmt="%s", header="match_date|match_id|teamA|teamB|teamA_id|teamB_id|teamA_url|teamB_url|scoreA|scoreB|audience|ref|match_report_url|match_report_id|serie|serie_url")	
	print "   Storing merged results in " + str(mydir)+"/merged.csv ..."



if __name__ == "__main__":
	main()
