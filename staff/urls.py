from django.conf.urls import url

from .views import login_view, loggedout_view, volunteerListView, email_view


urlpatterns = [


url(
        r'^$',login_view, name = 'login'#SignInView.as_view()
        ),

url( 
		r'^volunteer_list/$',volunteerListView, name='volunteer_list'
		),

url(
		r'^logout/',loggedout_view, name='logout'
		),


url(
		r'^send_email/',email_view, name='email'
		)
	

]
