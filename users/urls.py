from django.urls import path
from users.views import login_view

app_name = "users"
urlpatterns = [
    path('', login_view, name="login"),
]