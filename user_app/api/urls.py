from django.urls import path
# this gives us access token if we send our username and password.
from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user_app.api.views import registration_view, logout_view


urlpatterns = [
    path("login/", obtain_auth_token, name='login'),
    path("register/", registration_view, name='register'),
    path("logout/", logout_view, name='logout'),

    # JWT
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #this URL is going to generate (2)tokens
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
