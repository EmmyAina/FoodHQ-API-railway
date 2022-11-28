from django.db import models

from django.core.files import File
from urllib.request import urlretrieve
import uuid
from datetime import datetime, timezone
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractBaseUser, Permission, PermissionsMixin
from datetime import datetime, timedelta, timezone
from .manager import UserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'),
                              null=True,
                              blank=False,
                              unique=True)
    username = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=300, null=True)
    phone_number = models.CharField(max_length=11)
    is_staff = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("-date_joined", )

    objects = UserManager()

    def __str__(self):
        return f"{self.id} {self.email}"
    
    def update_username(self, new_username):
        self.username = new_username
        self.save()


# Create your models here.
TOKEN_TYPE = (
    ('ACCOUNT_VERIFICATION', 'ACCOUNT_VERIFICATION'),
    ('PASSWORD_RESET', 'PASSWORD_RESET'),
    ('AUTH_TOKEN', 'AUTH_TOKEN'),
)


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=225, null=True)
    token_type = models.CharField(max_length=100,
                                  choices=TOKEN_TYPE,
                                  default='ACCOUNT_VERIFICATION')
    access = models.CharField(max_length=350, null=True, blank=True)
    refresh = models.CharField(max_length=350, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.token} {str(self.user)}'

    def is_valid(self):
        lifespan_in_seconds = float(settings.TOKEN_LIFESPAN * 60 * 60)
        now = datetime.now(timezone.utc)
        time_diff = now - self.created_at
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds:
            return False
        return True

    def verify_user(self):
        self.user.verified = True
        self.user.save()

    def generate(self):
        if not self.token:
            self.token = get_random_string(120)
            self.save()

    # def reset_user_password(self, password):
    #     self.user.set_password(password)
    #     self.user.verified = True
    #     self.user.save()


class OTPToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=6, null=True)
    token_type = models.CharField(max_length=100,
                                  choices=TOKEN_TYPE,
                                  default='ACCOUNT_VERIFICATION')
    access = models.CharField(max_length=350, null=True, blank=True)
    refresh = models.CharField(max_length=350, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.token} {str(self.user)}'

    def is_valid(self):
        lifespan_in_seconds = float(settings.TOKEN_LIFESPAN * 60 * 60)
        now = datetime.now(timezone.utc)
        time_diff = now - self.created_at
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds:
            return False
        return True

    def verify_user(self):
        self.user.verified = True
        self.user.save()

    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    def generate(self):
        if not self.token:
            self.token = self.random_with_N_digits(4)
            self.save()

class PasswordResetToken(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=6, null=True)
    token_type = models.CharField(max_length=100,
                                  choices=TOKEN_TYPE,
                                  default='PASSWORD_RESET')
    has_been_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def is_valid(self):
        lifespan_in_seconds = float(settings.TOKEN_LIFESPAN * 60 * 60)
        now = datetime.now(timezone.utc)
        time_diff = now - self.created_at
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds:
            return False
        return True

    def verify_user(self):
        self.has_been_confirmed = True
        self.save()
    
    def reset_password(self, password):
        self.user.set_password(password)
        self.user.save()

    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    def generate(self):
        if not self.token:
            self.token = self.random_with_N_digits(4)
            self.save()
