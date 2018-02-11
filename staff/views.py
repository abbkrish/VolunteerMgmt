from django.shortcuts import render


from .forms import LogInForm, EmailForm
# Create your views here.

from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response, reverse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from volunteermgmtdjango.users.models import User

import json 

from django.core import serializers

from .models import EmailUsers, Emails

from signin.models import UserTable

from signin.models import SignedInUsers

from django.utils.html import mark_safe


from .services import Email 

# Create your views here.


#Since DateTime.date is not JSON serializable
def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError


@login_required(login_url = '/staff/')
def volunteer_list_view(request, format='json'):
    if request.user.is_authenticated and request.method == 'GET':
        queryset = SignedInUsers.objects.all().distinct('User__first_name', 'User__last_name', 'User__email', 'date', 'User__volunteer_group')
        values = queryset.values('User__first_name', 'User__last_name', 'User__email', 'date', 'User__volunteer_group')
        data = list(values)
        context = {'user_data': mark_safe(json.dumps(data, default = date_handler)), "staff_signed_in": True, "staff_logout": "Staff Logout"}
        return render(request,'staff/volunteer_list.html', context)
    

    elif request.method == 'POST' and request.user.is_authenticated:
        
        if 'emails' in request.session.keys():
            del request.session['emails']
        
        if EmailUsers.objects.count() > 0:
                EmailUsers.objects.all().delete()
        dat = json.loads(request.POST['data'])

        #iterate through dat to get the list of emails
        emails = []
        for i in dat:
            emails.append(i['User__email'])

        #get distinct emails
        distinct_emails = list(set(emails))
        emails_instance = EmailUsers.objects.create(emails = distinct_emails)
        return HttpResponseRedirect(reverse('staff:email'))
    else: 
        return redirect(reverse('staff:login'))



@login_required(login_url = '/staff/')
def email_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:

            #Selected emails from Emails Page
            email_instance = EmailUsers.objects.order_by('-loggedin_ts')[0]
            email_strings = ','.join(map(str,email_instance.emails))
            form = EmailForm(initial= {'recipients': email_strings})
            context = {"form": form, "staff_signed_in": True, "staff_logout": "Staff Logout"}            
            return render(request, 'staff/send_email.html', context)

    elif request.method == 'POST' and request.user.is_authenticated:
        form = EmailForm(request.POST)
        if form.is_valid():
            d = dict()
            d['message'] = form.cleaned_data['message']
            d['sender'] = form.cleaned_data['sender']
            d['cc_myself'] = form.cleaned_data['cc_myself']
            d['recipients'] = form.cleaned_data['recipients']
            d['subject'] = form.cleaned_data['subject']
            E = Email(**d)
            E.send_email()

            #Store email in Emails Database Table
            Emails.objects.create(subject = d['subject'], 
                                  message = d['message'],
                                  sender = d['sender'],
                                  recipients = d['recipients'],
                                  cc_myself = d['cc_myself'],
                                  )
            return HttpResponseRedirect(reverse('home:home_view'))
        else:
            return HttpResponseRedirect(reverse('staff:email'))

    return render(request, reverse('staff:email'), {})
    



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
            user = form.login(request)
            if user is not None:
                login(request, user)
                request.session['email'] = form.cleaned_data['email']

                #to indicate sigin in through sign in
                request.session['type'] = 'signing in'
                return HttpResponseRedirect(reverse('staff:volunteer_list'))
            else:

                return render(request, '404.html', {})
        else:
            context = {"form": form, 'staff': 'Staff Login'}
            return render(request, 'staff/staff_login.html', context)

        return render(request, reverse('home:home_view'))


def loggedout_view(request):
    logout(request)
    return redirect(reverse('home:home_view'))