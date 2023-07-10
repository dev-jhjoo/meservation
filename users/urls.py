from django.urls import path
from users.views import login_view, signup_view, UsersInfo, UserInfo
from rest_framework import routers
from django.urls import include

app_name = "users"

urlpatterns = [
    path('login/', login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path('info/', UsersInfo.as_view(), name="info"),
    path('info/<uuid:uuid>/', UserInfo.as_view(), name="user-detail"),
]
