from django.urls import path

from .views import (
	CreatePatientAPIView,
    PatientsListAPIView,
    PatientRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('add', CreatePatientAPIView.as_view()),
    path('list', PatientsListAPIView.as_view()),
    path('patient/details/<int:pk>', PatientRetrieveUpdateDestroyAPIView.as_view()),
]
