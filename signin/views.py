from django.shortcuts import render

from volunteermgmtdjango.users.models import User

import json 

from django.contrib.auth import login, logout
from django.views.generic import ListView, TemplateView
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django_tables2 import RequestConfig
from django_tables2 import SingleTableView
from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response, HttpResponse, reverse
from django.core import serializers


from staff.forms import LogInForm
from .models import UserTable
from .models import SignedInUsers
from django.utils.html import mark_safe
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from django_filters.views import FilterView
from .filters import UserFilter
# Create your views here.



@login_required(login_url = '/signin/staff/')
def sign_in_view(request):
    queryset = User.objects.filter(is_staff=False, is_active=True)
    values = queryset.values('first_name', 'last_name', 'email', 'waiver_filed', 'volunteer_group')
    data = list(values)
    context = {'user_data': mark_safe(json.dumps(data)),"staff_logout": "Staff Logout", "staff_signed_in": True,
               }
    return render(request,'pages/signin.html', context)




def staff_login_view(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('signin:signin'))
        form = LogInForm()
        context = {"form": form, 'staff': 'Staff Login'}
        return render(request, 'pages/staff_login_signin.html', context)
    else:
        form = LogInForm(request.POST)
        
        if form.is_valid():
            user = form.login(request)
            print("in staff post login view(request):")
            if user is not None:
                login(request, user)
                request.session['email'] = form.cleaned_data['email']

                #to indicate sigin in through sign in
                request.session['type'] = 'signing in'
                return HttpResponseRedirect(reverse('signin:signin'))
            else:

                return render(request, '404.html', {})
        else:
            context = {"form": form, 'staff': 'Staff Login'}
            return render(request, 'pages/staff_login_signin.html', context)

        return render(request, reverse('home:home_view'))

    

class SignInView(SingleTableView, FilterView):
    template_name = 'pages/signin.html'

    model = User
    table_class = UserTable
    filterset_class = UserFilter

    def get_context_data(self,*args,**kwargs):
        context = super(SignInView, self).get_context_data(**kwargs)
        queryset = User.objects.all()
        table = UserTable(queryset)
        context['table'] = table
        return context


class PostSignIn(TemplateView):

    
    def get(self, *args, **kwargs):
        sign_in_instance = ' ' + 'null' + ' ' 
        signin_instance = SignedInUsers.objects.latest('loggedin_ts')
        context = {'type':'signing in', 'vname':signin_instance.User.first_name + ' ' + signin_instance.User.last_name}
        return render(self.request,'pages/signed_in_user.html', context)


    def post(self, *args, **kwargs):
        self.request.session.flush()
        email_key = self.request.POST['data[email]']
        self.request.session['first_name'] = self.request.POST['data[first_name]']
        self.request.session['last_name'] = self.request.POST['data[last_name]']

        #Add to Sign In Logs
        user = User.objects.get(email=email_key)
        signin_instance = SignedInUsers.objects.create(User = user)
        return redirect('signin:submit')
