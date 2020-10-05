from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .serializers import UserDetailsSerializer

USER = get_user_model()

class UserDataAPIView(APIView):

    def get(self, request, *args, **kwargs):
        userSerializer = UserDetailsSerializer(request.user)
        return Response(userSerializer.data, status=status.HTTP_200_OK)
