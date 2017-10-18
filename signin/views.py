from django.shortcuts import render

from volunteermgmtdjango.users.models import User

import json 
from django.views.generic import ListView, TemplateView
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django_tables2 import RequestConfig
from django_tables2 import SingleTableView
from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response, HttpResponse
from django.core import serializers
from .models import UserTable
from django.utils.html import mark_safe
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from django_filters.views import FilterView
from .filters import UserFilter
# Create your views here.




def signInView(request):
	queryset = User.objects.filter(is_staff=False)
	values = queryset.values('first_name', 'last_name', 'email', 'waiver_filed', 'volunteer_group')
	data = list(values)
	table = UserTable(values)
	#table.paginate(per_page=1)
	#RequestConfig(request).configure(table)
	#json = json.dumps(data)
	#json = serializers.serialize('json', data)
	context = {'user_data': mark_safe(json.dumps(data)),
               }
	return render(request,'pages/signin.html', context)
	#return render(request,'pages/signin.html', {'table':table})



class SignInView(SingleTableView, FilterView):
	template_name = 'pages/signin.html'

	model = User
	table_class = UserTable
	filterset_class = UserFilter

	#def get_table_data(self):
		#f = filters.UserFilter()

	def get_context_data(self,*args,**kwargs):
		context = super(SignInView, self).get_context_data(**kwargs)
		queryset = User.objects.all()
		table = UserTable(queryset)
		#RequestConfig(self.request).configure(table)
		context['table'] = table
		return context

	#def get(self,*args,**kwargs):
		#my_filter = UserFilter(self.request.GET)
		#my_choice = 



'''
class SignInView(TemplateView):
	template_name = 'pages/signin.html'

	def get_context_data(self,*args,**kwargs):
		context = super(SignInView, self).get_context_data(**kwargs)
		queryset = User.objects.all()
		table = UserTable(queryset)
		#RequestConfig(self.request).configure(table)
		context['table'] = table
		return context
'''

class PostSignIn(TemplateView):


	
	template_name = 'pages/signed_in_user.html'
	def get(self, *args, **kwargs):
		context = {}
		return render(self.request,'pages/signed_in_user.html', context)
	def get_context_data(self,*args,**kwargs):
		context = super(SignInView, self).get_context_data(**kwargs)
		volunteer = Volunteer.objects.get(email= request.session['email'])
		context = {'vname': volunteer.first_name + ' ' + volunteer.last_name, 'type': self.request.session['type'], 'nav2': 'home'}
		return context

	def post(self, *args, **kwargs):
		context = {}
		print(self.request.POST)
		#return render(self.request,'pages/home.html', context)
		#redirect('home/')
		return HttpResponseRedirect('/home')
