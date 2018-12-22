#-----------------------------------------------------------------------
# store_data.py
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
import inflect

#---------------------------------------------------------------------#

article_citation_map = {}

def calcCitPerYear(art_need_cit, sum_cit_yr):

	MAGIC_NUMBER = 100

	article_str = ''
	index = 0
	art_need_cit_i = 0

	while index < len(art_need_cit):

		# Call every hundred times
		if index % MAGIC_NUMBER == 0 and index != 0:
			
			cit_per_year_array = []
			try:
				success, cit_per_year_array = get_citations_per_year(article_str)
			except Exception, e:
				print 'calcCitPerYear failure', e
			
			# Handle case where success is false
			if success == False: 
				print 'get_citations_per_year failure'

			else:
				#print 'success'
				for cit_per_year in cit_per_year_array:
					sum_cit_yr += cit_per_year
					this_art = int(art_need_cit[art_need_cit_i])
					article_citation_map[this_art] = cit_per_year
					art_need_cit_i += 1

			article_str = ''
	
		article = art_need_cit[index]
		if index == len(art_need_cit) - 1 or (index % MAGIC_NUMBER) == (MAGIC_NUMBER -1): 
			append_me = str(article)
		else: append_me = str(article) + ','
		article_str += append_me
		index += 1

	# Last part
	#print 'article_str: ', article_str
	success, cit_per_year_array = get_citations_per_year(article_str)
	# Handle case where success is false
	if success == False: 
		print 'get_citations_per_year failure'

	else:
		#print 'success'
		for cit_per_year in cit_per_year_array:
			#print 'art_need_cit_i:', art_need_cit_i
			sum_cit_yr += cit_per_year
			this_art = int(art_need_cit[art_need_cit_i])
			article_citation_map[this_art] = cit_per_year
			art_need_cit_i += 1

	return sum_cit_yr

# (1 + log10(nDM) + log10((Sum(Cit/yr)+1)/10)) * (1 + log10(nU/nD) + log10(nU/nM)), 
# where nDM is the number of PubMed publications related to both the disease and marker (DM), 
# Cit/yr is the sum of the annualized number of citations of DM, nU is the number of PubMed 
# publications, nD is the number of publication regarding the disease of interest, and nM is the 
# number of publications regarding the marker of interest.
def calcWeight(marker_article_map, disease, marker):


	disease_articles = marker_article_map.get(disease)
	marker_articles = marker_article_map.get(marker)
	#print 'disease_articles: ', disease_articles
	#print 'marker_articles: ', marker_articles

	DM = []

	for dis_art in disease_articles:
		if dis_art in marker_articles: 
			DM.append(dis_art)

	if len(DM) == 0: return 0
			
	sum_cit_yr = 0
	art_need_cit = []

	for art in DM:
		if art in article_citation_map:
			#print 'art in hashmap already'
			sum_cit_yr += article_citation_map[art]
		else:
			art_need_cit.append(art)

	if len(art_need_cit) != 0:
		sum_cit_yr = calcCitPerYear(art_need_cit, sum_cit_yr)

	nU = 20809119
	nDM = len(DM)
	nD = len(disease_articles)
	nM = len(marker_articles)

	cit_term = (sum_cit_yr + 1) / 10

	first_factor = 1 + math.log10(nDM) + math.log10(cit_term)
	second_factor = 1 +  math.log10(nU / nD) + math.log10(nU / nM)

	total_weight = first_factor * second_factor

	#print 'nDM: ', nDM, ' nD: ', nD, ' nM: ', nM, ' cit_term: ', cit_term, 'total weight: ', total_weight

	return total_weight


def makeGraph(marker_article_map, marker_type_map):

	pattern = re.compile("Spe.*")

	G = Graph(directed = True)

	# Add nodes to the graph with speciied types
	thisID = 0
	for marker in marker_article_map:

		thisType = marker_type_map[marker]

		if pattern.match(thisType): continue

		G.add_vertex(1) # Add one vertex
		G.vs[thisID]["name"] = marker
		G.vs[thisID]["type"] = thisType
		G.vs[thisID]["papers"] = marker_article_map.get(marker)

		thisID += 1 # Increment

	# Add edges to the graph 
	numNodes = thisID
	print 'numNodes: ', numNodes

	i = 0
	edges = []
	weights = []

	article_citation_map = defaultdict()

	for srcNode in range(0, numNodes):

		if srcNode % 10 == 0: print srcNode

		thisType = G.vs[srcNode]["type"]

		# Don't do anything if this isn't a disease -- edges
		# only leave diseases
		if thisType != 'Disease': continue

		for tarNode in range(0, numNodes):

			# Don't put species in the graph
			if pattern.match(G.vs[tarNode]["type"]): continue

			thisWeight = calcWeight(marker_article_map, \
				G.vs[srcNode]["name"], G.vs[tarNode]["name"])

			if thisWeight != 0:

				weights.append(thisWeight)
				G.degree(mode="in")
				edges.append((srcNode, tarNode))

	# Add all at once for better performance
	G.add_edges(edges)
	G.degree(mode="in")
	G.es['weight'] = weights

	print 'num vert' + str(G.vcount())
	print 'num edges' + str(G.ecount())

	return G

# 240335 human
# 52860793 species
def main(argv):

	fname = "../Data/graphs/disease_graph_v3.pickle"

	# marker_article_map = defaultdict(list)
	# marker_type_map = {}

	# lastGoodID = 0

	# # Save previous rows so can backtrack if find a relevant (human) article
	# rows = []
	# rows_index = 0

	# # RegEx's because string comparison didn't work
	# pattern = re.compile("Spe.*")
	# pattern2 = re.compile("Huma.*")

	# p = inflect.engine()

	# for doc in range(0, 29000000, 1000000):
	# #for doc in range(0, 1000000, 1000000):

	# 	# Name of the current file
	# 	filename = '../Data/tsv_files/PubTator.' + str(doc) + \
	# 		'_' + str(doc+1000000) + '.BioC.tsv'
		
	# 	with open(filename) as tsvfile:

	# 		reader = csv.reader(tsvfile, delimiter = '\t')
	# 		i = 0

	# 		for row in reader:

	# 			rows.append(row)
	# 			rows_index += 1

	# 			# If still a good paper (related to humans)
	# 			paper_id = row[0]
	# 			if (lastGoodID == paper_id):

	# 				marker = row[1].lower()

	# 				# Deal with things like "metastisis," which NLP thinks is plural...
	# 				if marker[len(marker)-3:len(marker)] != 'sis':

	# 					marker_single = p.singular_noun(marker)
	# 					if marker_single == False: marker_single = marker

	# 				else: marker_single = marker

	# 				this_type = row[2]

	# 				# don't append an article more than once!
	# 				if row[0] not in marker_article_map[marker_single]:
	# 					marker_article_map[marker_single].append(row[0])
					
	# 				marker_type_map[marker_single] = this_type

	# 				continue

	# 			thisType = row[2]

	# 			# Check species
	# 			if pattern.match(thisType):

	# 				thisSpecies = row[1]

	# 				# Human?
	# 				if pattern2.match(thisSpecies):

	# 					# ID of the most recent paper related to humans
	# 					lastGoodID = row[0]

	# 					# Backtrack until see all of the terms related to this paper
	# 					while rows[rows_index-1][0] == lastGoodID:

	# 						marker = row[1].lower()

	# 						# Deal with things like "metastisis," which NLP thinks is plural...
	# 						if marker[len(marker)-3:len(marker)] != 'sis':

	# 							marker_single = p.singular_noun(marker)
	# 							if marker_single == False: marker_single = marker

	# 						else: marker_single = marker

	# 						# don't append an article more than once!
	# 						if row[0] not in marker_article_map[marker_single]:
	# 							marker_article_map[marker_single].append(row[0])
	# 						marker_type_map[marker_single] = row[2]

	# 						rows_index -= 1

	# 					rows_index = len(rows)

	# 			if i % 100000 == 0: 
	# 				print "Doc: ", doc, "line: ", i
	# 			i+=1

	# with open("../Data/marker_article_map_v3.txt", "wb") as myFile:
	# 	pickle.dump(marker_article_map, myFile)

	# with open("../Data/marker_type_map.txt_v3", "wb") as myFile:
	# 	pickle.dump(marker_type_map, myFile)

	with open('../Data/marker_type_map_v3.txt', 'rb') as dict_items_open:
		marker_type_map = pickle.load(dict_items_open)

	with open('../Data/marker_article_map_v3.txt', 'rb') as dict_items_open:
		marker_article_map = pickle.load(dict_items_open)

	print len(marker_article_map)
	print len(marker_type_map)

	markerGraph = makeGraph(marker_article_map, marker_type_map)

	markerGraph.write_pickle(fname=fname)
		
#----------------------------------------------------------------------#	

if __name__ == '__main__':
	main(argv)
