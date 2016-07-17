from django.shortcuts import render
#from django.contrib.auth.decorators import login_required
#from django.core.context_processors import csrf
#from datetime import datetime
from django.http import HttpResponse
import json
import time
from django.core import serializers
from models import * 
from django.views.decorators.cache import cache_page

#import datetime
# Create your views here.

QUICKBLOCK = 75000

#@login_required
def oai(request):
	return render(request, 'oai/oai.html')

def oai_size(request):
	return HttpResponse(str(AbstractModel.objects.count()))

def oai_rate(request):
	identifier = request.GET['identifier']
	rating = int(request.GET['rating'])
	query = AbstractModel.objects.filter(identifier=identifier)
	queryCache = AbstractCacheModel.objects.filter(identifier=identifier)
	if rating < 0:
		rating = None

	query.update(rating = rating)
	queryCache.update(rating = rating)

	createCacheFromQuery(query.filter(cached=0))
	
	if query.count() is 0:
		return HttpResponse("Error: The database does not contain the item you wish to rate.");
	return HttpResponse("oai_rate");



#@cache_page(60 * 5)
def oai_filter(request):
	startTime = time.time();

	abstractFilters = request.GET['abstract'].split(',')
	titleFilters = request.GET['title'].split(',')
	authorsFilters = request.GET['authors'].split(',')
	cateFilters = request.GET['cate'].split(',')
	since = request.GET['since']
	until = request.GET['until']
	quickIndex = int(request.GET['quickIndex'])

	query = AbstractModel.objects.filter(cached=False)

	header = {}
	header['querySize'] = query.count()

	query = query.filter(pk__gte = quickIndex)
	query = query.filter(pk__lt = quickIndex + QUICKBLOCK)
	
	if since != "":
		query = query.filter(datestamp__gte = since)

	if until != "":
		query = query.filter(datestamp__lte = until)

	for fil in abstractFilters:
		query = query.filter(abstract__icontains = fil)
	for fil in titleFilters:
		query = query.filter(title__icontains = fil)
	for fil in authorsFilters:
		query = query.filter(authors__icontains = fil)
	for fil in cateFilters:
		query = query.filter(categories__icontains = fil)


	query = query.values('identifier','title', 'abstract', 'authors', 'rating')

	body = list(query)

	header['time'] = time.time() - startTime

	response = json.dumps({'header':header, 'body':body})
	return HttpResponse(response)



def oai_cache(request):
	startTime = time.time();

	abstractFilters = request.GET['abstract'].split(',')
	titleFilters = request.GET['title'].split(',')
	authorsFilters = request.GET['authors'].split(',')
	cateFilters = request.GET['cate'].split(',')
	since = request.GET['since']
	until = request.GET['until']

	query = AbstractCacheModel.objects

	header = {}
	header['querySize'] = AbstractModel.objects.count()

	if since != "":
		query = query.filter(datestamp__gte = since)

	if until != "":
		query = query.filter(datestamp__lte = until)

	for fil in abstractFilters:
		query = query.filter(abstract__icontains = fil)
	for fil in titleFilters:
		query = query.filter(title__icontains = fil)
	for fil in authorsFilters:
		query = query.filter(authors__icontains = fil)
	for fil in cateFilters:
		query = query.filter(categories__icontains = fil)


	query = query.values('identifier','title', 'abstract', 'authors', 'rating')

	body = list(query)

	header['time'] = time.time() - startTime

	response = json.dumps({'header':header, 'body':body})
	return HttpResponse(response)

