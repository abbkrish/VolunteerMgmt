from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from signin.models import SignedInUsers

from .forms import SubmitForm
from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'



## TODO Later : Fix the issue where transaction isnt rolled back on failure
def signup_view(request):
    volunteer_group_list = ('Christ Church', 'Newark Academy', 'New Volunteers', 'World Wide Orphans', 
      'Congregation Beth El','Investors', 'Seton Hall Nursing', 'Freewalkers', 'Carpenter Club', 
      'Clarity', 'Arturo\'s','Temple Sharey Tefilo','Congregation B\'nai Jesurun' )
    
    if request.method == 'GET':
        form = SubmitForm(data_list = volunteer_group_list)
        context = {"form": form}
        return render(request,'pages/signup.html', context)
    else:
        
        form = SubmitForm(request.POST, initial={"password":'NULL', "confirm_password": 'NULL'})
        context = {"nav1": "Login", "form": form}
        if form.is_valid() and form.valid_username(form.cleaned_data['email']) and form.check_minor_certification(form.cleaned_data['minor'], form.cleaned_data['parents_signature']):
            new_volunteer = User(first_name = form.cleaned_data['first_name'],
                                      last_name = form.cleaned_data['last_name'],
                                      email = form.cleaned_data['email'],
                                      street_address_1 = form.cleaned_data['street_addr_1'],
                                      street_address_2 = form.cleaned_data['street_addr_2'],
                                      zipcode = form.cleaned_data['zipcode'],
                                      waiver_filed = form.cleaned_data['waiverfiled'],
                                      need_community_svc_hrs = form.cleaned_data['need_community_svc_hrs'],
                                      volunteer_group = form.cleaned_data['volunteergroup'],
                                      city = form.cleaned_data['city'],
                                      state = form.cleaned_data['state'],
                                      emergency_name = form.cleaned_data['emergency_name'],
                                      accept_terms  = form.cleaned_data['accept_terms'],
                                      parents_signature = form.cleaned_data['parents_signature']
                                      )
            #XXX: removed password hence commented this line 
            #new_volunteer.set_password(form.cleaned_data['password'])
            if not form.cleaned_data['phone_number'].startswith('+1'):
              new_volunteer.phone_number = '+1{}'.format(form.cleaned_data['phone_number'])
            else:
              new_volunteer.phone_number = form.cleaned_data['phone_number']


            if not form.cleaned_data['emergency_phone'].startswith('+1'):
              new_volunteer.emergency_phone = '+1{}'.format(form.cleaned_data['emergency_phone'])
            else:
              new_volunteer.emergency_phone = form.cleaned_data['emergency_phone']



            new_volunteer.save()

            #No login needed
            #request.session['email'] = new_volunteer.email
            #to indicate sigin in through new registration
            #request.session['type'] = 'signing up'
            #user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            #login(request, new_volunteer)
            #logout(request)
            signin_instance = SignedInUsers.objects.create(User = new_volunteer)
            return render(request, 'pages/signed_up.html', context = {"type":"signing up", "vname":form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name']})

        else:
            context['form'] = form
            return render(request,'pages/signup.html', context)



