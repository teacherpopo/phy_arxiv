from django.db import models

# Create your models here.

#class CacheModel(models.Model):
#	dateCached = models.DateField(db_index = True, null = True, default = None)
#	abstractObj = models.ForeignKey('AbstractModel', on_delete=models.CASCADE)


class AbstractCacheModel(models.Model):
	# mandatory metedata fields
	datestamp = models.DateField(db_index = True, null = True, default = None)
	identifier = models.CharField(null = True, max_length = 15, default = None)
	created = models.DateField(null = True, default = None)
	title = models.CharField(null = True, max_length = 300, default = None)
	authors = models.TextField(null = True, default = None) # JSON format
	abstract = models.TextField(null = True, default = None)

	# optional metadata fields
	categories = models.TextField(null = True, default = None) # JSON format
	licenseStr = models.CharField(null = True, max_length = 300, default = None)
	updated = models.DateField(null = True, default = None)
	comments = models.TextField(null = True, default = None)
	journalRef = models.CharField(null = True, max_length = 300, default = None)
	doi = models.CharField(null = True, max_length = 300, default = None)
	reportNo = models.CharField(null = True, max_length = 100, default = None)

	# ratings
	rating = models.IntegerField(null = True, default = None)
	rated = models.DateField(null = True, default = None)
	archived = models.BooleanField(null = False, default = False)

	# math
	MSCClass = models.CharField(null = True, max_length = 100, default = None)
	# computer science
	ACMClass = models.CharField(null = True, max_length = 100, default = None)



class AbstractModel(models.Model):
	# mandatory metedata fields
	datestamp = models.DateField(db_index = True, null = True, default = None)
	identifier = models.CharField(null = True, max_length = 15, default = None)
	created = models.DateField(null = True, default = None)
	title = models.CharField(null = True, max_length = 300, default = None)
	authors = models.TextField(null = True, default = None) # JSON format
	abstract = models.TextField(null = True, default = None)

	# optional metadata fields
	categories = models.TextField(null = True, default = None) # JSON format
	licenseStr = models.CharField(null = True, max_length = 300, default = None)
	updated = models.DateField(null = True, default = None)
	comments = models.TextField(null = True, default = None)
	journalRef = models.CharField(null = True, max_length = 300, default = None)
	doi = models.CharField(null = True, max_length = 300, default = None)
	reportNo = models.CharField(null = True, max_length = 100, default = None)

	# ratings
	rating = models.IntegerField(null = True, default = None)
	rated = models.DateField(null = True, default = None)
	archived = models.IntegerField(null = False, default = 0)

	# math
	MSCClass = models.CharField(null = True, max_length = 100, default = None)
	# computer science
	ACMClass = models.CharField(null = True, max_length = 100, default = None)

	cached = models.IntegerField(null = False, default = 0)

	#class Meta:
	#	ordering = ['datestamp']


def createCacheFromQuery(abstractQuery):
        cacheList = []
        for abstractObj in abstractQuery:
                cacheList.append(AbstractCacheModel(datestamp = abstractObj.datestamp, identifier = abstractObj.identifier, created = abstractObj.created,
                                  title = abstractObj.title, authors = abstractObj.authors, abstract = abstractObj.abstract,
                                  categories = abstractObj.categories, licenseStr = abstractObj.licenseStr, updated = abstractObj.updated,
                                  comments = abstractObj.comments, journalRef = abstractObj.journalRef, doi = abstractObj.doi, reportNo = abstractObj.reportNo,
                                  rating = abstractObj.rating, rated = abstractObj.rated, archived = abstractObj.archived,
                                  MSCClass = abstractObj.MSCClass, ACMClass = abstractObj.ACMClass))
        abstractQuery.update(cached = 1)

        AbstractCacheModel.objects.bulk_create(cacheList)




