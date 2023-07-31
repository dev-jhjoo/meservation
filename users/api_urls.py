from django.urls import path
from users.views import user_signup, user_info, user_login, user_following, user_followers, user_follow, user_unfollow, user_withdraw, get_schedule, create_schedule

app_name = "users"

urlpatterns = [
    path('info/', user_info, name="api-user-detail"),
    path('signup/', user_signup, name="api-signup"),
    path('withdraw/', user_withdraw, name="api-withdraw"),
    path('login/', user_login, name='api-login'),

    path('following/', user_following, name='api-following'),
    path('followers/', user_followers, name='api-followers'),
    path('follow/', user_follow, name='api-follow'),
    path('unfollow/', user_unfollow, name='api-unfollow'),

    path('schedule/', get_schedule, name='api-schedule'),
    path('schedule/create/', create_schedule, name='api-schedule'),
    # path('schedule/delete/', delete_schedule, name='api-schedule'),
]