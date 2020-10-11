from rest_framework.serializers import (
	ModelSerializer,
	SerializerMethodField,
)

from patients.models import patient

class CreatePatientSerializer(ModelSerializer):

	class Meta:
		model = patient
		fields = [
			'id',
			'patientRegistrationNumber',
			'firstName',
			'middleName',
            'surname',
			'dateOfBirth',
			'age',
			'gender',
			'mainPhoneNumber',
            'alternativePhoneNumber',
			'email',
			'county',
			'subCounty',
			'estateOrArea',
			'registrationDate',
			'lastUpdated'
		]

	def create(self, validated_data):
		newPatient = patient(
			patientRegistrationNumber = validated_data['patientRegistrationNumber'],
			firstName = validated_data['firstName'],
			middleName = validated_data['middleName'],
            surname = validated_data['surname'],
			dateOfBirth = validated_data['dateOfBirth'],
			gender = validated_data['gender'],
			mainPhoneNumber = validated_data['mainPhoneNumber'],
            alternativePhoneNumber = validated_data['alternativePhoneNumber'],
			email = validated_data['email'],
			county = validated_data['county'],
			subCounty = validated_data['subCounty'],
			estateOrArea = validated_data['estateOrArea']
			)
			
		return newPatient

class PatientsListSerializer(ModelSerializer):

	class Meta:
		model = patient
		fields = [
			'id',
			'patientRegistrationNumber',
			'firstName',
			'middleName',
            'surname',
			'dateOfBirth',
			'age',
			'gender',
			'mainPhoneNumber',
            'registrationDate'
		]

class RetrievePatientSerializer(ModelSerializer):

	class Meta:
		model = patient
		fields = [
			'id',
			'patientRegistrationNumber',
			'firstName',
			'middleName',
            'surname',
			'dateOfBirth',
			'age',
			'gender',
			'mainPhoneNumber',
            'alternativePhoneNumber',
			'email',
			'county',
			'subCounty',
			'estateOrArea',
			'registrationDate',
			'lastUpdated'
		]
