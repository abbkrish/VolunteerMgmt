from django import forms

from django.contrib.auth.hashers import make_password

from django.core import validators

from .fields import MultiEmailField

from volunteermgmtdjango.users.models import User

from django.contrib.auth import authenticate, login, logout




class LogInForm(forms.Form):
    email = forms.EmailField(label='email', widget=forms.TextInput(attrs={'placeholder': 'Enter your Email'}))
    password = forms.CharField(label='pwd', max_length = 300, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'}))


    def find_user(self):
        try:
            volunteer = User.objects.get(email=self.cleaned_data['email'])
            if not volunteer.is_staff:
                raise forms.ValidationError("Sorry, only staff is allowed to access this page")
        except:
            raise forms.ValidationError("Sorry, that email or password entered is invalid")
            volunteer = None
        return volunteer 


    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        volunteer = self.find_user()
        if volunteer is None:
            return self.cleaned_data
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user



class EmailForm(forms.Form):
    subject = forms.CharField(max_length=100, required = False)
    message = forms.CharField(widget=forms.Textarea, required=True)
    sender = forms.EmailField(required = True)
    recipients = MultiEmailField(widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False)


    def clean(self):
        cleaned_data = super(EmailForm, self).clean()
        cc_myself = cleaned_data.get("cc_myself")
        subject = cleaned_data.get("subject")
        recipients = cleaned_data.get('recipients')
        sender = cleaned_data.get('sender')
        message = cleaned_data.get('message')
        




