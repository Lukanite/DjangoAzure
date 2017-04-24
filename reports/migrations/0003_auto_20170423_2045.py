# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_report_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportattachment',
            name='isencrypted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='report',
            name='group',
            field=models.ForeignKey(blank=True, null=True, default=None, to='auth.Group'),
        ),
    ]
