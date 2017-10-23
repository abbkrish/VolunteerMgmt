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
    form = SubmitForm()
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        else:
            form = SubmitForm()
            context = {"nav1": "Login", "form": form}
            return render(request,'pages/signup.html', context)
    else:
        form = SubmitForm(request.POST, initial={"password":'NULL', "confirm_password": 'NULL'})
        context = {"nav1": "Login", "form": form}
        if form.is_valid():
            print("valid")
            new_volunteer = User(first_name = form.cleaned_data['first_name'],
                                      last_name = form.cleaned_data['last_name'],
                                      email = form.cleaned_data['email'],
                                      street_address_1 = form.cleaned_data['street_addr_1'],
                                      street_address_2 = form.cleaned_data['street_addr_2'],
                                      zipcode = form.cleaned_data['zipcode'],
                                      waiver_filed = form.cleaned_data['waiverfiled'],
                                      volunteer_group = form.cleaned_data['volunteergroup'],
                                      city = form.cleaned_data['city'],
                                      state = form.cleaned_data['state']
                                      )
            #XXX: removed password hence commented this line 
            #new_volunteer.set_password(form.cleaned_data['password'])
            
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
            print(form.errors.as_data())
            return render(request,'signup.html', context)



