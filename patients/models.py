from django.db import models

class Patient(models.Model):
	patientRegistrationNumber = models.IntegerField(blank=True, null=True)
	firstName = models.CharField(max_length=50, blank=True, null=True)
	middleName = models.CharField(max_length=50, blank=True, null=True)
	surname = models.CharField(max_length=50, blank=True, null=True)
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



patient = Patient
