from django.shortcuts import render


from .forms import LogInForm, EmailForm
# Create your views here.

from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response, reverse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from volunteermgmtdjango.users.models import User

import json 

from django.core import serializers

from signin.models import UserTable

from signin.models import SignedInUsers

from django.utils.html import mark_safe

# Create your views here.


#Since DateTime.date is not JSON serializable
def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError


@login_required(login_url = '/staff/')
def volunteerListView(request, format='json'):
    if request.user.is_authenticated and request.method == 'GET':
        queryset = SignedInUsers.objects.all().distinct('User__first_name', 'User__last_name', 'User__email', 'date', 'User__volunteer_group')
        values = queryset.values('User__first_name', 'User__last_name', 'User__email', 'date', 'User__volunteer_group')
        data = list(values)
        table = UserTable(values)
       

      
        context = {'user_data': mark_safe(json.dumps(data, default = date_handler)), "staff_signed_in": True, "staff_logout": "Staff Logout"}
        return render(request,'staff/volunteer_list.html', context)
    elif request.method == 'POST' and request.user.is_authenticated:
        
       
        dat = json.loads(request.POST['data'])
        print(dat, " Post dat")

        #iterate through dat to get the list of emails
        emails = []
        for i in dat:
            emails.append(i['User__email'])

        #get distinct emails
        distinct_emails = list(set(emails))
        context = {'emails': distinct_emails, "staff_signed_in": True, "staff_logout": "Staff Logout"
                   }
        request.session['emails'] = distinct_emails
        print(request.session['emails'], " Post")
        return HttpResponseRedirect(reverse('staff:email'))
    else: 
        return redirect(reverse('staff:login'))



@login_required(login_url = '/staff/')
def email_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:

            #Selected emails from Emails Page
            emails = []
            if 'emails' in request.session.keys():
                emails = request.session['emails']
            print(emails, "Get")
            email_strings = ''
            for j,s in enumerate(emails):
                email_strings += s 
                if j < len(emails) - 1:
                    email_strings += ','
            form = EmailForm(initial= {'recipients': email_strings})
            context = {"form": form, "staff_signed_in": True, "staff_logout": "Staff Logout"}
            return render(request, 'staff/send_email.html', context)

    elif request.method == 'POST' and request.user.is_authenticated:
        pass

    return render(request, reverse('staff:email'), {})
    pass



def login_view(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect(reverse('staff:volunteer_list'))
        form = LogInForm()
        context = {"form": form, 'staff': 'Staff Login'}
        return render(request, 'staff/staff_login.html', context)
    else:
        form = LogInForm(request.POST)
        if form.is_valid():

            volunteer = User.objects.get(email=form.cleaned_data['email'])
            if volunteer.is_staff == True:
                try:
                    user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])                
                except:
                    return redirect('/403')
                if user is not None:
                    login(request, user)
                    request.session['email'] = form.cleaned_data['email']

                    #to indicate sigin in through sign in
                    request.session['type'] = 'signing in'
                    return HttpResponseRedirect(reverse('staff:volunteer_list'))
                else:

                    return render(request, '404.html', {})

        return render(request, "##")


def loggedout_view(request):
    logout(request)
    return redirect(reverse('home:home_view'))