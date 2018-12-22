from __future__ import division
from sys import argv
import urllib2
import ssl
import re, time
from bs4 import BeautifulSoup

# Return title, date for PubMed article w/ id pubid

#TIME_TO_SLEEP = 5
TIME_TO_SLEEP = 3
def get_title(id_list):

	try:

		time.sleep(TIME_TO_SLEEP)

		id_list_array = id_list.split(',')
		print 'id_list_array length: ', len(id_list_array)

		db = 'pubmed';

		#assemble the epost URL
		base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
		url = base + "epost.fcgi?db=" + db + "&id=" + id_list

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
		#print soup

		titles = []
		iteration = 0

		for tag in soup.findAll('docsum'):		

			# Loop through until find the id that == the next expected
			while True:

				next_expected = id_list_array[iteration]
				this_id = ''

				for a_tag in tag.find("id"):
					this_id = str(a_tag)

				#print 'next expected: ', next_expected
				#print 'this id: ', this_id 

				if next_expected != this_id:
					titles.append('')
					iteration += 1
				else:
					iteration += 1
					break
				
			# Find date
			num_tags = 0

			for a_tag in tag.find("item", {"name" : "Title"}):

				titles.append(a_tag)
				num_tags += 1

			# In case there is no date in the article
			if num_tags == 0: titles.append('')

		# In case there were errors at the end
		while len(titles) != len(id_list_array):
			titles.append('')

		return (True, titles)

	except Exception, e:
		print e
		return (False, '')

def get_date(id_list):

	try:

		time.sleep(TIME_TO_SLEEP)

		id_list_array = id_list.split(',')

		db = 'pubmed';

		#assemble the epost URL
		base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
		url = base + "epost.fcgi?db=" + db + "&id=" + id_list

		#print 'first url:', url

		# Might need to specify parser
		request = urllib2.Request(url)
		gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) 

		output = urllib2.urlopen(request, context=gcontext).read()

		web = output[output.find('<WebEnv>')+len('<WebEnv>'):output.find('</WebEnv>')]
		key = output[output.find('<QueryKey>')+len('<QueryKey>'):output.find('</QueryKey>')]

		#assemble the esummary URL
		url = base + 'esummary.fcgi?db=' + db + '&query_key=' + key + '&WebEnv=' + web

		#print 'second url:', url

		time.sleep(TIME_TO_SLEEP)

		#post the esummary URL
		request = urllib2.Request(url)
		doc_summaries = urllib2.urlopen(request, context=gcontext).read()
		#print doc_summaries

		# Parse xml file
		soup = BeautifulSoup(doc_summaries, features = 'lxml')

		dates = []
		iteration = 0

		for tag in soup.findAll('docsum'):		

			# Loop through until find the id that == the next expected
			while True:

				next_expected = id_list_array[iteration]
				this_id = ''

				for a_tag in tag.find("id"):
					this_id = str(a_tag)

				if next_expected != this_id:
					dates.append(0)
					iteration += 1
				else:
					iteration += 1
					break
				
			# Find date
			num_tags = 0
			for a_tag in tag.find("item", {"name" : "PubDate"}):
				dates.append(a_tag)
				num_tags += 1

			# In case there is no date in the article
			if num_tags == 0: dates.append('')

		# In case there were errors at the end
		while len(dates) != len(id_list_array):
			dates.append(0)

		return (True, dates)

	except Exception, e:
		print 'date', e
		return (False, [])

def get_citations(id_list):

	try:

		time.sleep(TIME_TO_SLEEP)

		id_list_array = id_list.split(',')

		dbfrom = 'pubmed'
		linkname = 'pubmed_pmc_refs'

		#assemble the epost URL
		base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
		url = base + "elink.fcgi?dbfrom=" + dbfrom + "&linkname=" + linkname

		for pubid in id_list_array:
			append_me = '&id=' + pubid
			url += append_me

		# Might need to specify parser
		request = urllib2.Request(url)
		gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) 

		output = urllib2.urlopen(request, context=gcontext).read()

		# Parse xml file
		soup = BeautifulSoup(output, features = 'xml')

		citations = []
		iteration = 0

		for tag in soup.findAll('LinkSet'):	

			num_cit = 0	

			# Loop through until find the id that == the next expected
			while True:

				next_expected = id_list_array[iteration]
				this_id = ''

				for a_tag in tag.find("Id"):
					this_id = str(a_tag)
					break

				if next_expected != this_id:
					citations.append(0)
					iteration += 1
				else:
					iteration += 1
					break

			# Find citations
			num_citations = 0

			for a_tag in tag.find_all("Link"):
				num_citations += 1

			citations.append(num_citations)

		# In case there were errors at the end
		while len(citations) != len(id_list_array):
			citations.append(0)

		return (True, citations)

	except Exception, e:
		print 'citations', e
		return (False, [])

# # Return number of citations in PMC for PubMed article w/ id pubid
# # Adapted from https://www.ncbi.nlm.nih.gov/pmc/tools/cites-citedby/
# def get_citations(id_list):

# 	id_array = id_list.split(',')
# 	citations = []

# 	for pubid in id_array:

# 		success, num_cit = get_citations_indiv(pubid)

# 		if success == False:
# 			num_cit = 0
# 		citations.append(num_cit)

# 	return citations

def get_citations_per_year(id_list):

	try:

		CURRENT_YEAR = 2019

		success, dates = get_date(id_list)
		if success == False:
			return (False, [])

		#print 'got dates'

		years = []
		for date in dates:
			if date == 0:
				years.append(-1)
			else:
				year = date.split(' ', 1)[0]
				year = year.split('-', 1)[0]
				#print 'year: ', year
				if not year.isdigit(): years.append(-1)
				else:
					num_years = CURRENT_YEAR - int(year)
					years.append(num_years)

		#print 'got years'

		success, citations = get_citations(id_list)
		if success == False:
			return (False, [])

		#print 'got citations'

		if len(citations) != len(dates): 
			print 'len(citations): ', len(citations)
			print 'len(dates): ', len(dates)
			return (False, 'length dif')

		cit_per_year_array = []
		i = 0

		for num_cit in citations:

			if years[i] == -1:
				cit_per_year_array.append(0)
			else:
				num_cit = int(num_cit)
				if years[i] == 0:
					years[i] = 1
				cit_per_year = num_cit/years[i]
				cit_per_year_array.append(cit_per_year)

			i += 1

		#print 'year: ', year, ' num_cit: ', num_cit, ' cit_per_year: ', cit_per_year

		return (True, cit_per_year_array)

	except Exception, e:
		print get_citations_per_year, e
		return (False, [])


def main():

	#pubid = argv[1] 
	#print get_esummaries(pubid)
	#print get_citations(pubid)

	#pubid = argv[1]
	#print get_title(str(pubid))
	#print get_date(str(pubid))

	#id_list = '2'
	id_list = '1,2,3'

	for pubid in range(0,int(argv[1])):
		print get_citations_per_year(str(id_list))
		#print get_date(str(id_list))
		# print get_citations_per_year(str(id_list))
		# print get_citations_per_year(id_list)


#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
	main()

	



    