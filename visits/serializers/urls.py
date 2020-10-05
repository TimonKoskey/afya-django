from django.urls import path

from .views import (
    CreateNewVisitAPIView,
    AllPatientVisitsListAPIView,
    ActiveVisitsListAPIView,
    RetrieveVisitAPIView,
    UpdateVisitAPIView,
    DeleteVisitAPIView,
    getVisitsByDateAPIView,
    FollowUpVisitsAPIView,
    CreateSessionPaymentInfoAPIView,
    getSessionPaymentsListAPIView,
    RetrieveUpdateDeleteSessionPaymentAPIView,
    CreateSessionComplaintsAPIView,
    RetrieveUpdateDeleteSessionComplaintsAPIView
)

urlpatterns = [
    path('create/<int:patient_pk>', CreateNewVisitAPIView.as_view()),
    path('patient/visits/history/<int:patient_pk>', AllPatientVisitsListAPIView.as_view()),
    path('list/active', ActiveVisitsListAPIView.as_view()),
    path('list/follow-up', FollowUpVisitsAPIView.as_view()),
    path('list/by-date', getVisitsByDateAPIView.as_view()),
    path('session/details/get/<int:pk>', RetrieveVisitAPIView.as_view()),
    path('session/details/update/<int:visit_pk>', UpdateVisitAPIView.as_view()),
    path('session/details/delete/<int:pk>', DeleteVisitAPIView.as_view()),
    path('payment/create/<int:visit_pk>', CreateSessionPaymentInfoAPIView.as_view()),
    path('payments/list/<int:visit_pk>', getSessionPaymentsListAPIView.as_view()),
    path('payment/details/<int:pk>', RetrieveUpdateDeleteSessionPaymentAPIView.as_view()),
    path('complaints/create/<int:pk>', CreateSessionComplaintsAPIView.as_view()),
    path('complaints/details/<int:pk>', RetrieveUpdateDeleteSessionComplaintsAPIView.as_view()),
]
