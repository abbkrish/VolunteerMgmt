from django.conf.urls import url

from .views import homepage_view


urlpatterns = [


url(
        r'^~home/$',homepage_view
        ),
]
