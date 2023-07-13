from django.urls import path
from users.views import UsersInfo, UserInfo, UserSignup, UserLogin

app_name = "users"

urlpatterns = [
    path('info/', UsersInfo.as_view(), name="api-info"),
    path('info/<uuid:uuid>/', UserInfo.as_view(), name="api-user-detail"),
    path('signup/', UserSignup.as_view(), name="api-signup"),
    path('login/', UserLogin.as_view(), name='api-login')
]