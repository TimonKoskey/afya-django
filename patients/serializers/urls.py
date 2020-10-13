from django.urls import path

from .views import (
	CreatePatientAPIView,
    PatientsListAPIView,
    PatientRetrieveUpdateDestroyAPIView,
	CheckIfPatientRecordsExistAPIView,
	UpdatePatientDetailsAPIView
)

urlpatterns = [
	path('check', CheckIfPatientRecordsExistAPIView.as_view()),
    path('add', CreatePatientAPIView.as_view()),
    path('list', PatientsListAPIView.as_view()),
    path('patient/details/<int:pk>', PatientRetrieveUpdateDestroyAPIView.as_view()),
	path('patient/details/update/<int:patient_pk>', UpdatePatientDetailsAPIView.as_view()),
]
