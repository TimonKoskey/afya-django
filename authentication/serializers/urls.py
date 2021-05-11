from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import (
    UserDataAPIView,
    CreateUserAPIView,
    GetUsersListAPIView,
    RetrieveUpdateDestroyUserAPIView,
    DeleteUserAPIView,
    ConfirmCurrentPasswordAPIView,
    ChangePasswordAPIView
)

urlpatterns = [
    path('api-token-auth', obtain_jwt_token),
    path('details', UserDataAPIView.as_view()),
    path('create', CreateUserAPIView.as_view()),
    path('list/users', GetUsersListAPIView.as_view()),
    path('user/delete/<int:pk>', DeleteUserAPIView.as_view()),
    path('user/details/<int:pk>', RetrieveUpdateDestroyUserAPIView.as_view()),
    path('user/update/<int:pk>', RetrieveUpdateDestroyUserAPIView.as_view()),
    path('user/retrieve/<int:pk>', RetrieveUpdateDestroyUserAPIView.as_view()),
    path('password/confirm', ConfirmCurrentPasswordAPIView.as_view()),
    path('password/change', ChangePasswordAPIView.as_view()),
]
