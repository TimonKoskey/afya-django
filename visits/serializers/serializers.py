from rest_framework.serializers import (
	ModelSerializer, SerializerMethodField
)

from patients.models import patient
from patients.serializers.serializers import PatientsListSerializer, RetrievePatientSerializer

from visits.models import ( visitModel, paymentModel, vitalsModel, complaintsModel, physicalExamsModel, comorbiditiesModel, investigationsModel, diagnosisModel,
    treatmentModel, remarksModel, merged)

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

		return newVitals

class ComplaintsSerializer(ModelSerializer):

	class Meta:
		model = complaintsModel
		fields = ['id', 'entry']

	def create(self, validated_data):
		newComplaints = complaintsModel(
			entry = validated_data.get('entry', '')
        )

		return newComplaints

class PhysicalExamSerializer(ModelSerializer):

	class Meta:
		model = physicalExamsModel
		fields = ['id', 'entry']

	def create(self, validated_data):
		newPhysicalExam = physicalExamsModel(
			entry = validated_data.get('entry', '')
        )

		return newPhysicalExam

class ComorbiditiesSerializer(ModelSerializer):

	class Meta:
		model = comorbiditiesModel
		fields = ['id', 'entry']

	def create(self, validated_data):
		newComorbidities = comorbiditiesModel(
			entry = validated_data.get('entry', '')
        )

		return newComorbidities

class InvestigationsSerializer(ModelSerializer):

	class Meta:
		model = investigationsModel
		fields = [
			'id',
			'test',
			'results',
			'date',
			'lastUpdated'
		]

	def create(self, validated_data):
		newInvestigationObj = investigationsModel(
			test = validated_data.get('test', '')
        )

		return newInvestigationObj

class DiagnosisSerializer(ModelSerializer):

	class Meta:
		model = diagnosisModel
		fields = ['id', 'entry']

	def create(self, validated_data):
		newDiagnosis = diagnosisModel(
			entry = validated_data.get('entry', '')
        )

		return newDiagnosis

class TreatmentSerializer(ModelSerializer):

	class Meta:
		model = treatmentModel
		fields = ['id', 'entry']

	def create(self, validated_data):
		newTreatment = treatmentModel(
			entry = validated_data.get('entry', '')
        )

		return newTreatment

class RemarksSerializer(ModelSerializer):

	class Meta:
		model = remarksModel
		fields = ['id', 'entry']

	def create(self, validated_data):
		newRemarks = remarksModel(
			entry = validated_data.get('entry', '')
        )

		return newRemarks

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
			'status',
            'vitals',
            'complaints',
            'physicalExams',
            'comorbidities',
            'investigations',
            'diagnosis',
            'treatment',
            'remarks',
			'date',
			'lastUpdated',
            'payments'
		]

	def get_patient(self,obj):
		patient = RetrievePatientSerializer(obj.patient).data
		return patient

	def get_vitals(self,obj):
		try:
			vitalsObj = vitalsModel.objects.filter(visit=obj)
			vitals = VitalsEntrySerializer(vitalsObj,many=True).data
			return vitals
		except Exception as e:
			return None

	def get_complaints(self,obj):
		try:
			complaintsObj = complaintsModel.objects.filter(visit=obj)
			complaints = ComplaintsSerializer(complaintsObj,many=True).data
			return complaints
		except Exception as e:
			return None

	def get_physicalExams(self,obj):
		try:
			physicalExamsObj = physicalExamsModel.objects.filter(visit=obj)
			physicalExams = PhysicalExamSerializer(physicalExamsObj,many=True).data
			return physicalExams
		except Exception as e:
			return None

	def get_comorbidities(self,obj):

		try:
			comorbiditiesObj = comorbiditiesModel.objects.filter(visit=obj)
			comorbidities = ComorbiditiesSerializer(comorbiditiesObj,many=True).data
			return comorbidities
		except Exception as e:
			return None

	def get_investigations(self,obj):

		try:
			investigationsObjs = investigationsModel.objects.filter(visit=obj)
			investigations = InvestigationsSerializer(investigationsObjs,many=True).data
			return investigations
		except Exception as e:
			return None

	def get_diagnosis(self,obj):

		try:
			diagnosisObj = diagnosisModel.objects.filter(visit=obj)
			diagnosis = DiagnosisSerializer(diagnosisObj,many=True).data
			return diagnosis
		except Exception as e:
			return None

	def get_treatment(self,obj):

		try:
			treatmentObj = treatmentModel.objects.filter(visit=obj)
			treatment = TreatmentSerializer(treatmentObj,many=True).data
			return treatment
		except Exception as e:
			return None

	def get_remarks(self,obj):

		try:
			remarksObj = remarksModel.objects.get(visit=obj)
			remarks = RemarksSerializer(remarksObj,many=True).data
			return remarks
		except Exception as e:
			return None

	def get_payments(self,obj):
		paymentObjs = paymentModel.objects.filter(visit=obj)
		payments = PaymentSerializer(paymentObjs,many=True).data
		return payments

class MergedSessionsSerializer(ModelSerializer):
	previous = SerializerMethodField()
	next = SerializerMethodField()

	class Meta:
		model = merged
		fields = [
			'id',
			'previous',
			'next'
		]

	def get_previous(self,obj):
		previous = RetrieveVisitSerializer(obj.previous).data
		return previous;

	def get_next(self,obj):
		next = RetrieveVisitSerializer(obj.next).data
		return next;
