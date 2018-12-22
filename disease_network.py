#!/usr/bin/env python

#-----------------------------------------------------------------------
# disease_network.py
# Author: Rebecca Barber
#-----------------------------------------------------------------------

from __future__ import division
from sys import *
import csv
from igraph import *
import numpy, operator
import math
import pickle
import re
from get_uid_info import *
import inflect
import cPickle

#---------------------------------------------------------------------#

class DiseaseNetwork:

	def __init__(self):

		self._network = Graph.Read_Pickle('disease_graph_v3.pickle')

		with open('all_diseases.txt', 'rb') as fp: 
			self._diseases = pickle.load(fp)

	def get_disease_options(self):
		return self._diseases

	# checks if abbrev is an abbreviation of text
	def is_abbrev(self, abbrev, text):
	    abbrev=abbrev.lower()
	    text=text.lower()
	    words=text.split()
	    if not abbrev:
	        return True
	    if abbrev and not text:
	        return False
	    if abbrev[0]!=text[0]:
	        return False
	    else:
	        return (self.is_abbrev(abbrev[1:],' '.join(words[1:])) or
	                any(self.is_abbrev(abbrev[1:],text[i+1:])
	                    for i in range(len(words[0]))))

	# Check if bm1 (biomarker 1) and bm2 (biomarker 2) are too similar
	def clash(self, bm1, bm2):

		# So checking isn't case-sensitive
		bm1 = bm1.lower()
		bm2 = bm2.lower()

		# So checking is not plural-sensitive
		p = inflect.engine()
		bm1_single = p.singular_noun(bm1)
		bm2_single = p.singular_noun(bm2)

		# If the biomarker was already single, this returns False
		if bm1_single == False: bm1_single = bm1
		if bm2_single == False: bm2_single = bm2

		if bm1_single.find(bm2_single) > -1: return True # bm2 in bm1
		if bm2_single.find(bm1_single) > -1: return True  # bm1 in bm2

		# Check for abbreviations
		if self.is_abbrev(bm1, bm2): return True
		if self.is_abbrev(bm2, bm1): return True

		return False

	def unique_articles(self, vals):

		unique_vals = []
		for item in vals:
			if item not in unique_vals:
				unique_vals.append(item)

		return unique_vals

	def get_disease_info(self, disease, diseases, genes, chemicals, \
		pmutations, dnamutations, snps):

		g = self._network

		# finds vertex for given disease
		vertices = g.vs.select(name=disease)
		if vertices is None or len(vertices) == 0: return [],[]
		disease_articles = []
		for v in vertices:
			index = v.index
			disease_articles = v['papers']

		# find all of the neighbors of the vertex
		neighbors = g.neighbors(disease, mode="out")
		if len(neighbors) == 0: return [],[]

		# get all of the weights associated with the vertices
		weights = []
		for neighbor in neighbors:
			weights.append(g.es[g.get_eid(index, neighbor)]['weight'])

		# sort neighbors and weights in order of descending weight
		weights, neighbors = zip(*sorted(zip(weights, neighbors), reverse=True))

		# print top neighbors
		NUM_RETURN = 100

		top_results = []
		top_result_types = []
		top_result_articles = []

		i = 0
		for neighbor in neighbors:

			if i == NUM_RETURN: break
			v = g.vs.find(neighbor)
			biomarker = v['name']

			if v['type'] == 'Disease' and diseases == False: continue
			if v['type'] == 'Gene' and genes == False: continue
			if v['type'] == 'Chemical' and chemicals == False: continue
			if v['type'] == 'ProteinMutation' and pmutations == False: continue
			if v['type'] == 'DNAMutation' and dnamutations == False: continue
			if v['type'] == 'SNP' and snps == False: continue

			# Make sure the disease/biomarker don't coincide
			if self.clash(disease, biomarker): continue

			success = True

			# Make sure current biomarker doesn't clash with anything we already have
			# Save index of the clasher (if it exists) so we can reference it later
			index = 0
			for result in top_results:
				if self.clash(biomarker, result): 
					success = False
					break

				index += 1

			marker_articles = v['papers']
			both_articles = []

			for dis_art in disease_articles:
				if dis_art in marker_articles: both_articles.append(dis_art)

			# If two results clash, still want to save papers of the clasher.
			# Because if you have EGFR and the full name, you don't want to forget
			# the papers that EGFR is in (if it appears second)!
			# So you have to append the papers that reference EGFR to those that
			# reference its full name.
			if success == False: 
				for article in both_articles:
					# Check if it's already there
					if article not in top_result_articles[index]:
						top_result_articles[index].append(article)
				continue


			# Because they thought that "virus" was plural...
			# And disease
			if v['type'] == 'Disease' and len(biomarker) > 2:
				if biomarker[len(biomarker)-2:len(biomarker)] == 'si':
					biomarker = biomarker + 's'

			if biomarker.find('viru') > -1:
				biomarker = biomarker.replace("viru", "virus")

			top_results.append(biomarker)
			top_result_types.append(v['type'])
			both_articles = self.unique_articles(both_articles)
			top_result_articles.append(both_articles)

			# print biomarker, ' ', weights[i]

			i +=1

		return top_results, top_result_types, top_result_articles

		
def main(argv):

	disease = argv[1]
	network = DiseaseNetwork()
	top_results, top_result_types, top_result_articles = network.get_disease_info(disease, True, True, True, True, True, True)

	# print everything
	for index in range(0, len(top_results)):
		print(top_results[index], ' ', top_result_types[index], ' ', top_result_articles[index])
	

#----------------------------------------------------------------------#	

if __name__ == '__main__':
	main(argv)

