from django.conf.urls import url

from . import views
from .views import signup_view

urlpatterns = [
    url(r'^signup/', signup_view, name='signup'),
]


