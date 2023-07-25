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


def create_response(code, message, data, status=status.HTTP_200_OK):
    return Response({
        "code": code,
        "message": message,
        "data": data
    }, status=status)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_info(request):
    if request.method == 'GET':
        return get_user_info(request)
    elif request.method == 'POST':
        return update_user_info(request)
    
def get_user_info(request):
    uuid = request.data.get("uuid")
    if not uuid:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        data = {
            "count": len(serializer.data),
            "users": serializer.data
        }

        return create_response(2000, "Success", data)

    try:
        user = User.objects.get(uuid=uuid)
        serializer = UserSerializer(user)
        data = {
            "user": serializer.data
        }

        return create_response(2000, "Success", data)
    except User.DoesNotExist:
        data = {
            "count": 0,
            "users": []
        }

        return create_response(4001, "유저가 존재하지 않습니다.", data, status=status.HTTP_400_BAD_REQUEST)

def update_user_info(request):
    uuid = request.data.get("uuid")
    try:
        user = User.objects.get(uuid=uuid)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "count": len(serializer.data),
                "user": serializer.data
            }
            return create_response(2000, "Success", data)
        
        if serializer.error_messages:
            messages = {}
            for field, error in serializer.errors.items():
                messages[field] = error[0]

            return create_response(4001, messages, {}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        data = {
            "count": 0,
            "user": []
        }
        return create_response(2001, "유저가 존재하지 않습니다.", data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def user_signup(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        data = {
                "user": serializer.data
            }

        return create_response(2000, "Success", data)
    
    if serializer.error_messages:
            messages = {}
            for field, error in serializer.errors.items():
                messages[field] = error[0]

            return create_response(4001, messages, {}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_withdraw(request):
    uuid = request.data.get("uuid")

    if not uuid:
        data = {}
        return create_response(4001, "유저 uuid가 없습니다.", data, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(uuid=uuid)

        if user.deleted_at:
            data = {}
            return create_response(4001, "이미 탈퇴한 유저입니다.", data, status=status.HTTP_400_BAD_REQUEST)
        
        user.deleted_at = True
        user.save()

        data = {
            "count": len(UserSerializer(user).data),
            "user": UserSerializer(user).data
        }
        return create_response(2000, "Success", data)
    except User.DoesNotExist:
        data = {}
        return create_response(4001, "유저가 존재하지 않습니다.", data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, email=email, password=password)
    if user is not None:
        try:
            refresh = RefreshToken.for_user(user)

            data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": UserSerializer(user).data
                }

            return create_response(2000, "Success", data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        data = {}
        return create_response(4002, "이메일 또는 비밀번호를 잘못 입력했습니다. 입력하신 내용을 다시 확인해주세요.", data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_followers(request):
    uuid = request.data.get("uuid")
    try:
        user = User.objects.get(uuid=uuid)
        following = user.following_user_uuid.all()
        serializer = UserFriendshipSerializer(following, many=True)

        data = {
            "count": len(serializer.data),
            "friendList": serializer.data
        }

        return create_response(2000, "Success", data)

    except User.DoesNotExist:
        data = {
            "count": 0,
            "friendList": []
        }

        return create_response(4001, "유저가 존재하지 않습니다.", data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_following(request):
    uuid = request.data.get("uuid")
    try:
        user = User.objects.get(uuid=uuid)
        follower = user.followed_user_uuid.all()
        serializer = UserFriendshipSerializer(follower, many=True)

        data = {
            "count": len(serializer.data),
            "friendList": serializer.data
        }

        return create_response(2000, "Success", data)
    except User.DoesNotExist:
        data = {
            "count": 0,
            "friendList": []
        }

        return create_response(4001, "유저가 존재하지 않습니다.", data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_follow(request):
    uuid = request.data.get("uuid")
    try:
        user = User.objects.get(uuid=uuid)
        target_user = request.user
        if user == target_user:
            data = {
                "count": 0,
            }

            return create_response(4001, "자기 자신을 팔로우할 수 없습니다.", data, status=status.HTTP_400_BAD_REQUEST)
        elif user.following.filter(uuid=target_user.uuid).exists():
            data = {
                "count": 0,
            }

            return create_response(4001, "이미 팔로우 중인 사용자입니다.", data, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.following.add(target_user)

            data = {
                "count": 1,
                "followingList": UserFriendshipSerializer(user.following_user_uuid.all(), many=True).data
            }
            return create_response(2000, "Success", data)
    except User.DoesNotExist:
        data = {
            "count": 0,
        }

        return create_response(4001, "유저가 존재하지 않습니다.", data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_unfollow(request):
    uuid = request.data.get("uuid")
    try:
        user = User.objects.get(uuid=uuid)
        target_user = request.user
        if user == target_user:
            data = {
                "count": 0,
            }

            return create_response(4001, "자기 자신을 언팔로우할 수 없습니다.", data, status=status.HTTP_400_BAD_REQUEST)
        elif not user.following.filter(uuid=target_user.uuid).exists():
            data = {
                "count": 0,
            }

            return create_response(4001, "팔로우 중인 사용자가 아닙니다.", data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                "count": 1,
                "unfollowingList": UserFriendshipSerializer(user.following_user_uuid.all(), many=True).data
            }

            user.following.remove(target_user)
            return create_response(2000, "Success", data)

    except User.DoesNotExist:
        data = {
            "count": 0,
        }

        return create_response(4001, "유저가 존재하지 않습니다.", data, status=status.HTTP_400_BAD_REQUEST)

