#!/usr/bin/python
# encoding: utf-8

from bs4 import BeautifulSoup
from urllib2 import urlopen
import numpy as np
import argparse

def get_tables(url):
	html = urlopen(url).read()
	soup = BeautifulSoup(html, "lxml", from_encoding="iso-8859-1")
	tables = soup.find_all("table")
	return tables

def get_team_info(table):
	content = table.findAll("td")
	teamID = content[2].text
	teamNAME = content[3].text
	playerSOCNUMS, playerNAMES, playerJERSEYS, playerGOALS, playerASS, playerPOINTS, playerPEN, teamLEADER = [], [], [], [], [], [], [], [] 
	n = 7
	offset = 11
	for i in range(len(content)-offset-4):
		j = i + offset;
		if i%n == 0:
			if content[j].text.strip() != "":
				#print "socnum = "+content[j].text
				playerSOCNUMS.append(content[j].text.encode("utf-8"))
			else:
				#print "socnum = NA"
				playerSOCNUMS.append("NA")
		if i%n == 1:
			if content[j].text.strip() != "":
				#print "jersey = "+content[j].text
				playerJERSEYS.append(content[j].text.encode("utf-8"))
			else:
				#print "jersey = NA"
				playerJERSEYS.append("NA")
		if i%n == 2:
			if content[j].text.strip() != "":
				#print "name = "+content[j].text
				playerNAMES.append(content[j].text.encode("utf-8"))
			else:
				#print "name = NA"
				playerNAMES.append("NA")
		if i%n == 3:
			if content[j].text.strip() != "":
				#print "goals = "+content[j].text
				playerGOALS.append(content[j].text.encode("utf-8"))
			else:
				#print "goals = 0"
				playerGOALS.append("0")
		if i%n == 4:
			if content[j].text.strip() != "":
				#print "ass = "+content[j].text
				playerASS.append(content[j].text.encode("utf-8"))
			else:
				#print "ass = 0"
				playerASS.append("0")
		if i%n == 5:
			if content[j].text.strip() != "":
				#print "points = "+content[j].text
				playerPOINTS.append(content[j].text.encode("utf-8"))
			else:
				#print "points = 0"
				playerPOINTS.append("0")
		if i%n == 6:
			if content[j].text.strip() != "":
				#print "pen = "+content[j].text
				playerPEN.append(content[j].text.encode("utf-8"))
			else:
				#print "pen = 0"
				playerPEN.append("0")
	teamLEADER.append(content[len(content)-3].text.encode("utf-8"))
	return teamID, teamNAME, playerSOCNUMS, playerNAMES, playerJERSEYS, playerGOALS, playerASS, playerPOINTS, playerPEN, teamLEADER

def get_match_info(table):
	content = table.findAll("td")
	match_name, match_id, season, match_datetime, arena, result, halftime, audience, temp = [content[i].text.encode("utf-8") for i in range(1,18,2)]
	return match_name, match_id, season, match_datetime, arena, result, halftime, audience, temp 

def get_goal_stats(table):
	content = table.findAll("td")
	penalty_goalsA = content[4].text.encode("utf-8")
	penalty_goalsB = content[5].text.encode("utf-8")
	corner_goalsA = content[7].text.encode("utf-8")
	corner_goalsB = content[8].text.encode("utf-8")
	freeshot_goalsA = content[10].text.encode("utf-8")
	freeshot_goalsB = content[11].text.encode("utf-8")
	ownshot_goalsA = content[13].text.encode("utf-8")
	ownshot_goalsB = content[14].text.encode("utf-8")
	return penalty_goalsA, penalty_goalsB, corner_goalsA, corner_goalsB, freeshot_goalsA, freeshot_goalsB, ownshot_goalsA, ownshot_goalsB

def get_corner_penalty_stats(table):
	content = table.findAll("td")
	num_cornersA = content[4].text.encode("utf-8")
	num_cornersB = content[5].text.encode("utf-8")
	num_penaltiesA = content[7].text.encode("utf-8")
	num_penaltiesB = content[8].text.encode("utf-8")
	return num_cornersA, num_cornersB, num_penaltiesA, num_penaltiesB

def write_to_file(file_name,df):
	head_row = "match_date|match_id|teamA|teamB|teamA_id|teamB_id|teamA_url|teamB_url|scoreA|scoreB|audience|ref|match_report_url|match_report_id"
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
	#parser = argparse.ArgumentParser(description='An argparse example', epilog='Example usage: python scaper.py --output=scraper_output.csv --url=http://elitrapport.se/schema.asp?gamesectionID=10105')
	#parser.add_argument('-u', '--url', dest='url', required=True, help='url to scrape on elitrapport.se')
	#parser.add_argument('-o', '--output', dest='output', required=True, help='file to save the result')
	#args = parser.parse_args()
	#url = args.url
	#fname = args.output

	fname = "scraper_output.csv"
	url = "http://www.elitrapport.se/Data/report7400.html"
	
	print "\nStarting to scrape match report "+str(url)+" to "+str(fname)

	# Get the html tables
	tables = get_tables(url)
	
	# TeamA
	teamAID, teamANAME, playerASOCNUMS, playerANAMES, playerAJERSEYS, playerAGOALS, playerAASS, playerAPOINTS, playerAPEN, teamALEADER = get_team_info(tables[1])
	#print teamAID
	#print teamANAME
	#print teamALEADER[0]
	#print playerANAMES

	# TeamB
	#print ""
	teamBID, teamBNAME, playerBSOCNUMS, playerBNAMES, playerBJERSEYS, playerBGOALS, playerBASS, playerBPOINTS, playerBPEN, teamBLEADER = get_team_info(tables[2])
	#print teamBID
	#print teamBNAME
	#print teamBLEADER[0]
	#print playerBNAMES
	#print playerBGOALS

	match_name, match_id, season, match_datetime, arena, result, halftime, audience, temp = get_match_info(tables[3])
	penalty_goalsA, penalty_goalsB, corner_goalsA, corner_goalsB, freeshot_goalsA, freeshot_goalsB, ownshot_goalsA, ownshot_goalsB = get_goal_stats(tables[4])
	num_cornersA, num_cornersB, num_penaltiesA, num_penaltiesB = get_corner_penalty_stats(tables[5])
	
	get_penalty_info(table[6])

	# Parse information
	#match_dates = get_match_dates(content)
	#match_ids = get_match_ids(content)
	#teamA, teamB = get_team_names(content)
	#A_urls, B_urls, A_ids, B_ids = get_team_urls_ids(content)
	#scoreA, scoreB = get_score(content)
	#audience = get_audience(content)
	#ref = get_ref(content)
	#match_report_url, match_report_id = get_match_report(content)
	
	# Gather all results
	'''df = (
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
		match_report_id
		)

	print "\n\nScraped "+str(len(match_dates))+" matches"

	# Write result to file
	write_to_file(fname,df)'''

if __name__ == "__main__":
	main()
