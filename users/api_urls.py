from django.urls import path
from users.views import user_signup, user_info, user_login, user_following, user_followers, user_follow, user_unfollow

app_name = "users"

urlpatterns = [
    path('info/', user_info, name="api-user-detail"),
    path('signup/', user_signup, name="api-signup"),
    # paht('signout/', user_signout, name="api-signout"')
    path('login/', user_login, name='api-login'),

    path('following/', user_following, name='api-following'),
    path('followers/', user_followers, name='api-followers'),
    path('follow/', user_follow, name='api-follow'),
    path('unfollow/', user_unfollow, name='api-unfollow'),
]