from django.urls import path
from users.views import UserSignup, users_info, user_info, user_login, user_following, user_followers, user_follow

app_name = "users"

urlpatterns = [
    path('info/', users_info, name="api-info"),
    path('info/<uuid:uuid>/', user_info, name="api-user-detail"),
    path('signup/', UserSignup.as_view(), name="api-signup"),
    path('login/', user_login, name='api-login'),

    path('following/<uuid:uuid>/', user_following, name='api-following'),
    path('followers/<uuid:uuid>/', user_followers, name='api-following'),
    path('follow/<uuid:uuid>/', user_follow, name='api-follow'),
]