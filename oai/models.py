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
	MSCClass = models.CharField(null = True, max_length = 100, default = None)
	ACMClass = models.CharField(null = True, max_length = 100, default = None)

	# ratings
	rating = models.IntegerField(null = True, default = None)
	rated = models.DateField(null = True, default = None)
	archived = models.BooleanField(null = False, default = False)




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
	MSCClass = models.CharField(null = True, max_length = 100, default = None)
	ACMClass = models.CharField(null = True, max_length = 100, default = None)

	# ratings
	rating = models.IntegerField(null = True, default = None)
	rated = models.DateField(null = True, default = None)
	archived = models.IntegerField(null = False, default = 0)

	# cache
	cached = models.IntegerField(null = False, default = 0)

	#class Meta:
	#	ordering = ['datestamp']


