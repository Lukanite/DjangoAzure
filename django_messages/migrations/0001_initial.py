# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('subject', models.CharField(verbose_name='Subject', max_length=140)),
                ('body', models.TextField(verbose_name='Body')),
                ('sent_at', models.DateTimeField(blank=True, verbose_name='sent at', null=True)),
                ('read_at', models.DateTimeField(blank=True, verbose_name='read at', null=True)),
                ('replied_at', models.DateTimeField(blank=True, verbose_name='replied at', null=True)),
                ('sender_deleted_at', models.DateTimeField(blank=True, verbose_name='Sender deleted at', null=True)),
                ('recipient_deleted_at', models.DateTimeField(blank=True, verbose_name='Recipient deleted at', null=True)),
                ('is_encrypted', models.BooleanField(verbose_name='Message is encrypted', default=False)),
                ('parent_msg', models.ForeignKey(blank=True, verbose_name='Parent message', null=True, to='django_messages.Message', related_name='next_messages')),
                ('recipient', models.ForeignKey(blank=True, verbose_name='Recipient', null=True, to=settings.AUTH_USER_MODEL, related_name='received_messages')),
                ('sender', models.ForeignKey(related_name='sent_messages', verbose_name='Sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sent_at'],
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
    ]
