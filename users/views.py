from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login

from users.models import User
from users.forms import LoginForm, SignupForm

# from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer, UserSignupSerializer, UserFriendshipSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                # 추후 메인 페이지로 경로 수정 필요
                response = redirect("/main")
                return response
            else:
                form.add_error(None, "이메일 또는 비밀번호가 올바르지 않습니다.")
        context = {
            "form": form,
        }
        return render(request, 'users/login.html', context)
    else:
        form = LoginForm()
        context = {
            "form": form,
        }
        return render(request, 'users/login.html', context)

def signup_view(request):
    if request.method == "POST":
        print("hahaha")
        form = SignupForm(data=request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/users/login")
    else:
        form = SignupForm()

    context = {
        "form": form,
    }
    return render(request, 'users/signup.html', context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_info(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_info(request, uuid):
    if request.method == "GET":
        try:
            user = User.objects.get(uuid=uuid)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"statusMessage": "잘못된 요청", "resultCode": "400"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "POST":
        user = User.objects.get(uuid=uuid)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserSignup(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, email=email, password=password)
    if user is not None:
        try:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, 
            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"statusMessage": "잘못된 요청", "resultCode": "400"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_following(request):
    uuid = request.data.get("uuid")
    try:
        user = User.objects.get(uuid=uuid)
        following = user.following_user_id.all()
        serializer = UserFriendshipSerializer(following, many=True)

        response_data = {
            "resultCode": 200,
            "resultMessage": {
                "count": len(serializer.data),
                "friendList": serializer.data
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"statusMessage": "잘못된 요청", "resultCode": "400"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_followers(request):
    uuid = request.data.get("uuid")
    try:
        user = User.objects.get(uuid=uuid)
        follower = user.followed_user_id.all()
        print(follower)
        serializer = UserFriendshipSerializer(follower, many=True)

        response_data = {
            "resultCode": 200,
            "resultMessage": {
                "count": len(serializer.data),
                "friendList": serializer.data
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"statusMessage": "잘못된 요청", "resultCode": "400"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_follow(request):
    uuid = request.data.get("uuid")
    try:
        user = User.objects.get(uuid=uuid)
        target_user = request.user
        if user == target_user:
            return Response({"statusMessage": "잘못된 요청", "resultCode": "400"}, status=status.HTTP_400_BAD_REQUEST)
        elif user.following.filter(uuid=target_user.uuid).exists():
            return Response({"statusMessage": "이미 팔로우 중인 사용자입니다.", "resultCode": "400"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.following.add(target_user)
        return Response({"statusMessage": "팔로우 성공", "resultCode": "200"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"statusMessage": "잘못된 요청", "resultCode": "400"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_unfollow(request):
    uuid = request.data.get("uuid")
    try:
        user = User.objects.get(uuid=uuid)
        target_user = request.user
        if user == target_user:
            return Response({"statusMessage": "잘못된 요청", "resultCode": "400"}, status=status.HTTP_400_BAD_REQUEST)
        elif not user.following.filter(uuid=target_user.uuid).exists():
            return Response({"statusMessage": "팔로우 중인 사용자가 아닙니다.", "resultCode": "400"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.following.remove(target_user)
        return Response({"statusMessage": "언팔로우 성공", "resultCode": "200"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"statusMessage": "잘못된 요청", "resultCode": "400"}, status=status.HTTP_400_BAD_REQUEST)
