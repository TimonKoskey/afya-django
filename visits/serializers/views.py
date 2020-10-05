from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime, timezone
from django.db.models import Q

from rest_framework.generics import (
	RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
)

from patients.models import patient

from visits.models import ( visitModel, paymentModel, vitalsModel, complaintsModel, physicalExamsModel, comorbiditiesModel, investigationsModel, diagnosisModel,
    treatmentModel, remarksModel, merged )
from .serializers import (
	PaymentSerializer, VitalsEntrySerializer, VisitsListSerializer, RetrieveVisitSerializer, ComplaintsSerializer
)

class CreateNewVisitAPIView(APIView):

    def get(self, request, *args, **kwargs):
        patient_pk = kwargs['patient_pk']
        patientObj = get_object_or_404(patient, pk=patient_pk)

        newVisit = visitModel(patient=patientObj,status='Active')
        newVisit.save()
        newVisitSerializer = RetrieveVisitSerializer(newVisit)

        return Response(newVisitSerializer.data, status=status.HTTP_201_CREATED)

class AllPatientVisitsListAPIView(ListAPIView):
	serializer_class = VisitsListSerializer

	def get_queryset(self, *args, **kwargs):
		patient_pk = self.kwargs['patient_pk']
		patientObj = get_object_or_404(patient, pk=patient_pk)
		queryset = visitModel.objects.filter(patient=patientObj)
		return queryset

class ActiveVisitsListAPIView(ListAPIView):
	serializer_class = VisitsListSerializer

	def get_queryset(self, *args, **kwargs):
		queryset = visitModel.objects.filter(status='Active')
		return queryset

class FollowUpVisitsAPIView(ListAPIView):
	serializer_class = VisitsListSerializer

	def get_queryset(self, *args, **kwargs):
		currentDate = datetime.now().replace(tzinfo=timezone.utc).astimezone(tz=None).date()
		queryset = visitModel.objects.filter(
			Q(followUpStatus='Open'),
			Q(followUpDate=currentDate)
		)
		return queryset

class getVisitsByDateAPIView(ListAPIView):
	serializer_class = VisitsListSerializer

	def get_queryset(self, *args, **kwargs):
		dateTimeString = self.request.GET.get('dateTimeString')
		date = datetime.strptime(dateTimeString, "%a, %d %b %Y %H:%M:%S %Z")
		dateStart = datetime.combine(date, datetime.min.time()).replace(tzinfo=timezone.utc).astimezone(tz=None)
		dateEnd = datetime.combine(date, datetime.max.time()).replace(tzinfo=timezone.utc).astimezone(tz=None)
		print(dateEnd);

		queryset = visitModel.objects.filter(
			Q(date__lte=dateEnd),
			Q(date__gte=dateStart)
		)

		return queryset

class RetrieveVisitAPIView(RetrieveAPIView):
	queryset = visitModel.objects.all()
	serializer_class = RetrieveVisitSerializer

class UpdateVisitAPIView(APIView):

	def put(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		visitData = request.data
		if visitData['followUpDate']:
			date = datetime.strptime(visitData['followUpDate'], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc).astimezone(tz=None).date()
			visitData['followUpDate'] = date

		visitSerializer = RetrieveVisitSerializer(data=visitData)
		if visitSerializer.is_valid():
			visitObj = get_object_or_404(visitModel, pk=visit_pk)
			visitObj.status = visitData.get('status', visitObj.status)
			visitObj.followUpStatus = visitData.get('followUpStatus', visitObj.followUpStatus)
			visitObj.followUpDate = visitData.get('followUpDate', visitObj.followUpDate)
			visitObj.save()
			return Response(RetrieveVisitSerializer(visitObj).data, status=status.HTTP_201_CREATED)

		return Response(visitSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteVisitAPIView(DestroyAPIView):
	queryset = visitModel.objects.all()
	serializer_class = RetrieveVisitSerializer

class CreateSessionPaymentInfoAPIView(APIView):

	def post(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		data = request.data

		serializer = PaymentSerializer(data=data)
		if serializer.is_valid():
			paymentObj = serializer.create(serializer.validated_data)
			visitObj = get_object_or_404(visitModel, pk=visit_pk)
			paymentObj.visit = visitObj
			paymentObj.save()
			return Response(PaymentSerializer(paymentObj).data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class getSessionPaymentsListAPIView(ListAPIView):
	serializer_class = PaymentSerializer

	def get_queryset(self, *args, **kwargs):
		visit_pk = self.kwargs['visit_pk']
		visitObj = get_object_or_404(visitModel, pk=visit_pk)
		queryset = paymentModel.objects.filter(visit=visitObj)
		return queryset

class RetrieveUpdateDeleteSessionPaymentAPIView(RetrieveUpdateDestroyAPIView):
	queryset = paymentModel.objects.all()
	serializer_class = PaymentSerializer

class CreateSessionComplaintsAPIView(CreateAPIView):
	queryset = complaintsModel.objects.all()
	serializer_class = ComplaintsSerializer

class RetrieveUpdateDeleteSessionComplaintsAPIView(RetrieveUpdateDestroyAPIView):
	queryset = complaintsModel.objects.all()
	serializer_class = ComplaintsSerializer
