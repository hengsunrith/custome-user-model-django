# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

class UserManager(BaseUserManager):

    def create_user(self, email, username=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("U must have a email address")
        if not password:
            raise ValueError("U must have a password")
        if not username:
            raise ValueError("U must have a full name")
        user_obj = self.model(
            email = self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, username=None, password=None):
        user = self.create_user(
            email,
            full_name=username,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, username=None, password=None):
        user = self.create_user(
            email,
            full_name=username,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True) # can login
    staff = models.BooleanField(default=False) # staff user non superuser
    admin = models.BooleanField(default=False) # superuser
    dob = models.DateField(null=True)
    phone = models.CharField(max_length=20, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' # username
    # username and password is required by default
    REQUIRED_FIELDS = ['username'] # ['full_name'] # python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_user_name(self):
        if self.username:
            return self.username
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)