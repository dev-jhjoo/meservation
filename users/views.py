from django.shortcuts import render, redirect
from users.forms import LoginForm, SignupForm
from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from users.models import User
from users.serializers import UserSerializer


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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
