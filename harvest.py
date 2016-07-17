# execute by logging into the django shell:
# python manage.py shell
# then execute
# execfile('harvest.py')

import requests
import time
import xml.etree.ElementTree as ET
import json
from oai.models import *
#import os
#os.environ.setdefault(r'DJANGO_SETTINGS_MODULE', r'phy_arxiv.settings')

#import django
#django.setup()



def errorHarvest(output):
    errorMessage = r'Retry after 20 seconds'
    return errorMessage in output

def getURL(verb, metadataPrefix, fromStr = None, untilStr = None, setStr = None):
    requestURL = r'http://export.arxiv.org/oai2'
    requestURL += r'?verb=' + verb
    requestURL += r'&metadataPrefix=' + metadataPrefix
    if fromStr is not None:
        requestURL += r'&from=' + fromStr
    if untilStr is not None:
        requestURL += r'&until=' + untilStr
    if setStr is not None:
        requestURL += r'&set=' + setStr
    return requestURL

def getOutput(verb, metadataPrefix, fromStr = None, untilStr = None, setStr = None):
    requestURL = getURL(verb, metadataPrefix, fromStr, untilStr, setStr)
    
    noResponse = True
    while noResponse:
        response = requests.get(requestURL)
        output = response.content
        noResponse = errorHarvest(output)
        if noResponse:
            time.sleep(25)    
    return output

def getText(element):
    if element == None:
        return None
    else:
        return element.text

def dateToStr(date):
    if date == None:
        return None
    return str(date)

output = getOutput(verb = 'ListRecords', metadataPrefix = 'arXiv', fromStr = '2000-01-01', setStr = 'physics')

starttime = time.time()

root = ET.fromstring(output)

#root = ET.parse(r'test.xml')

ns = {r'root':r'http://www.openarchives.org/OAI/2.0/', r'arXiv':r'http://arxiv.org/OAI/arXiv/'}

abstractObjList = []
#pkList = []
for record in root.iter(r'{' + ns[r'root'] + r'}record'):
    header = record.find(r'root:header', ns)
    datestamp = getText(header.find(r'root:datestamp', ns))

    entry = record.find(r'root:metadata', ns).find(r'arXiv:arXiv', ns)
    identifier = getText(entry.find(r'arXiv:id', ns))
    created = getText(entry.find(r'arXiv:created', ns))
    title = getText(entry.find(r'arXiv:title', ns))
    abstract = getText(entry.find(r'arXiv:abstract', ns))

    categories = json.dumps(getText(entry.find(r'arXiv:categories', ns)).split())

    authorsElement = entry.find(r'arXiv:authors', ns).findall(r'arXiv:author', ns)
    authors = []
    for authorElement in authorsElement:
        keyname = getText(authorElement.find(r'arXiv:keyname', ns))
        forenames = getText(authorElement.find(r'arXiv:forenames', ns))
        authors.append({r'keyname': keyname, r'forenames': forenames})
    authors = json.dumps(authors)

    licenseStr = getText(entry.find(r'arXiv:license', ns))
    updated = getText(entry.find(r'arXiv:updated', ns))
    comments = getText(entry.find(r'arXiv:comments', ns))
    journalRef = getText(entry.find(r'arXiv:journal-ref', ns))
    doi = getText(entry.find(r'arXiv:doi', ns))

    query = AbstractModel.objects.filter(identifier = identifier)
    deleteTheRest = False
    doNothing = False
    for obj in query:
        if deleteTheRest:
            obj.delete()
            continue
        deleteTheRest = True
        if not [dateToStr(obj.datestamp), obj.identifier, dateToStr(obj.created), obj.title,
            obj.licenseStr, obj.abstract, dateToStr(obj.updated), obj.comments,
            obj.journalRef, obj.doi, obj.categories, obj.authors] == [datestamp, identifier, created, title, licenseStr, abstract,
             updated, comments, journalRef, doi, categories, authors]:
            obj.datestamp = datestamp
            obj.identifier = identifier
            obj.created = created
            obj.title = title
            obj.licenseStr = licenseStr
            obj.abstract = abstract
            obj.updated = updated
            obj.comments = comments
            obj.journalRef = journalRef
            obj.doi = doi
            obj.categories = categories
            obj.authors = authors
            obj.save()
        else:
            doNothing = True
                
    if doNothing:
        continue

    abstractObj = AbstractModel(datestamp = datestamp, identifier = identifier,
                                    created = created, title = title,
                                    licenseStr = licenseStr, abstract = abstract,
                                    updated = updated, comments = comments,
                                    journalRef = journalRef, doi = doi,
                                    categories = categories, authors = authors)
    abstractObjList.append(abstractObj)


#AbstractModel.objects.filter(pk__in = pkList).delete()
AbstractModel.objects.bulk_create(abstractObjList)

print (time.time() - starttime)
