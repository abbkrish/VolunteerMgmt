from django import forms

from django.core import validators

class MultiEmailField(forms.Field):
	def to_python(self, value):
		"Normalize data to a list of strings."

		# Return an empty list if no input was given.
		if not value:
			return []

		#return email list with white space stripped off
		email_list = [i.strip() for i in value.split(',')]
		
		return email_list

	def validate(self, value):
		"Check if value consists only of valid emails."

		# Use the parent's handling of required fields, etc.
		super(MultiEmailField, self).validate(value)

		for email in value:
			validators.validate_email(email)

