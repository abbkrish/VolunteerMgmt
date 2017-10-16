from django_filters import rest_framework as filters
from django.db import models

# Create your models here.
import django_tables2 as tables
from django_tables2.utils import A

from volunteermgmtdjango.users.models import User

class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'volunteer_group')