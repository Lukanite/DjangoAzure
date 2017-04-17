# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_auto_20170410_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='attachment',
            field=models.FileField(upload_to='reports/'),
        ),
    ]
