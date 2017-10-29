from django.core import mail

from django.core.mail import send_mail, BadHeaderError

from django.http import HttpResponse, HttpResponseRedirect



class Email():


	def __init__(self, *args, **kwargs):
			self.from_email = kwargs['sender']
			self.message = kwargs['message']
			self.cc_myself = kwargs.pop('cc_myself', False)
			self.recipient_list = kwargs['recipients']
			self.subject = kwargs.pop('subject', '')



	def open(self):
		self.connection = mail.get_connection()


	def close(self):
		self.connection.close()


	def send_email(self):
		try:
			self.open()
			send_mail(self.subject, self.message, self.from_email, self.recipient_list)
		except BadHeaderError:
			raise BadHeaderError
		finally:
			self.close()