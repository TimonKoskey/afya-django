# Generated by Django 3.1.1 on 2020-10-04 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0006_auto_20201001_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='balance',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]