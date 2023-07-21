from django.urls import path
from users.views import UserSignup, users_info, user_info, user_login, user_following, user_followers, user_follow, user_unfollow

app_name = "users"

urlpatterns = [
    path('info/', users_info, name="api-info"),
    path('info/<uuid:uuid>/', user_info, name="api-user-detail"),
    path('signup/', UserSignup.as_view(), name="api-signup"),
    path('login/', user_login, name='api-login'),

    path('following/', user_following, name='api-following'),
    path('followers/', user_followers, name='api-following'),
    path('follow/', user_follow, name='api-follow'),
    path('unfollow/', user_unfollow, name='api-unfollow'),
]