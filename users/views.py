from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone

from datetime import datetime

from users.models import User, Friendship, Schedule
from users.forms import LoginForm, SignupForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer, UserSignupSerializer, UserFriendshipSerializer, ScheduleSerializer

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
        users = User.objects.filter(is_deleted=False).all()
        serializer = UserSerializer(users, many=True)
        data = {
            "count": len(serializer.data),
            "users": serializer.data
        }

        return create_response(2000, "Success", data)

    try:
        user = User.objects.get(uuid=uuid, is_deleted=False)
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
        user = User.objects.get(uuid=uuid, is_deleted=False)
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
    user_uuid = request.user.uuid

    if not user_uuid:
        data = {}
        return create_response(4001, "유저 uuid가 없습니다.", data, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(uuid=user_uuid)

        if user.is_deleted:
            data = {}
            return create_response(4003, "이미 탈퇴한 유저입니다.", data, status=status.HTTP_400_BAD_REQUEST)
        
        Friendship.objects.filter(following_user=user).update(is_deleted=True)
        Friendship.objects.filter(followed_user=user).update(is_deleted=True)

        user.is_deleted = True
        user.delete_at = timezone.now()
        user.save()

        data = {
            "count": 1,
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
    
    is_deleted_user = User.objects.filter(email=email, is_deleted=True).exists()
    if is_deleted_user:
        data = {}
        return create_response(4003, "탈퇴한 유저입니다.", data, status=status.HTTP_400_BAD_REQUEST)

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
        user = User.objects.get(uuid=uuid, is_deleted=False)
        following = user.following_user_uuid.all().filter(is_deleted=False)
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
        user = User.objects.get(uuid=uuid, is_deleted=False)
        follower = user.followed_user_uuid.all().filter(is_deleted=False)
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
        user = User.objects.get(uuid=uuid, is_deleted=False)
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
        user = User.objects.get(uuid=uuid, is_deleted=False)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_schedule(request):
    user_uuid = request.user.uuid

    schedule = Schedule.objects.filter(uuid=user_uuid, is_deleted=False)
    serializer = ScheduleSerializer(schedule, many=True)

    data = {
        "count": len(serializer.data),
        "schedules": serializer.data
    }

    return create_response(2000, "Success", data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_schedule(request):
    user_uuid = request.user.uuid
    data = request.data.copy()
    data['uuid'] = user_uuid
    serializer = ScheduleSerializer(data=data)

    local_timezone = timezone.get_default_timezone()
    start_time = timezone.make_aware(datetime.fromisoformat(data.get('start_time', '')), local_timezone)
    end_time = timezone.make_aware(datetime.fromisoformat(data.get('end_time', '')), local_timezone)

    if not start_time or not end_time:
        return create_response(4003, "시작 시간과 종료 시간을 모두 입력해주세요.", {}, status=status.HTTP_400_BAD_REQUEST)

    if start_time >= end_time:
        return create_response(4004, "시작 시간은 종료 시간보다 이전이어야 합니다.", {}, status=status.HTTP_400_BAD_REQUEST)

    now = timezone.now()
    if start_time < now or end_time < now:
        return create_response(4005, "과거의 시간에 스케줄을 생성할 수 없습니다.", {}, status=status.HTTP_400_BAD_REQUEST)

    overlap_schedules = Schedule.objects.filter(uuid=user_uuid, start_time__lt=data['end_time'], end_time__gt=data['start_time'])
    if overlap_schedules.exists():
        return create_response(4002, "이미 등록된 일정이 있습니다.", {}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        serializer.save()

        data = {
            "count": 1,
            "schedule": serializer.data
        }
        return create_response(2000, "Success", data)
    
    messages = {}
    for key, value in serializer.errors.items():
        messages[key] = value[0]
        
    return create_response (4001, messages, {}, status=status.HTTP_400_BAD_REQUEST)
