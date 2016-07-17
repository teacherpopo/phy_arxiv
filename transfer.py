# execute by logging into the django shell:
# python manage.py shell
# then execute
# execfile('harvest.py')

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
cur = cnx.cursor()

cur.execute(r'SELECT id, datestamp, abstract FROM abstracts WHERE id')

abstractObjList = []
for (identity, datestamp, mailing) in cur:
    datestamp = str(datestamp)[:10]
    identifier = trim("identifier", findItem('arXiv', mailing))
    #created = trim("created", findItem('Date', mailing, identifier))
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

    abstractObj = AbstractModel(datestamp = datestamp, identifier = identifier,
                                    created = created, title = title,
                                    licenseStr = licenseStr, abstract = abstract,
                                    updated = updated, comments = comments,
                                    journalRef = journalRef, doi = doi,
                                    categories = categories, authors = authors,
                                    MSCClass = MSCClass, ACMClass = ACMClass, reportNo = reportNo)
    abstractObjList.append(abstractObj)

AbstractModel.objects.bulk_create(abstractObjList)
#cur.execute(r'SELECT datestamp, abstracts_id, rating FROM annotations WHERE annotation="ssgubser"')




#for row in cur.fetchall()[:10]:
#    print row

cur.close()
cnx.close()
print (time.time() - starttime)
