from django.conf.urls import url

from .views import SignInView, PostSignIn, sign_in_view


urlpatterns = [

url( 
		r'^submit/',PostSignIn.as_view(), name='submit'
		),
url(
        r'^$',sign_in_view, name = 'signin'#SignInView.as_view()
        ),

]
