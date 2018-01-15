from django import forms

from django.contrib.auth.hashers import make_password

import floppyforms

from django.core import validators

from django.db import models

from .models import User

from .fields import ListTextWidget, OptionalChoiceField

from phonenumber_field.modelfields import PhoneNumberField


class SubmitForm(forms.Form):
    first_name = forms.CharField(label='first_name', max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Enter your First name'}))
    last_name = forms.CharField(label='last_name', max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Enter your Last name'}))
    email = forms.EmailField(label='email', widget=forms.TextInput(attrs={'placeholder': 'Enter your Email'}))
    street_addr_1 = forms.CharField(label='addr1', max_length = 500, widget=forms.TextInput(attrs={'placeholder': 'Street Address, PO Box, Company Name'}))
    street_addr_2 = forms.CharField(label='addr2', max_length = 500, widget=forms.TextInput(attrs={'placeholder': 'Apartment, Unit '}))
    city = forms.CharField(label='city', max_length = 500, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    state = forms.CharField(label='state', max_length = 500, widget=forms.TextInput(attrs={'placeholder': 'State'}))
    zipcode = forms.CharField(label='zipcode', max_length = 100, widget=forms.TextInput(attrs={'placeholder': '5 digit zipcode'}))
    need_community_svc_hrs = forms.BooleanField(label='waiver', required=False)
    phone_number = forms.CharField(label='phone', max_length = 500, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    volunteergroup = OptionalChoiceField(choices=(ListTextWidget.get_choices_list()), max_length=200)
    #volunteergroup = forms.CharField(label='volunteergroup', max_length = 500)
    emergency_name =forms.CharField(label='emergency_name', max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Emergency Contact name'}))
    emergency_phone = forms.CharField(label='emergency_phone', max_length = 500, widget=forms.TextInput(attrs={'placeholder': 'Emergency Contact Phone Number'}))
    waiverfiled = forms.BooleanField(label='waiver', required=False)
    other = forms.CharField(label='other', max_length = 500, required=False, widget=forms.TextInput(attrs={'placeholder': 'Other'}))
    
    #password = forms.CharField(label='pwd', max_length = 300, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'}), initial = 'NULL')
    #confirm_password = forms.CharField(label = "c_pwd", max_length = 300, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your Password'}), initial='NULL')



    def __init__(self, *args, **kwargs):
        _volunteer_group_list = kwargs.pop('data_list', None)
        super(SubmitForm, self).__init__(*args, **kwargs)
        #print(_volunteer_group_list)
        #self.fields['volunteergroup'].widget= floppyforms.widgets.Input(datalist=ListTextWidget.getDataList())
        #self.fields['volunteergroup'].widget = ListTextWidget(data_list=_volunteer_group_list, name='volunteer_group_list')

    class Meta:
        model = User
        fields = ('email')
        #widgets = {
            #'volunteergroup': floppyforms.widgets.Input(datalist=ListTextWidget.getDataList())
        #}
        


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


    
    def valid_username(self, email):
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already in use')
            return False
        return True

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(SubmitForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



class SignInForm(forms.Form):
    email = forms.EmailField(label='email', widget=forms.TextInput(attrs={'placeholder': 'Enter your Email'}))
    password = forms.CharField(label='pwd', max_length = 300, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'}))


