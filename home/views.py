

# Create your views here.
from django.views.generic import ListView, TemplateView
from django.contrib.auth import authenticate, login, logout
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django_tables2 import RequestConfig
from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response


class HomePageView(TemplateView):
	template_name = 'pages/home.html'

	def get_context_data(self,*args,**kwargs):
		if self.request.method == 'GET':
			context = {"nav1_href":"signin" ,"nav1": "Volunteer Sign In", "signed_in": False, 'staff': 'Staff Login'}
			'''if not self.request.user.is_authenticated:
				context = {"nav1_href":"signin" ,"nav1": "Sign In", "signed_in": False}
			else:
				context = {"nav1_href":"users/signout", "nav1": "Logout", "signed_in": True}'''
		return context