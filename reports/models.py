from django.db import models
from django.contrib.auth.models import Group, User

# Create your models here.
class Sector(models.Model):
    """Name lookup for sectors"""
    def __str__(self):
        return self.name
    name = models.CharField(max_length=255)

class Industry(models.Model):
    """Name lookup for industries"""
    def __str__(self):
        return self.name
    name = models.CharField(max_length=255)

class Attachment(models.Model):
    """Information about attachments"""
    def __str__(self):
        return self.name
    name = models.CharField(max_length=255)

class Report(models.Model):
    """Model for a report from any company"""
    def __str__(self):
        return self.name
    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    company_ceo = models.CharField(max_length=255)
    company_phone = models.CharField(max_length=30)
    company_email = models.EmailField(max_length=255)
    company_location = models.CharField(max_length=255)
    company_country = models.CharField(max_length=60)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, default=None, blank=True, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, default=None, blank=True, null=True)
    projects = models.TextField(null=True, blank=True)
    isprivate = models.BooleanField(default=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
    release_date = models.DateField(auto_now_add=True)

class ReportAttachment(models.Model):
    """Attachment for a report"""
    def __str__(self):
        return self.attachment.name
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='reports/', blank=True)
    isencrypted = models.BooleanField(default=False)
    attachmenthash = models.CharField(max_length=60, blank=True, null=True)