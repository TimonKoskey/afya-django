from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime, timezone, timedelta

from rest_framework.generics import (
	RetrieveUpdateDestroyAPIView,
	ListAPIView
)

from patients.models import patient

from .serializers import (
	CreatePatientSerializer,
	PatientsListSerializer,
	RetrievePatientSerializer
)

class CreatePatientAPIView(APIView):

	def post(self, request, *args, **kwargs):
		patientData = request.data
		dateOfBirth = ((datetime.strptime(patientData['dob'], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone(timedelta(hours=3))))+timedelta(days=1)).date()
		currentDate = ((datetime.now().replace(tzinfo=timezone(timedelta(hours=3))))+timedelta(days=1)).date()
		patientData['dateOfBirth'] = dateOfBirth
		patientDataSerializer = CreatePatientSerializer(data=patientData)

		if patientDataSerializer.is_valid():
			newPatient = patientDataSerializer.create(patientDataSerializer.validated_data)
			years = currentDate.year - dateOfBirth.year
			age = str(years) + ' years'
			if currentDate.month < dateOfBirth.month or (currentDate.month == dateOfBirth.month and currentDate.day < dateOfBirth.day):
				years -= 1
				age = str(years) + ' years'
			if years == 0:
				years = currentDate.month - dateOfBirth.month
				age = str(years) + ' months'

			newPatient.age = age
			newPatient.save()
			newPatientSerializer = CreatePatientSerializer(newPatient)

			return Response(newPatientSerializer.data, status=status.HTTP_201_CREATED)

		return Response(patientDataSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientsListAPIView(ListAPIView):
	serializer_class = PatientsListSerializer

	def get_queryset(self, *args, **kwargs):
		queryset = patient.objects.all()
		return queryset

class PatientRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
	queryset = patient.objects.all()
	serializer_class = RetrievePatientSerializer

class CheckIfPatientRecordsExistAPIView(APIView):

	def post(self, request, *args, **kwargs):
		data = request.data
		patientsQueryset = patient.objects.filter(
			Q(firstName=data['firstName']) & Q(surname=data['surname']) & Q(mainPhoneNumber=data['mainPhoneNumber'])
		)
		serializer = PatientsListSerializer(patientsQueryset,many=True).data
		return Response(serializer, status=status.HTTP_200_OK)
