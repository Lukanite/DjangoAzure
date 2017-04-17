# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_messages', '0002_auto_20160607_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_encrypted',
            field=models.BooleanField(verbose_name='Message is encrypted', default=False),
        ),
    ]
