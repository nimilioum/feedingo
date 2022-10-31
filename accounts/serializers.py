from rest_framework.serializers import ModelSerializer, CharField
from .models import User


class UserRegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password",)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        user.save()

        return user
