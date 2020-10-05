from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

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
		patientDataSerializer = CreatePatientSerializer(data=patientData)

		if patientDataSerializer.is_valid():
			newPatient = patientDataSerializer.create(patientDataSerializer.validated_data)
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
