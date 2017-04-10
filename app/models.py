"""
Definition of models.
"""

from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django import forms

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CHOICES = [('company_user', 'Company User'),
               ('investor_user', 'Investor User')]

    user_type = models.CharField(max_length=13, choices=CHOICES, default='company_user', null=True)

    def __str__(self):
        return  "Username:" + self.user.username + " User_Type:" + self.user_type

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender")
    receiver = models.ForeignKey(User, related_name="receiver")
    subject = models.CharField(max_length=200)
    content = models.TextField()
    send_date = models.DateTimeField(default=timezone.now)

    def store(self):
        self.send_date = timezone.now()
        self.save()

    def __str__(self):
        return self.subject

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Group(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    groupmembers = models.CharField(max_length=20)
        # forms.ModelChoiceField(queryset=User.objects.all())
    @classmethod
    def create(cls, name, description, groupmembers):
        group = cls(name=name, description=description, groupmembers=groupmembers)
        return group

