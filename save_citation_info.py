#-----------------------------------------------------------------------
# save_citation_info.py
# Author: Rebecca Barber
#-----------------------------------------------------------------------

from sys import *
import csv
import pickle
import urllib2
from get_uid_info import *

#---------------------------------------------------------------------#

def main(argv):

	# with open('article_citation_map.txt', 'rb') as dict_items_open:
	# 	article_citation_map = pickle.load(dict_items_open)

	# for k, v in article_citation_map.iteritems():
	# 	print k, v

	article_citation_map = {}
	pattern = re.compile("Spe.*")
	pattern2 = re.compile("Huma.*")

	#for i in range(0, 1000000, 1000000):
	for i in range(0, 29000000, 1000000):

		print
		print i

		filename = '../Data/tsv_files/PubTator.' + str(i) + \
			'_' + str(i+1000000) + '.BioC.tsv'

		with open(filename) as tsvfile:

			reader = csv.reader(tsvfile, delimiter = '\t')

			j = -1

			for row in reader:

				if j % 10000 == 0: 
					print j
				j+=1

				if j == 0: continue

				# Check species
				thisType = row[2]
				if pattern.match(thisType):

					thisSpecies = row[1]

					# Human?
					if pattern2.match(thisSpecies):

						pubid = row[0]

						if pubid in article_citation_map: continue

						success, numCit = get_citations_per_year(str(pubid))
						if success == False: continue

						article_citation_map[pubid] = numCit


	with open("article_citation_map.txt", "wb") as myFile:
		pickle.dump(article_citation_map, myFile)

#----------------------------------------------------------------------#	

if __name__ == '__main__':
	main(argv)


