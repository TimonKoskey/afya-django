# Generated by Django 3.1.1 on 2021-03-19 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visit',
            name='followUpDate',
        ),
        migrations.RemoveField(
            model_name='visit',
            name='followUpStatus',
        ),
    ]
