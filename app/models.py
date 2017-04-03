"""
Definition of models.
"""

from django.db import models
from django.utils import timezone

class Messages(models.Model):
    sender = models.ForeignKey('auth.User')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    send_date = models.DateTimeField(default=timezone.now)

    def store(self):
        self.send_date = timezone.now()
        self.save()

    def __str__(self):
        return self.subject
