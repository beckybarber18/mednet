#-----------------------------------------------------------------------
# get_all_diseases.py
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

#---------------------------------------------------------------------#

def main(argv):

	g = Graph.Read_Pickle('../disease_graph_v2.pickle')

	vertices = g.vs
	print 'num vertices: ', len(vertices)

	all_diseases = []

	i = 0
	for v in vertices:
		if i % 1000 == 0: print(i)
		if v['type'] != 'Disease':
			continue
		disease = v['name']
		if disease not in all_diseases:
			all_diseases.append(disease)
		i += 1

	all_diseases = sorted(all_diseases)

	with open("all_diseases.txt", "wb") as myFile:
		pickle.dump(all_diseases, myFile)

if __name__ == '__main__':
	main(argv)