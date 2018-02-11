from django.test import RequestFactory

from test_plus.test import TestCase
# Create your tests here.


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
