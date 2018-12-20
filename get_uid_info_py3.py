#from __future__ import division
from sys import argv
#import urllib2
import urllib.request, urllib.error, urllib.parse
import ssl
import re
from bs4 import BeautifulSoup
import base64

# Return title, date for PubMed article w/ id pubid
def get_title(pubid):

	db = 'pubmed';

	#assemble the epost URL
	base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
	url = base + "epost.fcgi?db=" + db + "&id=" + pubid

	# Might need to specify parser
	#request = urllib2.Request(url)

	print('here1')
	request = urllib.request.Request(url)
	gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) 

	#output = urllib2.urlopen(request, context=gcontext).read()
	output = urllib.request.urlopen(request, context=gcontext).read()

	web = output[output.find(b'<WebEnv>')+len(b'<WebEnv>'):output.find(b'</WebEnv>')]
	key = output[output.find(b'<QueryKey>')+len(b'<QueryKey>'):output.find(b'</QueryKey>')]

	print('here2')

	#assemble the esummary URL

	print('here3')

	key_decoded = key.decode('utf8')
	web_decoded = web.decode('utf8')

	url = base + 'esummary.fcgi?db=' + db + '&query_key=' + key_decoded + '&WebEnv=' + web_decoded

	#post the esummary URL
	#request = urllib2.Request(url)
	#doc_summaries = urllib2.urlopen(request, context=gcontext).read()
	request = urllib.request.Request(url)
	doc_summaries = urllib.request.urlopen(request, context=gcontext).read()

	# Parse xml file
	soup = BeautifulSoup(doc_summaries, features = 'xml')

	for tag in soup.findAll("DocSum"):
		# Find title
		for a_tag in tag.find("Item", {"Name" : "Title"}):
			title = a_tag

	return title

def get_date(pubid):

	try:

		db = 'pubmed';

		#assemble the epost URL
		base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
		url = base + "epost.fcgi?db=" + db + "&id=" + pubid

		# Might need to specify parser
		# request = urllib2.Request(url)
		request = urllib.request.Request(url)
		gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) 

		# output = urllib2.urlopen(request, context=gcontext).read()
		output = urllib.request.urlopen(request, context=gcontext).read()

		web = output[output.find(b'<WebEnv>')+len(b'<WebEnv>'):output.find(b'</WebEnv>')]
		key = output[output.find(b'<QueryKey>')+len(b'<QueryKey>'):output.find(b'</QueryKey>')]

		#assemble the esummary URL
		url = base + 'esummary.fcgi?db=' + db + '&query_key=' + key + '&WebEnv=' + web

		#post the esummary URL
		# request = urllib2.Request(url)
		# doc_summaries = urllib2.urlopen(request, context=gcontext).read()
		request = urllib.request.Request(url)
		doc_summaries = urllib.request.urlopen(request, context=gcontext).read()

		# Parse xml file
		soup = BeautifulSoup(doc_summaries, features = 'xml')

		for tag in soup.findAll("DocSum"):

			# Find date
			for a_tag in tag.find("Item", {"Name" : "PubDate"}):
				date = a_tag

		return (True, date)

	#except Exception, e:
	except Exception as e:
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
		# request = urllib2.Request(url)
		request = urllib.request.Request(url)
		gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) 

		#output = urllib2.urlopen(request, context=gcontext).read()
		output = urllib.request.urlopen(request, context=gcontext).read()

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

	#except Exception, e:
	except Exception as e:
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

	#except Exception, e:
	except Exception as e:
		return (False, '')


def main():

	#pubid = argv[1] 
	#print get_esummaries(pubid)
	#print get_citations(pubid)

	for pubid in range(2800000,2800100):
		#print get_date(str(pubid))
		print((get_date(str(pubid))))


#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
	main()

	



    