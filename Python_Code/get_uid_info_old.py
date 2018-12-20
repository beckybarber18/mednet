from __future__ import division
from sys import argv
import urllib2
import ssl
import re
from bs4 import BeautifulSoup

# Return title, date for PubMed article w/ id pubid
def get_title(pubid):

	try:

		db = 'pubmed';

		#assemble the epost URL
		base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
		url = base + "epost.fcgi?db=" + db + "&id=" + pubid

		# Might need to specify parser
		request = urllib2.Request(url)
		gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) 

		output = urllib2.urlopen(request, context=gcontext).read()

		web = output[output.find('<WebEnv>')+len('<WebEnv>'):output.find('</WebEnv>')]
		key = output[output.find('<QueryKey>')+len('<QueryKey>'):output.find('</QueryKey>')]

		#assemble the esummary URL
		url = base + 'esummary.fcgi?db=' + db + '&query_key=' + key + '&WebEnv=' + web

		#post the esummary URL
		request = urllib2.Request(url)
		doc_summaries = urllib2.urlopen(request, context=gcontext).read()

		# Parse xml file
		soup = BeautifulSoup(doc_summaries, features = 'lxml')

		title = ''

		for tag in soup.findAll("DocSum"):

			# Find date
			for a_tag in tag.find("Item", {"Name" : "Title"}):
				title = a_tag

		return (True, title)

	except Exception, e:
		print e
		return (False, '')

def get_date(pubid):

	try:

		db = 'pubmed';

		#assemble the epost URL
		base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
		url = base + "epost.fcgi?db=" + db + "&id=" + pubid

		# Might need to specify parser
		request = urllib2.Request(url)
		gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) 

		output = urllib2.urlopen(request, context=gcontext).read()

		web = output[output.find('<WebEnv>')+len('<WebEnv>'):output.find('</WebEnv>')]
		key = output[output.find('<QueryKey>')+len('<QueryKey>'):output.find('</QueryKey>')]

		#assemble the esummary URL
		url = base + 'esummary.fcgi?db=' + db + '&query_key=' + key + '&WebEnv=' + web

		#post the esummary URL
		request = urllib2.Request(url)
		doc_summaries = urllib2.urlopen(request, context=gcontext).read()

		# Parse xml file
		soup = BeautifulSoup(doc_summaries, features = 'xml')

		date = ''

		for tag in soup.findAll("DocSum"):

			# Find date
			for a_tag in tag.find("Item", {"Name" : "PubDate"}):
				date = a_tag

		return (True, date)

	except Exception, e:
		print e
		return (False, '')

# Return number of citations in PMC for PubMed article w/ id pubid
# Adapted from https://www.ncbi.nlm.nih.gov/pmc/tools/cites-citedby/
def get_citations(pubid):

	try:

		dbfrom = 'pubmed'
		linkname = 'pubmed_pmc_refs'

		#assemble the epost URL
		base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
		url = base + "elink.fcgi?dbfrom=" + dbfrom + "&linkname=" + linkname + '&id=' + pubid

		# Might need to specify parser
		request = urllib2.Request(url)
		gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) 

		output = urllib2.urlopen(request, context=gcontext).read()

		# Parse xml file
		soup = BeautifulSoup(output, features = 'xml')

		citations = []
		num_cit = 0

	
		for tag in soup.find_all("Link"):
			# Get citations
			for cit_id in tag.find("Id"):
				citations.append(cit_id)
				num_cit += 1

		return (True, num_cit)

	except Exception, e:
		return (False, '')

def get_citations_per_year(pubid):

	try:

		CURRENT_YEAR = 2018

		success, date = get_date(pubid)
		if success == False:
			return (False, 0)

		year = date.split(' ', 1)[0]
		year = year.split('-', 1)[0]

		num_years = CURRENT_YEAR - int(year)

		success, num_cit = get_citations(pubid)
		if success == False:
			return (False, 0)

		num_cit = int(num_cit)

		cit_per_year = num_cit/num_years

		# print 'year: ', year, ' num_cit: ', num_cit, ' cit_per_year: ', cit_per_year

		return (True, cit_per_year)

	except Exception, e:
		return (False, '')


def main():

	#pubid = argv[1] 
	#print get_esummaries(pubid)
	#print get_citations(pubid)

	#pubid = argv[1]
	#print get_title(str(pubid))
	#print get_date(str(pubid))
	for pubid in range(int(argv[1]),int(argv[2])):
		print get_citations_per_year(str(pubid))


#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
	main()

	



    