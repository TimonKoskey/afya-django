from rest_framework.serializers import (
	ModelSerializer, SerializerMethodField
)

from patients.models import patient
from patients.serializers.serializers import (
    PatientsListSerializer, RetrievePatientSerializer
)

from visits.models import ( visitModel, paymentModel, vitalsModel, complaintsModel, physicalExamsModel, comorbiditiesModel, investigationsModel, diagnosisModel,
    treatmentModel, remarksModel, merged )


class PaymentSerializer(ModelSerializer):

	class Meta:
		model = paymentModel
		fields = [
			'id', 'concept', 'method', 'amount', 'balance', 'companyName', 'mpesaCode', 'description'
		]

	def create(self, validated_data):
		newPayment = paymentModel(
			concept = validated_data.get('concept', ''),
			method = validated_data.get('method', ''),
			amount = validated_data.get('amount', ''),
			balance = validated_data.get('balance', ''),
            companyName = validated_data.get('companyName', ''),
			mpesaCode = validated_data.get('mpesaCode', ''),
			description = validated_data.get('description', '')
		)
		return newPayment

class VitalsEntrySerializer(ModelSerializer):

	class Meta:
		model = vitalsModel
		fields = [
			'id',
			'systolic',
			'diastolic',
			'pulseRate',
            'temperature',
			'SPO2',
			'weight'
		]

	def create(self, validated_data):
		newVitals = vitalsModel(
			systolic = validated_data['systolic'],
			diastolic = validated_data['diastolic'],
			pulseRate = validated_data['pulseRate'],
            temperature = validated_data['temperature'],
			SPO2 = validated_data['SPO2'],
			weight = validated_data['weight']
		)

		newVitals.save()
		return newVitals

class ComplaintsSerializer(ModelSerializer):

	class Meta:
		model = complaintsModel
		fields = [
			'id', 'entry1', 'entry2', 'entry3', 'entry4', 'entry5', 'entry6', 'entry7'
		]

	# def create(self, validated_data):
	# 	newComplaints = complaintsModel(
	# 		entry1 = validated_data['entry1'],
	# 		entry2 = validated_data['entry2'],
    #         entry3 = validated_data['entry3'],
	# 		entry4 = validated_data['entry4'],
	# 		entry5 = validated_data['entry5'],
    #         entry6 = validated_data['entry6'],
    #         entry7 = validated_data['entry7']
    #     )
	#
	# 	newComplaints.save()
	# 	return newComplaints

class PhysicalExamSerializer(ModelSerializer):

	class Meta:
		model = physicalExamsModel
		fields = [
			'id', 'entry1', 'entry2', 'entry3', 'entry4', 'entry5', 'entry6', 'entry7'
		]

class ComorbiditiesSerializer(ModelSerializer):

	class Meta:
		model = comorbiditiesModel
		fields = [
			'id', 'entry1', 'entry2', 'entry3', 'entry4', 'entry5', 'entry6', 'entry7'
		]

class InvestigationsSerializer(ModelSerializer):

	class Meta:
		model = investigationsModel
		fields = [
			'id', 'entry1', 'entry2', 'entry3', 'entry4', 'entry5', 'entry6', 'entry7'
		]

class DiagnosisSerializer(ModelSerializer):

	class Meta:
		model = diagnosisModel
		fields = [
			'id', 'entry1', 'entry2', 'entry3', 'entry4', 'entry5', 'entry6', 'entry7'
		]

class TreatmentSerializer(ModelSerializer):

	class Meta:
		model = treatmentModel
		fields = [
			'id', 'entry1', 'entry2', 'entry3', 'entry4', 'entry5', 'entry6', 'entry7'
		]

class RemarksSerializer(ModelSerializer):

	class Meta:
		model = remarksModel
		fields = [
			'id', 'entry1', 'entry2', 'entry3', 'entry4', 'entry5', 'entry6', 'entry7'
		]

class VisitsListSerializer(ModelSerializer):
	patient = SerializerMethodField()

	class Meta:
		model = visitModel
		fields = [
			'id',
            'patient',
			'status',
			'date'
		]

	def get_patient(self,obj):
		patient = PatientsListSerializer(obj.patient).data
		return patient

class RetrieveVisitSerializer(ModelSerializer):
	patient = SerializerMethodField()
	vitals = SerializerMethodField()
	complaints = SerializerMethodField()
	physicalExams = SerializerMethodField()
	comorbidities = SerializerMethodField()
	investigations = SerializerMethodField()
	diagnosis = SerializerMethodField()
	treatment = SerializerMethodField()
	remarks = SerializerMethodField()
	payments = SerializerMethodField()

	class Meta:
		model = visitModel
		fields = [
			'id',
            'patient',
            'vitals',
            'complaints',
            'physicalExams',
            'comorbidities',
            'investigations',
            'diagnosis',
            'treatment',
            'remarks',
			'status',
			'date',
			'lastUpdated',
            'followUpStatus',
            'followUpDate',
            'payments'
		]

	def get_patient(self,obj):
		patient = RetrievePatientSerializer(obj.patient).data
		return patient

	def get_vitals(self,obj):
		try:
			vitalsObj = vitalsModel.objects.get(visit=obj)
			vitals = VitalsEntrySerializer(vitalsObj).data
			return vitals
		except Exception as e:
			return None

	def get_complaints(self,obj):
		try:
			complaintsObj = complaintsModel.objects.get(visit=obj)
			complaints = ComplaintsSerializer(complaintsObj).data
			return complaints
		except Exception as e:
			return None

	def get_physicalExams(self,obj):
		try:
			physicalExamsObj = physicalExamsModel.objects.get(visit=obj)
			physicalExams = PhysicalExamSerializer(physicalExamsObj).data
			return physicalExams
		except Exception as e:
			return None

	def get_comorbidities(self,obj):

		try:
			comorbiditiesObj = complaintsModel.objects.get(visit=obj)
			comorbidities = ComorbiditiesSerializer(comorbiditiesObj).data
			return comorbidities
		except Exception as e:
			return None

	def get_investigations(self,obj):

		try:
			investigationsObj = investigationsModel.objects.get(visit=obj)
			investigations = InvestigationsSerializer(investigationsObj).data
			return investigations
		except Exception as e:
			return None

	def get_diagnosis(self,obj):

		try:
			diagnosisObj = diagnosisModel.objects.get(visit=obj)
			diagnosis = DiagnosisSerializer(diagnosisObj).data
			return diagnosis
		except Exception as e:
			return None

	def get_treatment(self,obj):

		try:
			treatmentObj = treatmentModel.objects.get(visit=obj)
			treatment = TreatmentSerializer(treatmentObj).data
			return treatment
		except Exception as e:
			return None

	def get_remarks(self,obj):

		try:
			remarksObj = remarksModel.objects.get(visit=obj)
			remarks = RemarksSerializer(remarksObj).data
			return remarks
		except Exception as e:
			return None

	def get_payments(self,obj):
		paymentObjs = paymentModel.objects.filter(visit=obj)
		payments = PaymentSerializer(paymentObjs,many=True).data
		return payments

	# def update(self, instance, validated_data):
	# 	instance.status = validated_data.get('status', instance.status)
	# 	instance.followUpStatus = validated_data.get('followUpStatus', instance.followUpStatus)
	#
	# 	if ()
