from django.urls import path
from users.views import login_view, signup_view, UserViewSet
from rest_framework import routers
from django.urls import include

app_name = "users"

router = routers.DefaultRouter()
router.register('user', UserViewSet)

urlpatterns = [
    path('login/', login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    # path('v1/api/signup/', signup_api, name="signup_api"),
    path('v1/api/', include(router.urls))
]