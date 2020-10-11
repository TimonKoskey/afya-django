from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime, timezone, timedelta
from django.db.models import Q

from rest_framework.generics import (
	ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
)

from patients.models import patient

from visits.models import ( visitModel, paymentModel, vitalsModel, complaintsModel, physicalExamsModel, comorbiditiesModel, investigationsModel, diagnosisModel,
    treatmentModel, remarksModel, merged )
from .serializers import (
	PaymentSerializer, VitalsEntrySerializer, VisitsListSerializer, RetrieveVisitSerializer, ComplaintsSerializer, PhysicalExamSerializer,
	ComorbiditiesSerializer, InvestigationsSerializer, DiagnosisSerializer, TreatmentSerializer, RemarksSerializer, MergedSessionsSerializer )

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
		currentDate = ((datetime.now().replace(tzinfo=timezone(timedelta(hours=3))))+timedelta(days=1)).date()
		queryset = visitModel.objects.filter(
			Q(followUpDate=currentDate)
		)
		return queryset

class getVisitsByDateAPIView(ListAPIView):
	serializer_class = VisitsListSerializer

	def get_queryset(self, *args, **kwargs):
		dateTimeString = self.request.GET.get('dateTimeString')
		date = datetime.strptime(dateTimeString, "%a, %d %b %Y %H:%M:%S %Z")
		dateStart = (datetime.combine(date, datetime.min.time()).replace(tzinfo=timezone(timedelta(hours=3))))+timedelta(days=1)
		dateEnd = (datetime.combine(date, datetime.max.time()).replace(tzinfo=timezone(timedelta(hours=3))))+timedelta(days=1)
		print(dateStart);
		print(dateEnd);

		queryset = visitModel.objects.filter(
			Q(date__lte=dateEnd) &
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
			date = ((datetime.strptime(visitData['followUpDate'], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone(timedelta(hours=3))))+timedelta(days=1)).date()
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

class CreateSessionComplaintsAPIView(APIView):

	def post(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		data = request.data
		serializer = ComplaintsSerializer(data=data)

		if serializer.is_valid():
			complaintsObj = serializer.create(serializer.validated_data)
			visitObj = get_object_or_404(visitModel, pk=visit_pk)
			complaintsObj.visit = visitObj
			complaintsObj.save()
			return Response(ComplaintsSerializer(complaintsObj).data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	queryset = complaintsModel.objects.all()

class GetSessionComplaintsAPIView(APIView):

	def get(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		visitObj = get_object_or_404(visitModel, pk=visit_pk)
		complaintsObj = get_object_or_404(complaintsModel, visit=visitObj)
		return Response(ComplaintsSerializer(complaintsObj).data, status=status.HTTP_201_CREATED)

class RetrieveUpdateDeleteSessionComplaintsAPIView(RetrieveUpdateDestroyAPIView):
	queryset = complaintsModel.objects.all()
	serializer_class = ComplaintsSerializer

class CreateSessionPhycExamsAPIView(APIView):

	def post(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		data = request.data
		serializer = PhysicalExamSerializer(data=data)

		if serializer.is_valid():
			notesObj = serializer.create(serializer.validated_data)
			visitObj = get_object_or_404(visitModel, pk=visit_pk)
			notesObj.visit = visitObj
			notesObj.save()
			return Response(PhysicalExamSerializer(notesObj).data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetSessionPhycExamsAPIView(APIView):

	def get(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		visitObj = get_object_or_404(visitModel, pk=visit_pk)
		notesObj = get_object_or_404(physicalExamsModel, visit=visitObj)
		return Response(PhysicalExamSerializer(notesObj).data, status=status.HTTP_201_CREATED)

class RetrieveUpdateDeleteSessionPhycExamsAPIView(RetrieveUpdateDestroyAPIView):
	queryset = physicalExamsModel.objects.all()
	serializer_class = PhysicalExamSerializer

class CreateSessionComorbiditiesAPIView(APIView):

	def post(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		data = request.data
		serializer = ComorbiditiesSerializer(data=data)

		if serializer.is_valid():
			notesObj = serializer.create(serializer.validated_data)
			visitObj = get_object_or_404(visitModel, pk=visit_pk)
			notesObj.visit = visitObj
			notesObj.save()
			return Response(ComorbiditiesSerializer(notesObj).data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetSessionComorbiditiesAPIView(APIView):

	def get(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		visitObj = get_object_or_404(visitModel, pk=visit_pk)
		notesObj = get_object_or_404(comorbiditiesModel, visit=visitObj)
		return Response(ComorbiditiesSerializer(notesObj).data, status=status.HTTP_201_CREATED)

class RetrieveUpdateDeleteSessionComorbiditiesAPIView(RetrieveUpdateDestroyAPIView):
	queryset = comorbiditiesModel.objects.all()
	serializer_class = ComorbiditiesSerializer

class CreateSessionInvestigationsAPIView(APIView):

	def post(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		data = request.data
		serializer = InvestigationsSerializer(data=data)

		if serializer.is_valid():
			notesObj = serializer.create(serializer.validated_data)
			visitObj = get_object_or_404(visitModel, pk=visit_pk)
			notesObj.visit = visitObj
			notesObj.save()
			return Response(InvestigationsSerializer(notesObj).data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetSessionInvestigationsAPIView(APIView):

	def get(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		visitObj = get_object_or_404(visitModel, pk=visit_pk)
		notesObj = get_object_or_404(investigationsModel, visit=visitObj)
		return Response(InvestigationsSerializer(notesObj).data, status=status.HTTP_201_CREATED)

class RetrieveUpdateDeleteSessionInvestigationsAPIView(RetrieveUpdateDestroyAPIView):
	queryset = investigationsModel.objects.all()
	serializer_class = InvestigationsSerializer

class CreateSessionDiagnosisAPIView(APIView):

	def post(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		data = request.data
		serializer = DiagnosisSerializer(data=data)

		if serializer.is_valid():
			notesObj = serializer.create(serializer.validated_data)
			visitObj = get_object_or_404(visitModel, pk=visit_pk)
			notesObj.visit = visitObj
			notesObj.save()
			return Response(DiagnosisSerializer(notesObj).data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetSessionDiagnosisAPIView(APIView):

	def get(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		visitObj = get_object_or_404(visitModel, pk=visit_pk)
		notesObj = get_object_or_404(diagnosisModel, visit=visitObj)
		return Response(DiagnosisSerializer(notesObj).data, status=status.HTTP_201_CREATED)

class RetrieveUpdateDeleteSessionDiagnosisAPIView(RetrieveUpdateDestroyAPIView):
	queryset = diagnosisModel.objects.all()
	serializer_class = DiagnosisSerializer

class CreateSessionTreatmentAPIView(APIView):

	def post(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		data = request.data
		serializer = TreatmentSerializer(data=data)

		if serializer.is_valid():
			notesObj = serializer.create(serializer.validated_data)
			visitObj = get_object_or_404(visitModel, pk=visit_pk)
			notesObj.visit = visitObj
			notesObj.save()
			return Response(TreatmentSerializer(notesObj).data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetSessionTreatmentAPIView(APIView):

	def get(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		visitObj = get_object_or_404(visitModel, pk=visit_pk)
		notesObj = get_object_or_404(treatmentModel, visit=visitObj)
		return Response(TreatmentSerializer(notesObj).data, status=status.HTTP_201_CREATED)

class RetrieveUpdateDeleteSessionTreatmentAPIView(RetrieveUpdateDestroyAPIView):
	queryset = treatmentModel.objects.all()
	serializer_class = TreatmentSerializer

class CreateSessionRemarksAPIView(APIView):

	def post(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		data = request.data
		serializer = RemarksSerializer(data=data)

		if serializer.is_valid():
			notesObj = serializer.create(serializer.validated_data)
			visitObj = get_object_or_404(visitModel, pk=visit_pk)
			notesObj.visit = visitObj
			notesObj.save()
			return Response(RemarksSerializer(notesObj).data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetSessionRemarksAPIView(APIView):

	def get(self, request, *args, **kwargs):
		visit_pk = kwargs['visit_pk']
		visitObj = get_object_or_404(visitModel, pk=visit_pk)
		notesObj = get_object_or_404(remarksModel, visit=visitObj)
		return Response(RemarksSerializer(notesObj).data, status=status.HTTP_201_CREATED)

class RetrieveUpdateDeleteSessionRemarksAPIView(RetrieveUpdateDestroyAPIView):
	queryset = remarksModel.objects.all()
	serializer_class = RemarksSerializer

class GetComplaintsSuggestionsAPIView(APIView):

	def get(self, request, *args, **kwargs):
		suggestions = ['Headache', 'Visual disturbance', 'Radiculopathy - Upper Limbs', 'Radiculopathy - Lower Limbs']
		queryString = request.GET.get('queryString')
		complaintsQuerySet = complaintsModel.objects.all()

		if complaintsQuerySet:
			for complaintObj in complaintsQuerySet:
				if queryString in complaintObj.entry1 and complaintObj.entry1 not in suggestions:
					suggestions.append(complaintObj.entry1)
				if queryString in complaintObj.entry2 and complaintObj.entry2 not in suggestions:
					suggestions.append(complaintObj.entry2)
				if queryString in complaintObj.entry3 and complaintObj.entry3 not in suggestions:
					suggestions.append(complaintObj.entry3)
				if queryString in complaintObj.entry4 and complaintObj.entry4 not in suggestions:
					suggestions.append(complaintObj.entry4)
				if queryString in complaintObj.entry5 and complaintObj.entry5 not in suggestions:
					suggestions.append(complaintObj.entry5)
				if queryString in complaintObj.entry6 and complaintObj.entry6 not in suggestions:
					suggestions.append(complaintObj.entry6)
				if queryString in complaintObj.entry7 and complaintObj.entry7 not in suggestions:
					suggestions.append(complaintObj.entry7)

		return Response(suggestions, status=status.HTTP_200_OK)

class GetPhysicalExamsSuggestionsAPIView(APIView):

	def get(self, request, *args, **kwargs):
		suggestions = []
		queryString = request.GET.get('queryString')
		querySet = physicalExamsModel.objects.all()

		if querySet:
			for obj in querySet:
				if queryString in obj.entry1 and obj.entry1 not in suggestions:
					suggestions.append(obj.entry1)
				if queryString in obj.entry2 and obj.entry2 not in suggestions:
					suggestions.append(obj.entry2)
				if queryString in obj.entry3 and obj.entry3 not in suggestions:
					suggestions.append(obj.entry3)
				if queryString in obj.entry4 and obj.entry4 not in suggestions:
					suggestions.append(obj.entry4)
				if queryString in obj.entry5 and obj.entry5 not in suggestions:
					suggestions.append(obj.entry5)
				if queryString in obj.entry6 and obj.entry6 not in suggestions:
					suggestions.append(obj.entry6)
				if queryString in obj.entry7 and obj.entry7 not in suggestions:
					suggestions.append(obj.entry7)

		return Response(suggestions, status=status.HTTP_200_OK)

class GetComorbiditiesSuggestionsAPIView(APIView):

	def get(self, request, *args, **kwargs):
		suggestions = []
		queryString = request.GET.get('queryString')
		querySet = comorbiditiesModel.objects.all()

		if querySet:
			for obj in querySet:
				if queryString in obj.entry1 and obj.entry1 not in suggestions:
					suggestions.append(obj.entry1)
				if queryString in obj.entry2 and obj.entry2 not in suggestions:
					suggestions.append(obj.entry2)
				if queryString in obj.entry3 and obj.entry3 not in suggestions:
					suggestions.append(obj.entry3)
				if queryString in obj.entry4 and obj.entry4 not in suggestions:
					suggestions.append(obj.entry4)
				if queryString in obj.entry5 and obj.entry5 not in suggestions:
					suggestions.append(obj.entry5)
				if queryString in obj.entry6 and obj.entry6 not in suggestions:
					suggestions.append(obj.entry6)
				if queryString in obj.entry7 and obj.entry7 not in suggestions:
					suggestions.append(obj.entry7)

		return Response(suggestions, status=status.HTTP_200_OK)

class GetInvestigationsSuggestionsAPIView(APIView):

	def get(self, request, *args, **kwargs):
		suggestions = []
		queryString = request.GET.get('queryString')
		querySet = investigationsModel.objects.all()

		if querySet:
			for obj in querySet:
				if queryString in obj.entry1 and obj.entry1 not in suggestions:
					suggestions.append(obj.entry1)
				if queryString in obj.entry2 and obj.entry2 not in suggestions:
					suggestions.append(obj.entry2)
				if queryString in obj.entry3 and obj.entry3 not in suggestions:
					suggestions.append(obj.entry3)
				if queryString in obj.entry4 and obj.entry4 not in suggestions:
					suggestions.append(obj.entry4)
				if queryString in obj.entry5 and obj.entry5 not in suggestions:
					suggestions.append(obj.entry5)
				if queryString in obj.entry6 and obj.entry6 not in suggestions:
					suggestions.append(obj.entry6)
				if queryString in obj.entry7 and obj.entry7 not in suggestions:
					suggestions.append(obj.entry7)

		return Response(suggestions, status=status.HTTP_200_OK)

class GetDiagnosisSuggestionsAPIView(APIView):

	def get(self, request, *args, **kwargs):
		suggestions = ['Brain tumor - Benign', 'Brain tumor - Malignant', 'Lumbar Spondylosis', 'Cervical Spondylosis']
		queryString = request.GET.get('queryString')
		querySet = investigationsModel.objects.all()

		if querySet:
			for obj in querySet:
				if queryString in obj.entry1 and obj.entry1 not in suggestions:
					suggestions.append(obj.entry1)
				if queryString in obj.entry2 and obj.entry2 not in suggestions:
					suggestions.append(obj.entry2)
				if queryString in obj.entry3 and obj.entry3 not in suggestions:
					suggestions.append(obj.entry3)
				if queryString in obj.entry4 and obj.entry4 not in suggestions:
					suggestions.append(obj.entry4)
				if queryString in obj.entry5 and obj.entry5 not in suggestions:
					suggestions.append(obj.entry5)
				if queryString in obj.entry6 and obj.entry6 not in suggestions:
					suggestions.append(obj.entry6)
				if queryString in obj.entry7 and obj.entry7 not in suggestions:
					suggestions.append(obj.entry7)

		return Response(suggestions, status=status.HTTP_200_OK)

class GetTreatmentSuggestionsAPIView(APIView):

	def get(self, request, *args, **kwargs):
		suggestions = []
		queryString = request.GET.get('queryString')
		querySet = treatmentModel.objects.all()

		if querySet:
			for obj in querySet:
				if queryString in obj.entry1 and obj.entry1 not in suggestions:
					suggestions.append(obj.entry1)
				if queryString in obj.entry2 and obj.entry2 not in suggestions:
					suggestions.append(obj.entry2)
				if queryString in obj.entry3 and obj.entry3 not in suggestions:
					suggestions.append(obj.entry3)
				if queryString in obj.entry4 and obj.entry4 not in suggestions:
					suggestions.append(obj.entry4)
				if queryString in obj.entry5 and obj.entry5 not in suggestions:
					suggestions.append(obj.entry5)
				if queryString in obj.entry6 and obj.entry6 not in suggestions:
					suggestions.append(obj.entry6)
				if queryString in obj.entry7 and obj.entry7 not in suggestions:
					suggestions.append(obj.entry7)

		return Response(suggestions, status=status.HTTP_200_OK)

class GetRemarksSuggestionsAPIView(APIView):

	def get(self, request, *args, **kwargs):
		suggestions = []
		queryString = request.GET.get('queryString')
		querySet = remarksModel.objects.all()

		if querySet:
			for obj in querySet:
				if queryString in obj.entry1 and obj.entry1 not in suggestions:
					suggestions.append(obj.entry1)
				if queryString in obj.entry2 and obj.entry2 not in suggestions:
					suggestions.append(obj.entry2)
				if queryString in obj.entry3 and obj.entry3 not in suggestions:
					suggestions.append(obj.entry3)
				if queryString in obj.entry4 and obj.entry4 not in suggestions:
					suggestions.append(obj.entry4)
				if queryString in obj.entry5 and obj.entry5 not in suggestions:
					suggestions.append(obj.entry5)
				if queryString in obj.entry6 and obj.entry6 not in suggestions:
					suggestions.append(obj.entry6)
				if queryString in obj.entry7 and obj.entry7 not in suggestions:
					suggestions.append(obj.entry7)

		return Response(suggestions, status=status.HTTP_200_OK)

class GetOpenFollowUpAppointmentsList(ListAPIView):
	serializer_class = RetrieveVisitSerializer

	def get_queryset(self, *args, **kwargs):
		currentDate = ((datetime.now().replace(tzinfo=timezone(timedelta(hours=3))))+timedelta(days=1)).date()
		queryset = visitModel.objects.filter(
			Q(followUpStatus='Open') &
			Q(followUpDate__lte=currentDate)
		)
		return queryset

class getPreviousMergedSessionsAPIView(ListAPIView):
	serializer_class = RetrieveVisitSerializer

	def get_queryset(self, *args, **kwargs):
		visit_pk = self.kwargs['visit_pk']
		visitObj = get_object_or_404(visitModel,pk=visit_pk)
		queryset = merged.objects.filter(next=visitObj)
		visitObjsList = []
		if queryset:
			for obj in queryset:
				visitObjsList.append(obj.previous)
		return visitObjsList

class getNextMergedSessionsAPIView(ListAPIView):
	serializer_class = RetrieveVisitSerializer

	def get_queryset(self, *args, **kwargs):
		visit_pk = self.kwargs['visit_pk']
		visitObj = get_object_or_404(visitModel,pk=visit_pk)
		queryset = merged.objects.filter(previous=visitObj)
		visitObjsList = []
		if queryset:
			for obj in queryset:
				visitObjsList.append(obj.next)
		return visitObjsList
