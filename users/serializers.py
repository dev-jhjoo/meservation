from rest_framework import serializers
from users.models import User, Friendship

class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'uuid', 'email', 'nickname', 'first_name', 'last_name', 'description', 'status_message', 'profile_image', 'following')

    def get_following(self, obj):
        return [user.uuid for user in obj.following.all()]

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

class UserFriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('following_user_id', 'followed_user_id')