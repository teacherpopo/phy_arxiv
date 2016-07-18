from oai.models import *

def createCacheFromQuery(abstractQuery):
        cacheList = []
        for abstractObj in abstractQuery:
                if abstractObj.cached is False:
                        cacheList.append(AbstractCacheModel(datestamp = abstractObj.datestamp, identifier = abstractObj.identifier, created = abstractObj.created,
                                          title = abstractObj.title, authors = abstractObj.authors, abstract = abstractObj.abstract,
                                          categories = abstractObj.categories, licenseStr = abstractObj.licenseStr, updated = abstractObj.updated,
                                          comments = abstractObj.comments, journalRef = abstractObj.journalRef, doi = abstractObj.doi, reportNo = abstractObj.reportNo,
                                          rating = abstractObj.rating, rated = abstractObj.rated, archived = abstractObj.archived,
                                          MSCClass = abstractObj.MSCClass, ACMClass = abstractObj.ACMClass))
        abstractQuery.update(cached = 1)

        AbstractCacheModel.objects.bulk_create(cacheList)

