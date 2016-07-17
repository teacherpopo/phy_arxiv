
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phy_arxiv.settings")

from django.contrib.auth.models import Group
if not Group.objects.filter(name='staff').exists():
	Group.objects.create(name='staff')
if not Group.objects.filter(name='students').exists():
	Group.objects.create(name='students')