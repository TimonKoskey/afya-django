from rest_framework.serializers import (
	ModelSerializer,
	SerializerMethodField,
)

from patients.models import patient
# from visits.serializers.serializers import RetrieveVisitSerializer
# from visits.models import visitModel

class CreatePatientSerializer(ModelSerializer):

	class Meta:
		model = patient
		fields = [
			'id',
			'patientRegistrationNumber',
			'firstName',
			'lastname',
			'dateOfBirth',
			'age',
			'gender',
			'phoneNumber',
			'residence',
			'registrationDate',
			'lastUpdated'
		]

	def create(self, validated_data):
		newPatient = patient(
			patientRegistrationNumber = validated_data['patientRegistrationNumber'],
			firstName = validated_data['firstName'],
			lastname = validated_data['lastName'],
			dateOfBirth = validated_data['dateOfBirth'],
			gender = validated_data['gender'],
			phoneNumber = validated_data['phoneNumber'],
			residence = validated_data['residence']
			)

		return newPatient

class PatientsListSerializer(ModelSerializer):

	class Meta:
		model = patient
		fields = [
			'id',
			'patientRegistrationNumber',
			'firstName',
			'lastname',
			'dateOfBirth',
			'age',
			'gender',
			'phoneNumber',
			'residence'
		]

class RetrievePatientSerializer(ModelSerializer):

	class Meta:
		model = patient
		fields = [
			'id',
			'patientRegistrationNumber',
			'firstName',
			'lastname',
			'dateOfBirth',
			'age',
			'gender',
			'phoneNumber',
			'residence',
			'registrationDate',
			'lastUpdated'
		]

	def update(self, instance, validated_data):
		instance.patientRegistrationNumber = validated_data.get('patientRegistrationNumber', instance.patientRegistrationNumber)
		instance.firstName = validated_data.get('firstName', instance.firstName)
		instance.lastname = validated_data.get('lastName', instance.lastName)
		instance.dateOfBirth = validated_data.get('dateOfBirth', instance.dateOfBirth)
		instance.gender = validated_data.get('gender', instance.gender)
		instance.phoneNumber = validated_data.get('phoneNumber', instance.phoneNumber)
		instance.residence = validated_data.get('residence', instance.residence)

		return instance

	# def get_visits(self,obj):
	# 	visitsQueryset = visitModel.objects.filter(patient=obj)
	# 	visits = RetrieveVisitSerializer(visitsQueryset,many=True).data
	# 	return visits
