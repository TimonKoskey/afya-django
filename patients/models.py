from django.db import models
from celery.schedules import crontab
from celery.task import periodic_task
from datetime import datetime, timezone, timedelta

class Patient(models.Model):
	patientRegistrationNumber = models.IntegerField(blank=True, null=True)
	firstName = models.CharField(max_length=50, blank=True, null=True)
	middleName = models.CharField(max_length=50, blank=True, null=True)
	surname = models.CharField(max_length=50, blank=True, null=True)
	dateOfBirth = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
	age = models.CharField(max_length=50, blank=True, null=True)
	gender = models.CharField(max_length=50, blank=True, null=True)
	mainPhoneNumber = models.CharField(max_length=50, blank=True, null=True)
	alternativePhoneNumber = models.CharField(max_length=50, blank=True, null=True)
	email = models.EmailField(max_length=50, blank=True, null=True)
	county = models.CharField(max_length=50, blank=True, null=True)
	subCounty = models.CharField(max_length=50, blank=True, null=True)
	estateOrArea = models.CharField(max_length=50, blank=True, null=True)
	registrationDate = models.DateTimeField(auto_now=False, auto_now_add=True)
	lastUpdated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return "%s %s %s" %(self.firstName, self.middleName, self.surname)

	class Meta:
		verbose_name_plural = 'Patients'

@periodic_task(run_every=crontab(hour=0, minute=0))
def every_day():
	currentDate = ((datetime.now().replace(tzinfo=timezone(timedelta(hours=3))))+timedelta(days=1)).date()
	patientsQueryset = Patient.objects.all();

	if patientsQueryset:
		for patientObj in patientsQueryset:
			dateOfBirth = patientObj.dateOfBirth

			if dateOfBirth.month == currentDate.month and dateOfBirth.day == currentDate.day:
				years = currentDate.year - dateOfBirth.year
				patientObj.age = str(years) + ' years'
				patientObj.save()

patient = Patient