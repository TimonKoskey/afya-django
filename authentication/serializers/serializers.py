from django.contrib.auth import get_user_model
from rest_framework.serializers import (
	ModelSerializer,
	SerializerMethodField,
)

USER = get_user_model()

class UserDetailsSerializer(ModelSerializer):

    class Meta:
        model = USER
        fields = [
		      'username',
              'first_name',
              'last_name',
              'email',
              'is_staff',
              'is_superuser'
		]
