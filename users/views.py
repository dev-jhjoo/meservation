from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from users.models import User
from users.forms import LoginForm, SignupForm

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer, UserSignupSerializer

from rest_framework_simplejwt.tokens import RefreshToken


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


class UsersInfo(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserInfo(APIView):
    def get_object(self, uuid):
        return User.objects.get(uuid=uuid)

    def get(self, request, uuid):
        try:
            user = self.get_object(uuid)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"statusMessage": "잘못된 요청", "statusCode": "400"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uuid):
        user = self.get_object(uuid)
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

class UserLogin(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            try:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
