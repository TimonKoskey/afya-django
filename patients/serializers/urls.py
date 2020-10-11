from django.urls import path

from .views import (
	CreatePatientAPIView,
    PatientsListAPIView,
    PatientRetrieveUpdateDestroyAPIView,
	CheckIfPatientRecordsExistAPIView
)

urlpatterns = [
	path('check', CheckIfPatientRecordsExistAPIView.as_view()),
    path('add', CreatePatientAPIView.as_view()),
    path('list', PatientsListAPIView.as_view()),
    path('patient/details/<int:pk>', PatientRetrieveUpdateDestroyAPIView.as_view()),
]
