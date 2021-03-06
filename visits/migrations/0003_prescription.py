# Generated by Django 3.1.1 on 2021-05-21 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0002_appointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.CharField(blank=True, max_length=150, null=True)),
                ('visit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='visits.visit')),
            ],
            options={
                'verbose_name_plural': 'Prescription',
            },
        ),
    ]
