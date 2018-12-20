#-----------------------------------------------------------------------
# store_marker_types_and_articles.py
# Author: Rebecca Barber
#-----------------------------------------------------------------------

from __future__ import division
from sys import *
import csv
from collections import defaultdict
from igraph import *
#import networkx as nx
import numpy
import math
import pickle
import re
from get_uid_info import *

#---------------------------------------------------------------------#

def main(argv):

	marker_article_map = defaultdict(list)
	marker_type_map = {}

	lastGoodID = 0

	# Save previous rows so can backtrack if find a relevant (human) article
	rows = []
	rows_index = 0

	# RegEx's because string comparison didn't work
	pattern = re.compile("Spe.*")
	pattern2 = re.compile("Huma.*")

	for doc in range(0, 29000000, 1000000):
	#for doc in range(0, 1000000, 1000000):

		# Name of the current file
		filename = '../Data/tsv_files/PubTator.' + str(doc) + \
			'_' + str(doc+1000000) + '.BioC.tsv'
		
		with open(filename) as tsvfile:

			reader = csv.reader(tsvfile, delimiter = '\t')
			i = 0

			for row in reader:

				rows.append(row)
				rows_index += 1

				# If still a good paper (related to humans)
				if (lastGoodID == row[0]):
					
					marker_article_map[row[1]].append(row[0])
					marker_type_map[row[1]] = row[2]
					continue

				thisType = row[2]

				# Check species
				if pattern.match(thisType):

					thisSpecies = row[1]

					# Human?
					if pattern2.match(thisSpecies):

						# ID of the last paper related to humans
						lastGoodID = row[0]

						# Backtrack until see all of the terms related to this paper
						while rows[rows_index-1][0] == lastGoodID:

							marker_article_map[row[1]].append(row[0])
							marker_type_map[row[1]] = row[2]

							rows_index -= 1

						rows_index = len(rows)

				if i % 100000 == 0: 
					print "Doc: ", doc, "line: ", i
				i+=1

	with open("marker_article_map.txt", "wb") as myFile:
		pickle.dump(marker_article_map, myFile)

	with open("marker_type_map.txt", "wb") as myFile:
		pickle.dump(marker_type_map, myFile)

	# with open('marker_article_map.txt', 'rb') as dict_items_open:
	# 	marker_article_map = pickle.load(dict_items_open)

	# with open('marker_type_map.txt', 'rb') as dict_items_open:
	# 	marker_type_map = pickle.load(dict_items_open)

#----------------------------------------------------------------------#	

if __name__ == '__main__':
	main(argv)

