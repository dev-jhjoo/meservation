from django.urls import path
from users.views import login_view, signup

app_name = "users"
urlpatterns = [
    path('login/', login_view, name="login"),
    path('signup/', signup, name="signup"),
]