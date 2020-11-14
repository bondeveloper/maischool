from django.urls import path, include

from dj_rest_auth.registration.views import VerifyEmailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'account'

urlpatterns = [

    path('auth/', include('dj_rest_auth.urls'), name='auth'),
    path('auth/registration/', include('dj_rest_auth.registration.urls'),
         name='auth_registration'),
    path('auth/account-confirm-email/', VerifyEmailView.as_view(),
         name='account_email_verification_sent'),
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(),
         name='token_verify'),
]
