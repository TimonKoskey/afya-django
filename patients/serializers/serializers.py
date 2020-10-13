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

	def update(self, instance, validated_data):
		instance.patientRegistrationNumber = validated_data.get('patientRegistrationNumber', instance.patientRegistrationNumber)
		instance.firstName = validated_data.get('firstName', instance.firstName)
		instance.middleName = validated_data.get('middleName', instance.middleName)
		instance.surname = validated_data.get('surname', instance.surname)
		instance.dateOfBirth = validated_data.get('dateOfBirth', instance.dateOfBirth)
		instance.gender = validated_data.get('gender', instance.gender)
		instance.mainPhoneNumber = validated_data.get('mainPhoneNumber', instance.mainPhoneNumber)
		instance.alternativePhoneNumber = validated_data.get('alternativePhoneNumber', instance.alternativePhoneNumber)
		instance.email = validated_data.get('email', instance.email)
		instance.county = validated_data.get('county', instance.county)
		instance.subCounty = validated_data.get('subCounty', instance.subCounty)
		instance.estateOrArea = validated_data.get('estateOrArea', instance.estateOrArea)

		return instance
