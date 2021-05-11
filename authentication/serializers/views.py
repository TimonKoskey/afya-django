from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

from rest_framework.generics import (
	ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
)

from .serializers import UserDetailsSerializer
# from authentication.models import AfyaAppUser

USER = get_user_model()

class UserDataAPIView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        userSerializer = UserDetailsSerializer(user)
        # subject, from_email, to = 'OFFICE APPLICATION SECURITY ALERT', 'timonkosy92@gmail.com', 'timonkosy92@gmail.com'
        # text_content = ""
        # html_content = """<p>A user %s %s has logged in to the hospital management application. If this action is unauthorised click the link below to take appropriate actions</p>
        #                     <a href="http://localhost:4200/account/home">http://localhost:4200/account/admin</a>""" %(user.first_name, user.last_name)
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()
        return Response(userSerializer.data, status=status.HTTP_200_OK)

class CreateUserAPIView(APIView):

	def post(self, request, *args, **kwargs):
		userData = request.data
		userSerializer = UserDetailsSerializer(data=userData)
		if userSerializer.is_valid():
			userObj = userSerializer.create(userSerializer.validated_data)
			return Response(UserDetailsSerializer(userObj).data, status=status.HTTP_201_CREATED)
		return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUsersListAPIView(ListAPIView):
    serializer_class = UserDetailsSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = USER.objects.exclude(id=user.id)
        return queryset

class RetrieveUpdateDestroyUserAPIView(RetrieveUpdateDestroyAPIView):
    queryset = USER.objects.all()
    serializer_class = UserDetailsSerializer

class DeleteUserAPIView(DestroyAPIView):
    queryset = USER.objects.all()
    serializer_class = UserDetailsSerializer

class ConfirmCurrentPasswordAPIView(APIView):

	def post(self, request, *args, **kwargs):
		data = request.data
		user = request.user
		passwordConfirmation = user.check_password(data['currentPassword'])
		if passwordConfirmation:
			return Response(status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordAPIView(APIView):

	def post(self, request, *args, **kwargs):
		data = request.data
		user = request.user
		user.set_password(data['newPassword'])
		user.save()
		return Response(UserDetailsSerializer(user).data, status=status.HTTP_201_CREATED)
