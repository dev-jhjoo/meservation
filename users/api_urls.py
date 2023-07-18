from django.urls import path
from users.views import UserSignup, users_info, user_info, user_login

app_name = "users"

urlpatterns = [
    # path('info/', UsersInfo.as_view(), name="api-info"),
    path('info/', users_info, name="api-info"),
    path('info/<uuid:uuid>/', user_info, name="api-user-detail"),
    path('signup/', UserSignup.as_view(), name="api-signup"),
    path('login/', user_login, name='api-login')
]