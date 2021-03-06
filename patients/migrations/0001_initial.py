# Generated by Django 3.1.1 on 2021-05-17 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientRegistrationNumber', models.CharField(blank=True, max_length=50, null=True)),
                ('firstName', models.CharField(blank=True, max_length=50, null=True)),
                ('lastName', models.CharField(blank=True, max_length=50, null=True)),
                ('dateOfBirth', models.DateField(blank=True, null=True)),
                ('age', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(blank=True, max_length=50, null=True)),
                ('phoneNumber', models.CharField(blank=True, max_length=50, null=True)),
                ('residence', models.CharField(blank=True, max_length=50, null=True)),
                ('registrationDate', models.DateTimeField(auto_now_add=True)),
                ('lastUpdated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Patients',
            },
        ),
    ]
