from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from custom_user.models import AbstractEmailUser
from phonenumber_field.modelfields import PhoneNumberField



class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    """ Deleting the user - just set the is_active to False"""

    username = None
    first_name = models.CharField(max_length=200, default = 'NULL')
    last_name = models.CharField(max_length=200, default = 'NULL')
    email = models.EmailField(unique=True, default = 'test@test.com')
    street_address_1 = models.CharField(max_length=200, default = 'NULL')
    street_address_2 = models.CharField(max_length=200, default = 'NULL', blank=True)
    city = models.CharField(max_length=200, default = 'South Orange')
    state = models.CharField(max_length=200, default = 'NJ')
    zipcode = models.CharField(max_length=200, default = 'NULL')
    need_community_svc_hrs = models.BooleanField(default = False)
    phone_number = PhoneNumberField(blank=True)
    volunteer_group = models.CharField(max_length=200, default = 'NULL')
    emergency_name =  models.CharField(max_length=200, default = 'NULL')
    emergency_phone = PhoneNumberField(blank=True) 
    waiver_filed = models.BooleanField(default = False)
    other = models.CharField(max_length=200, default='NULL')
    password = models.CharField(max_length=200, default = 'NULL')
    accept_terms = models.BooleanField(default = True)
    parents_signature = models.CharField(default='NULL', max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


'''
@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    #name = models.CharField(_('Name of User'), blank=True, max_length=255)
    first_name = models.CharField(max_length=200, default = 'NULL')
    last_name = models.CharField(max_length=200, default = 'NULL')
    email = models.EmailField(primary_key=True, unique=True, default = 'test@test.com')
    street_address_1 = models.CharField(max_length=200, default = 'NULL')
    street_address_2 = models.CharField(max_length=200, default = 'NULL')
    city = models.CharField(max_length=200, default = 'South Orange')
    state = models.CharField(max_length=200, default = 'NJ')
    zipcode = models.CharField(max_length=200, default = 'NULL')
    waiver_filed = models.BooleanField(default = False)
    volunteer_group = models.CharField(max_length=200, default = 'NULL')
    password = models.CharField(max_length=200, default = 'NULL')
    created = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)



    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


'''