from django.db import models
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone, timedelta

class Patient(models.Model):
	patientRegistrationNumber = models.CharField(max_length=50,blank=True, null=True)
	firstName = models.CharField(max_length=50, blank=True, null=True)
	lastName = models.CharField(max_length=50, blank=True, null=True)
	dateOfBirth = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
	age = models.CharField(max_length=50, blank=True, null=True)
	gender = models.CharField(max_length=50, blank=True, null=True)
	phoneNumber = models.CharField(max_length=50, blank=True, null=True)
	residence = models.CharField(max_length=50, blank=True, null=True)
	registrationDate = models.DateTimeField(auto_now=False, auto_now_add=True)
	lastUpdated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return "%s %s" %(self.firstName, self.lastName)

	class Meta:
		verbose_name_plural = 'Patients'


def every_day():
	currentDate = (datetime.now().replace(tzinfo=timezone(timedelta(hours=3)))).date()
	patientsQueryset = Patient.objects.all();

	if patientsQueryset:
		for patientObj in patientsQueryset:
			dateOfBirth = patientObj.dateOfBirth

			if dateOfBirth.month == currentDate.month and dateOfBirth.day == currentDate.day:
				years = currentDate.year - dateOfBirth.year
				patientObj.age = str(years) + ' years'
				patientObj.save()

sched = BackgroundScheduler(daemon=True)
sched.add_job(every_day,'cron', hour=0, minute=5)
sched.start()

patient = Patient
