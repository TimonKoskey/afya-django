# Generated by Django 3.1.1 on 2020-09-20 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('data1', models.CharField(blank=True, max_length=150, null=True)),
                ('data2', models.CharField(blank=True, max_length=150, null=True)),
                ('data3', models.CharField(blank=True, max_length=150, null=True)),
                ('data4', models.CharField(blank=True, max_length=150, null=True)),
                ('data5', models.CharField(blank=True, max_length=150, null=True)),
                ('data6', models.CharField(blank=True, max_length=150, null=True)),
                ('data7', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'verbose_name_plural': 'Notes',
            },
        ),
        migrations.CreateModel(
            name='Vitals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('systolic', models.IntegerField(blank=True, null=True)),
                ('diastolic', models.IntegerField(blank=True, null=True)),
                ('pulseRate', models.IntegerField(blank=True, null=True)),
                ('temperature', models.IntegerField(blank=True, null=True)),
                ('SPO2', models.IntegerField(blank=True, null=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Vitals',
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('followUpStatus', models.CharField(blank=True, max_length=50, null=True)),
                ('followUpDate', models.DateField(auto_now_add=True)),
                ('comorbidities', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comorbidities', to='visits.notes')),
                ('complaints', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='complaints', to='visits.notes')),
                ('diagnosis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='diagnosis', to='visits.notes')),
                ('investigations', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='investigations', to='visits.notes')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patients.patient')),
                ('physicalExams', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='physicalExams', to='visits.notes')),
                ('remarks', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='remarks', to='visits.notes')),
                ('treatment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='treatment', to='visits.notes')),
                ('vitals', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='visits.vitals')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concept', models.CharField(blank=True, max_length=50, null=True)),
                ('method', models.CharField(blank=True, max_length=50, null=True)),
                ('amount', models.CharField(blank=True, max_length=50, null=True)),
                ('companyName', models.CharField(blank=True, max_length=50, null=True)),
                ('mpesaCode', models.CharField(blank=True, max_length=50, null=True)),
                ('visit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='visits.visit')),
            ],
        ),
        migrations.CreateModel(
            name='MergedVisits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('next', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next', to='visits.visit')),
                ('previous', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous', to='visits.visit')),
            ],
            options={
                'verbose_name_plural': 'Merged Visits',
            },
        ),
    ]