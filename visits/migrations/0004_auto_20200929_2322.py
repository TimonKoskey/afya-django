# Generated by Django 3.1.1 on 2020-09-29 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0003_auto_20200929_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='followUpDate',
            field=models.DateTimeField(null=True),
        ),
    ]
