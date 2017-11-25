from django.db import models
from datetime import datetime

# Create your models here.
import django_tables2 as tables
from django_tables2.utils import A

from volunteermgmtdjango.users.models import User

class UserTable(tables.Table):

	Select = tables.CheckBoxColumn()
	'''
	first_name = tables.CheckBoxColumn()
	last_name = tables.CheckBoxColumn()
	email = tables.CheckBoxColumn()
	waiver_filed = tables.CheckBoxColumn()
	volunteer_group = tables.CheckBoxColumn()
	'''
	class Meta:
		model = User
		attrs = {"class": "table-striped table-bordered"} 
		fields = {'first_name', 'last_name', 'email', 'waiver_filed', 'volunteer_group', 'Select'}



class SignedInUsers(models.Model):
	User = models.ForeignKey(User, on_delete = models.CASCADE)
	loggedin_ts = models.DateTimeField(auto_now_add=True)
	date = models.DateField(auto_now_add=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now_add=True)


