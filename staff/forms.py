from django import forms

from django.contrib.auth.hashers import make_password

from django.core import validators

from .fields import MultiEmailField




class LogInForm(forms.Form):
	email = forms.EmailField(label='email', widget=forms.TextInput(attrs={'placeholder': 'Enter your Email'}))
	password = forms.CharField(label='pwd', max_length = 300, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'}))



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
		




