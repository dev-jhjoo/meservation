from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'uuid', 'email', 'nickname', 'first_name', 'last_name', 'description')

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            nickname=validated_data['nickname'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            description=validated_data.get('description', '')
        )
        return user

    class Meta:
        model = User
        fields = ['id', 'uuid', 'email', 'password', 'nickname', 'first_name', 'last_name', 'description']