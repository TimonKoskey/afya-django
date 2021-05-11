from django.contrib.auth import get_user_model
from rest_framework.serializers import (
	ModelSerializer,
	SerializerMethodField,
)

# from authentication.models import AfyaAppUser

USER = get_user_model()

class UserDetailsSerializer(ModelSerializer):

	class Meta:
		model = USER
		fields = [
			  'id',
		      'username',
              'first_name',
              'last_name',
              'email',
			  'is_superuser',
			  'is_staff',
			  'is_active' ]

	def create(self, validated_data):
		newUser = USER(
			username = validated_data.get('username', ''),
			first_name = validated_data.get('first_name', ''),
			last_name = validated_data.get('last_name', ''),
			email = validated_data.get('email', ''),
		)
		password = newUser.first_name + newUser.last_name
		newUser.set_password(password)

		newUser.save()
		return newUser

# class AfyaAppUserSerializer(ModelSerializer):
# 	user = SerializerMethodField()
#
# 	class Meta:
# 		model = AfyaAppUser
# 		fields = [
# 			'id',
# 			'user',
# 			'is_superuser',
# 			'is_admin',
# 			'is_staff',
# 			'is_blocked'
# 		]
#
# 	def get_user(self,obj):
# 		user = UserDetailsSerializer(obj.user).data
# 		return user
