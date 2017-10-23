from django import forms

from django.contrib.auth.hashers import make_password

from django.core import validators







class LogInForm(forms.Form):
	email = forms.EmailField(label='email', widget=forms.TextInput(attrs={'placeholder': 'Enter your Email'}))
	password = forms.CharField(label='pwd', max_length = 300, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'}))







class MultiEmailField(forms.Field):
	def to_python(self, value):
		"Normalize data to a list of strings."

		# Return an empty list if no input was given.
		if not value:
			return []
		return value.split(',')

	def validate(self, value):
		"Check if value consists only of valid emails."

		# Use the parent's handling of required fields, etc.
		super(MultiEmailField, self).validate(value)

		for email in value:
			validators.validate_email(email)


class EmailForm(forms.Form):
	subject = forms.CharField(max_length=100)
	message = forms.CharField(widget=forms.Textarea)
	sender = forms.EmailField()
	recipients = MultiEmailField(widget=forms.Textarea)
	cc_myself = forms.BooleanField(required=False)


	def clean(self):
		cleaned_data = super(ContactForm, self).clean()
		cc_myself = cleaned_data.get("cc_myself")
		subject = cleaned_data.get("subject")

		if cc_myself and subject:
			# Only do something if both fields are valid so far.
			if "help" not in subject:
				raise forms.ValidationError(
					"Did not send for 'help' in the subject despite "
					"CC'ing yourself."
				)




