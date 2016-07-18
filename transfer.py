
import time
import string
import json
import mysql.connector
from oai.models import *

errors = []
names = ['arXiv:', 'Date:', 'Title:', 'Authors:','Categories:','Comments:','Report-no:',
         'DOI:','Journal-ref:','MSC-class:', 'ACM-class:', r'\\']

def removeBracketContent(content):
    init = -1
    final = -1
    index = 0
    for i in range(len(content)):
        if content[i] == '(':
            if init < 0:
                init = i
            index += 1
        elif content[i] == ')':
            index -= 1
            if index == 0:
                final = i
                break
    
    if init < 0 or final < 0:
        return content
    if init > final:
        return content
    
    content = content[:init] + content[(final+1):]
    return removeBracketContent(content)

def trim(name, content):
    if name == "identifier":
        index1 = content.find(' ')
        index2 = content.find('replaced')
        index = -1
        if index1 < 0 and index2 < 0:
            return content
        else:
            if index1 >= 0 and index2 >= 0:
                index = min(index1, index2)
            else:
                index = max(index1, index2)
            return content[:index].strip()
    elif name == "authors":
        content = content.replace(', and ', ', ')
        content = content.replace(' and ', ', ')
        content = removeBracketContent(content)
        content = content.split(',')
        for i in range(len(content)):
            one = content[i]
            one = one.strip()
            keyname = ''
            forenames = ''
            for j in reversed(range(len(one))):
                if one[j] == ' ':
                    keyname = one[j:].strip()
                    forenames = one[:j].strip()
                    break
            content[i] = {'keyname':keyname,'forenames':forenames}
        return json.dumps(content)
    else:
        return content

def findAbstract(mailing):
    mailing = mailing
    index = mailing.find('\n\\\\\n')
    residue = mailing[(index+4):]
    indexEnd = residue.find('\n\\\\')
    cut = residue[:indexEnd].strip()
    if 'Title:' in cut:
        return None
    return cut
    

def findItem(name, mailing, identifier="NO_ID"):
    NAME = name + ':'
    index = mailing.find(NAME)
    if index < 0:
        return None
    
    residue = mailing[(index + len(NAME)):]
    indexEnd = len(residue)
    for post in names:
        tmp = residue.find(post)
        if tmp == -1:
            tmp = len(residue)
	indexEnd = min(indexEnd, tmp)


    if indexEnd < 0:
	errors.append(identifier)
	return None
    
    cut = residue[:indexEnd].strip()
    cut = cut.replace('\n', '')
    cut = cut.replace('  ',' ')
    return cut

starttime = time.time()


cnx = mysql.connector.connect(host='localhost', user='root', password='utsg9800BAI*', database='arxiv')

curA = cnx.cursor()
curA.execute(r'SELECT datestamp, abstracts_id, rating FROM annotations WHERE annotation="ssgubser"')

annoObjList = {}
for (rated, abstractId, rating) in curA:
    annoObjList[abstractId] = {"rating":rating, "rated":str(rated)[:10]}
curA.close()

cur = cnx.cursor()
cur.execute(r'SELECT id, datestamp, abstract FROM abstracts')


abstractObjList = []
for (abstractId, datestamp, mailing) in cur:
    datestamp = str(datestamp)[:10]
    identifier = trim("identifier", findItem('arXiv', mailing))
    created = None
    title = findItem('Title', mailing, identifier)
    authors = trim("authors", findItem('Authors', mailing, identifier))
    abstract = findAbstract(mailing)
    
    categories = findItem('Categories', mailing, identifier)
    licenseStr = None
    updated = None
    comments = findItem('Comments', mailing, identifier)
    reportNo = findItem('Report-no', mailing, identifier)
    journalRef = findItem('Journal-ref', mailing, identifier)
    doi = findItem('DOI', mailing, identifier)
    MSCClass = findItem('MSC-class', mailing, identifier)
    ACMClass = findItem('ACM-class', mailing, identifier)

    rating = None
    rated = None
    if abstractId in annoObjList:
        rating = annoObjList[abstractId]['rating']
        rated = annoObjList[abstractId]['rated']
    archived = False

    cached = False

    abstractObj = AbstractModel(datestamp = datestamp, identifier = identifier,
                                    created = created, title = title, authors = authors,
                                    abstract = abstract,
                                    categories = categories, licenseStr = licenseStr, 
                                    updated = updated, comments = comments,
                                    reportNo = reportNo, journalRef = journalRef, doi = doi,
                                    MSCClass = MSCClass, ACMClass = ACMClass,
                                    rating = rating, rated = rated, archived = archived,
                                    cached = cached)
    abstractObjList.append(abstractObj)

AbstractModel.objects.bulk_create(abstractObjList)




cur.close()
cnx.close()
print (time.time() - starttime)
