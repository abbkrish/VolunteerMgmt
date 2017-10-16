from django import forms

from django.contrib.auth.hashers import make_password

from django.core import validators


from .models import Volunteer

class SubmitForm(forms.Form):
	first_name = forms.CharField(label='first_name', max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Enter your First name'}))
	last_name = forms.CharField(label='last_name', max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Enter your Last name'}))
	email = forms.EmailField(label='email', widget=forms.TextInput(attrs={'placeholder': 'Enter your Email'}))
	street_addr_1 = forms.CharField(label='addr1', max_length = 500, widget=forms.TextInput(attrs={'placeholder': 'Street Address, PO Box, Company Name'}))
	street_addr_2 = forms.CharField(label='addr2', max_length = 500, widget=forms.TextInput(attrs={'placeholder': 'Apartment, Unit '}))
	city = forms.CharField(label='city', max_length = 500, widget=forms.TextInput(attrs={'placeholder': 'City'}))
	state = forms.CharField(label='state', max_length = 500, widget=forms.TextInput(attrs={'placeholder': 'State'}))
	zipcode = forms.CharField(label='zipcode', max_length = 100, widget=forms.TextInput(attrs={'placeholder': '5 digit zipcode'}))
	waiverfiled = forms.BooleanField(label='waiver', required=False)
	volunteergroup = forms.CharField(label='volunteergroup', max_length = 500, widget=forms.TextInput(attrs={'placeholder': 'Eg: First Year Medical Student'}))
	password = forms.CharField(label='pwd', max_length = 300, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'}))
	confirm_password = forms.CharField(label = "c_pwd", max_length = 300, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your Password'}))



	class Meta:
		model = Volunteer
		fields = ('email')


	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password")
		password2 = self.cleaned_data.get("confirm_password")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2
	

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


