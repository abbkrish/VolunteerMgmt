from django.conf.urls import url

from .views import SignInView, PostSignIn, signInView


urlpatterns = [

url( 
		r'^submit/',PostSignIn.as_view(), name='submit'
		),
url(
        r'^$',signInView, name = 'signin'#SignInView.as_view()
        ),

]
