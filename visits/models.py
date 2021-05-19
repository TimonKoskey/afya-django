from django.db import models
from patients.models import patient

class Visit(models.Model):
    patient = models.ForeignKey(patient, null=True, blank=True, on_delete=models.CASCADE)
    date  = models.DateTimeField(auto_now=False, auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "%s" %(self.patient)

class Payment(models.Model):
    visit = models.ForeignKey(Visit, null=True, blank=True, on_delete=models.CASCADE)
    concept = models.CharField(max_length=50, blank=True, null=True)
    procedureName = models.CharField(max_length=50, blank=True, null=True)
    method = models.CharField(max_length=50, blank=True, null=True)
    amount = models.CharField(max_length=50, blank=True, null=True)
    balance = models.CharField(max_length=50, blank=True, null=True)
    companyName = models.CharField(max_length=50, blank=True, null=True)
    mpesaCode = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return "%s  -  %s  -  %s" %(self.visit, self.concept, self.amount)

class Vitals(models.Model):
    visit = models.ForeignKey(Visit, null=True, blank=True, on_delete=models.CASCADE)
    systolic = models.IntegerField(blank=True, null=True)
    diastolic = models.IntegerField(blank=True, null=True)
    pulseRate = models.IntegerField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    SPO2 = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Vitals'

    def __str__(self):
        return "%s" %(self.visit)

class Complaints(models.Model):
    visit = models.ForeignKey(Visit, null=True, blank=True, on_delete=models.CASCADE)
    entry = models.CharField(max_length=150, blank=True, null=True)
    # entry2 = models.CharField(max_length=150, blank=True, null=True)
    # entry3 = models.CharField(max_length=150, blank=True, null=True)
    # entry4 = models.CharField(max_length=150, blank=True, null=True)
    # entry5 = models.CharField(max_length=150, blank=True, null=True)
    # entry6 = models.CharField(max_length=150, blank=True, null=True)
    # entry7 = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Complaints'

    def __str__(self):
        return "%s" %(self.visit)

class PhysicalExams(models.Model):
    visit = models.ForeignKey(Visit, null=True, blank=True, on_delete=models.CASCADE)
    entry = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Physical Examinations'

    def __str__(self):
        return "%s" %(self.visit)

class Comorbidities(models.Model):
    visit = models.ForeignKey(Visit, null=True, blank=True, on_delete=models.CASCADE)
    entry = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Comorbidities'

    def __str__(self):
        return "%s" %(self.visit)

class Investigations(models.Model):
    visit = models.ForeignKey(Visit, null=True, blank=True, on_delete=models.CASCADE)
    test = models.CharField(max_length=150, blank=True, null=True)
    results = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = 'Investigations'

    def __str__(self):
        return "%s" %(self.visit)

class Diagnosis(models.Model):
    visit = models.ForeignKey(Visit, null=True, blank=True, on_delete=models.CASCADE)
    entry = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Diagnosis'

    def __str__(self):
        return "%s" %(self.visit)

class Treatment(models.Model):
    visit = models.ForeignKey(Visit, null=True, blank=True, on_delete=models.CASCADE)
    entry = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Treatment'

    def __str__(self):
        return "%s" %(self.visit)

class Remarks(models.Model):
    visit = models.ForeignKey(Visit, null=True, blank=True, on_delete=models.CASCADE)
    entry = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Remarks'

    def __str__(self):
        return "%s" %(self.visit)

class MergedVisits(models.Model):
    previous = models.ForeignKey(Visit, null=True, blank=True, on_delete=models.CASCADE, related_name='previous')
    next = models.ForeignKey(Visit, null=True, blank=True, on_delete=models.CASCADE, related_name='next')

    class Meta:
        verbose_name_plural = 'Merged Visits'

class Appointment(models.Model):
    patient = models.ForeignKey(patient, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    appointmentDate = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    status = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return "%s" %(self.patient)



visitModel = Visit
paymentModel = Payment
vitalsModel = Vitals
complaintsModel = Complaints
physicalExamsModel = PhysicalExams
comorbiditiesModel = Comorbidities
investigationsModel = Investigations
diagnosisModel = Diagnosis
treatmentModel = Treatment
remarksModel = Remarks
merged = MergedVisits
appointmentModel = Appointment
# investigationRequestModel = InvestigationRequest
