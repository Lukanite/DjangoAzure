"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CHOICES = [('company_user', 'Company User'),
               ('investor_user', 'Investor User')]

    user_type = models.CharField(max_length=13, choices=CHOICES, default='company_user', null=True)

    def __str__(self):
        return  "Username:" + self.user.username + " User_Type:" + self.user_type

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()