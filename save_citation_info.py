#-----------------------------------------------------------------------
# save_citation_info.py
# Author: Rebecca Barber
#-----------------------------------------------------------------------

from sys import *
import csv
import pickle
import urllib2, time
from get_uid_info import *

#---------------------------------------------------------------------#

def calcCitationInfo(articles):

	article_citation_map = {}
	MAGIC_NUMBER = 200
	NUM_RETRIES = 3
	TIME_TO_SLEEP_RETRY = 15
	TIME_TO_SLEEP_CALLS = 10
	article_str = ''
	bad_calls = []

	article_i = 0
	index = 0
	num_calls = 0

	while index < len(articles):

		# Call every hundred times
		if index % MAGIC_NUMBER == 0 and index != 0:

			print 'making a call now; call #', num_calls
			
			citation_counts = []
			time.sleep(TIME_TO_SLEEP_CALLS)
			success, citation_counts = get_citations_per_year(article_str)

			# Handle case where success is false
			if success == False:
				print 'get_citations_per_year failure'

				filename = "article_citation_map" + str(num_calls) + ".txt"

				with open(filename, "wb") as myFile:
					pickle.dump(article_citation_map, myFile)

				for i in range(0, NUM_RETRIES):

					print 'retry #', i
					time.sleep(TIME_TO_SLEEP_RETRY)
					success, citation_counts = get_citations_per_year(article_str)
					if success == True: 
						print 'success on try ', i
						break

			if success == True:
				if len(citation_counts) != MAGIC_NUMBER:
					print 'len(citations) != MAGIC_NUMBER; len(citations)=', len(citations)
					article_i += MAGIC_NUMBER
					bad_calls.append(num_calls)
			   
				else: 
					for citation_count in citation_counts:
						pubid = int(articles[article_i])
						article_citation_map[pubid] = citation_count
						article_i += 1
			
			if success == False: 
				article_i += MAGIC_NUMBER
				bad_calls.append(num_calls)
			num_calls += 1
			article_str = ''
	
		article = articles[index]
		if index == len(articles) - 1 or (index % MAGIC_NUMBER) == (MAGIC_NUMBER -1): 
			append_me = str(article)
		else: append_me = str(article) + ','
		article_str += append_me
		index += 1

	# Last part
	citation_counts = []
	success, citation_counts = get_citations_per_year(article_str)

	# Expected number of articles left
	expected_num = len(articles) - (num_calls*MAGIC_NUMBER)

	# Handle case where success is false
	# Handle case where success is false
	if success == False:
		print 'get_citations_per_year failure'

		filename = "article_citation_map" + str(num_calls) + ".txt"

		with open(filename, "wb") as myFile:
			pickle.dump(article_citation_map, myFile)

		for i in range(0, NUM_RETRIES):

			print 'retry #', i
			time.sleep(TIME_TO_SLEEP_RETRY)
			success, citation_counts = get_citations_per_year(article_str)
			if success == True: 
				print 'success on try ', i
				break

	if success == True:
		if len(citation_counts) != expected_num:
			print 'len(citation_counts)=', len(citation_counts)
			print 'expected_num=', expected_num
			print 'num calls = ', num_calls
			print 'len(articles) = ', len(articles)
			article_i += MAGIC_NUMBER
			bad_calls.append(num_calls)
	   
		else: 
			for citation_count in citation_counts:
				pubid = int(articles[article_i])
				article_citation_map[pubid] = citation_count
				article_i += 1

	if success == False: 
		bad_calls.append(num_calls)

	for bad_call in bad_calls: 
		printMe = str(bad_call) + ' ,'
		print printMe,
	
	return article_citation_map

def main(argv):

	# articles = []
	# pattern = re.compile("Spe.*")
	# pattern2 = re.compile("Huma.*")

	# #for i in range(0, 1000000, 1000000):
	# for doc in range(0, 29000000, 1000000):

	# 	filename = '../Data/tsv_files/PubTator.' + str(doc) + \
	# 		'_' + str(doc+1000000) + '.BioC.tsv'

	# 	with open(filename) as tsvfile:

	# 		reader = csv.reader(tsvfile, delimiter = '\t')

	# 		i = 0
	# 		for row in reader:

	# 			# Check species
	# 			thisType = row[2]
	# 			if pattern.match(thisType):

	# 				thisSpecies = row[1]

	# 				# Human?
	# 				if pattern2.match(thisSpecies):

	# 					pubid = row[0]
	# 					if pubid in articles: continue
	# 					articles.append(pubid)

	# 			# keep track of where we are
	# 			if i % 100000 == 0: 
	# 				print "Doc: ", doc, "line: ", i
	# 			i+=1

	# print 'len(articles): ', len(articles)

	# with open("articles_that_need_citations.txt", "wb") as myFile:
	# 	pickle.dump(articles, myFile)

	with open('articles_that_need_citations.txt', 'rb') as dict_items_open:
		articles = pickle.load(dict_items_open)

	print 'len(articles): ', len(articles)

	article_citation_map = calcCitationInfo(articles)

	with open("article_citation_map.txt", "wb") as myFile:
		pickle.dump(article_citation_map, myFile)

#----------------------------------------------------------------------#	

if __name__ == '__main__':
	main(argv)


