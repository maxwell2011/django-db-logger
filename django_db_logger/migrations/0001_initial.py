# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    initial = True
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StatusLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asctime', models.DateTimeField(help_text='Timestamp of the log entry', verbose_name='Timestamp')),
                ('module', models.CharField(help_text='Name portion of the filename', max_length=100, verbose_name='Model')),
                ('lineno', models.PositiveIntegerField(default=0, help_text='Source line number where the logging call was issued (if available, default: 0)', verbose_name='Line Number')),
                ('pid', models.PositiveIntegerField(default=0, help_text='Process id (if available, default: 0)', verbose_name='Process ID')),
                ('tid', models.PositiveIntegerField(default=0, help_text='Thread id (if available, default: 0)', verbose_name='Thread ID')),
                ('logger', models.CharField(help_text='Name of the logger', max_length=100, verbose_name='Logger')),
                ('level', models.PositiveSmallIntegerField(choices=[(0, 'NotSet'), (20, 'Info'), (30, 'Warning'), (10, 'Debug'), (40, 'Error'), (50, 'Fatal')], db_index=True, default=40, help_text='Log level of the entry', verbose_name='Level')),
                ('msg', models.TextField(help_text='Raw message', max_length=4096, verbose_name='Message')),
                ('trace', models.TextField(blank=True, help_text='Raw traceback exception info (if available)', max_length=4096, null=True, verbose_name='Traceback')),
            ],
            options={
                'verbose_name': 'Logging',
                'verbose_name_plural': 'Logging',
                'ordering': ('-asctime',),
            },
        ),
    ]
