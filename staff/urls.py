from django.conf.urls import url

from .views import login_view, loggedout_view, volunteer_list_view, email_view


urlpatterns = [


url(
        r'^$',login_view, name = 'login'#SignInView.as_view()
        ),

url( 
		r'^volunteer_list/$',volunteer_list_view, name='volunteer_list'
		),

url(
		r'^logout/',loggedout_view, name='logout'
		),


url(
		r'^send_email/',email_view, name='email'
		)
	

]
