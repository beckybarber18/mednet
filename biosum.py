#!/usr/bin/env python

#-----------------------------------------------------------------------
# biosum.py
# Author: Rebecca Barber
#-----------------------------------------------------------------------

from sys import argv, stderr
from disease_network import DiseaseNetwork
from get_uid_info import *
from time import localtime, asctime, strftime
from bottle import route, request, response, error, redirect, run
from bottle import template, TEMPLATE_PATH

TEMPLATE_PATH.insert(0, '')

# Original search form
def truefalse(str):
    if str == None:
        str = False
    else:
        str = True
    return str

@route('/', method=['GET', 'POST'])
def searchForm():

    disease = request.forms.get("disease")

    diseases = True
    genes = True
    chemicals = True
    pmutations = True
    dnamutations = True
    snps = True

    top_results = []
    top_result_types = []
    top_result_articles = []

    if disease is None:

        disease = ""

        try:
            network = DiseaseNetwork()
            disease_options = network.get_disease_options()
        except Exception as e:
            print >>stderr, e
    else:
        # Ensure there wasn't a database issue
        try:
            network = DiseaseNetwork()
            top_results, top_result_types, top_result_articles = network.get_disease_info(disease, \
                diseases, genes, chemicals, pmutations, dnamutations, snps)
            disease_options = network.get_disease_options()

        except Exception as e:
            print >>stderr, e

    n = len(top_result_articles)
    top_result_articles_1 = top_result_articles
    top_result_articles_2 = []

    NUM_IN_ROW = 8

    if n > NUM_IN_ROW:
        top_result_articles_1 = top_result_articles[0:NUM_IN_ROW]
        top_result_articles_2 = top_result_articles[NUM_IN_ROW:n]

    for i in range(0, len(top_result_types)):
        top_result_types[i] = top_result_types[i].lower()
    
    templateInfo = {
        'disease': disease,
        'diseases': diseases,
        'genes': genes,
        'chemicals': chemicals,
        'pmutations': pmutations,
        'dnamutations': dnamutations,
        'snps': snps,
        'top_results': top_results,
        'top_result_types': top_result_types,
        'disease_options': disease_options,
        'top_result_articles_1': top_result_articles_1,
        'top_result_articles_2': top_result_articles_2}

    response.set_cookie('prevDiseases', str(diseases))
    response.set_cookie('prevGenes', str(genes))
    response.set_cookie('prevChemicals', str(chemicals))
    response.set_cookie('prevPmutations', str(pmutations))
    response.set_cookie('prevDNAmutations', str(dnamutations))
    response.set_cookie('prevSNPs', str(snps))

    return template('searchform.tpl', templateInfo)

@route('/searchform', method=['GET', 'POST'])
def searchForm():

    disease = request.forms.get("disease")

    diseases = request.forms.get("diseases")
    diseases = truefalse(diseases)

    genes = request.forms.get("genes")
    genes = truefalse(genes)

    chemicals = request.forms.get("chemicals")
    chemicals = truefalse(chemicals)

    pmutations = request.forms.get("pmutations")
    pmutations = truefalse(pmutations)

    dnamutations = request.forms.get("dnamutations")
    dnamutations = truefalse(dnamutations)

    snps = request.forms.get("snps")
    snps = truefalse(snps)

    top_results = []
    top_result_types = []
    top_result_articles = []

    if disease is None:

        disease = ""

        try:
            network = DiseaseNetwork()
            disease_options = network.get_disease_options()
        except Exception as e:
            print >>stderr, e
    else:
        # Ensure there wasn't a database issue
        try:
            network = DiseaseNetwork()
            top_results, top_result_types, top_result_articles = network.get_disease_info(disease, \
                diseases, genes, chemicals, pmutations, dnamutations, snps)
            disease_options = network.get_disease_options()

        except Exception as e:
            print >>stderr, e

    top_result_articles_1 = []
    top_result_articles_2 = []

    for i in range(0, len(top_result_articles)):

        these_articles = top_result_articles[i]
        n = len(these_articles)

        first_part = these_articles
        second_part = []

        NUM_IN_ROW = 8

        if n > NUM_IN_ROW:
            first_part = these_articles[0:NUM_IN_ROW]
            second_part = these_articles[NUM_IN_ROW:n]

        top_result_articles_1.append(first_part)
        top_result_articles_2.append(second_part)

    for i in range(0, len(top_result_types)):
        top_result_types[i] = top_result_types[i].lower()

    templateInfo = {
        'disease': disease,
        'diseases': diseases,
        'genes': genes,
        'chemicals': chemicals,
        'pmutations': pmutations,
        'dnamutations': dnamutations,
        'snps': snps,
        'top_results': top_results,
        'top_result_types': top_result_types,
        'disease_options': disease_options,
        'top_result_articles_1': top_result_articles_1,
        'top_result_articles_2': top_result_articles_2}

    response.set_cookie('prevDiseases', str(diseases))
    response.set_cookie('prevGenes', str(genes))
    response.set_cookie('prevChemicals', str(chemicals))
    response.set_cookie('prevPmutations', str(pmutations))
    response.set_cookie('prevDNAmutations', str(dnamutations))
    response.set_cookie('prevSNPs', str(snps))

    return template('searchform.tpl', templateInfo)

def str2bool(str):
    if str == 'True':
        return True
    else: return False

@route('/details')
def details():

    marker = request.query.get('marker')
    disease = request.query.get('disease')

    diseases = request.get_cookie('prevDiseases')
    genes = request.get_cookie('prevGenes')
    chemicals = request.get_cookie('prevChemicals')
    pmutations = request.get_cookie('prevPmutations')
    dnamutations = request.get_cookie('prevDNAmutations')
    snps = request.get_cookie('prevSNPs')

    diseases = str2bool(diseases)
    genes = str2bool(genes)
    chemicals = str2bool(chemicals)
    pmutations = str2bool(pmutations)
    dnamutations = str2bool(dnamutations)
    snps = str2bool(snps)

    try:
        network = DiseaseNetwork()
        top_results, top_result_types, top_result_articles = network.get_disease_info(disease, \
            diseases, genes, chemicals, pmutations, dnamutations, snps)

    except Exception as e:
        print >>stderr, e

    i = 0
    while top_results[i] != marker: i += 1
    articles = top_result_articles[i]
    
    all_titles = []
    all_dates = []
    
    MAGIC_NUMBER = 100
    article_str = ''

    articles_unique = []
    for article in articles:
        if article not in articles_unique:
            articles_unique.append(article)

    n = len(articles_unique)
    # print 'articles_unique length: ', n

    index = 0
    while index < len(articles_unique):

        # Call every hundred times
        if index % MAGIC_NUMBER == 0 and index != 0:
            
            titles = []
            success, titles = get_title(article_str)
            # Handle case where success is false
            if success == False: 
                article_str_array = article_str.split(',')
                for art in article_str_array:
                    titles.append('Not Found')

            dates = []
            success, dates = get_date(article_str)
            # Handle case where success is false
            if success == False:
                article_str_array = article_str.split(',')
                for art in article_str_array:
                    dates.append('Not Found')

            for title in titles:
                all_titles.append(title)
            for date in dates:
                all_dates.append(date)
            article_str = ''
    
        article = articles[index]
        if index == len(articles_unique) - 1 or (index % MAGIC_NUMBER) == (MAGIC_NUMBER -1): 
            append_me = str(article)
        else: append_me = str(article) + ','
        article_str += append_me
        index += 1

    # Last part
    success, titles = get_title(article_str)
    # Handle case where success is false
    if success == False:
        article_str_array = article_str.split(',')
        for art in article_str_array:
            titles.append('Not Found')

    success, dates = get_date(article_str)
    # Handle case where success is false
    if success == False:
        article_str_array = article_str.split(',')
        for art in article_str_array:
            dates.append('Not Found')

    for title in titles:
        all_titles.append(title)
    for date in dates:
        all_dates.append(date)

    # print 'titles length: ', len(all_titles)
    # print 'dates length: ', len(all_dates)

    # URL is valid, so proceed as usual
    templateInfo = {
        'articles': articles,
        'disease': disease.title(),
        'marker': marker.title(),
        'titles': all_titles,
        'dates': all_dates}

    return template('details.tpl', templateInfo)

@error(404)
def notFound(error):
    return 'Not Found'

if __name__ == '__main__':
    # if len(argv) != 2:
    #     print('Usage: ' + argv[0] + ' port')
    #     exit(1)

    # if not argv[1].isdigit():
    #     print('Usage: port not an int')
    #     exit(1)

    #run(host='0.0.0.0', port=argv[1], debug=True)
    port = os.environ.get('PORT', 5000)

    run(host='0.0.0.0', port=port)
    