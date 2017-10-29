from django.db import models

# Create your models here.
import django_tables2 as tables
from django_tables2.utils import A

from django.contrib.postgres.fields import ArrayField
from volunteermgmtdjango.users.models import User

from .fields import MultiEmailField

class EmailUsers(models.Model):
	emails = ArrayField((models.CharField(max_length=10000)))
	loggedin_ts = models.DateTimeField(auto_now_add=True)
	date = models.DateField(auto_now_add=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)





class Emails(models.Model):
	subject = models.CharField(max_length=1000, default = '')
	message = models.CharField(max_length = 100000, default ='')
	sender = models.EmailField(default = '')
	recipients = ArrayField(models.EmailField())
	cc_myself = models.BooleanField(default = False)
	loggedin_ts = models.DateTimeField(auto_now_add=True)
	date = models.DateField(auto_now_add=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)