from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from user import views

app_name = 'user'

urlpatterns = [
    path('', views.ListUserView.as_view(), name="list"),
    path('view/<int:pk>', views.RetrieveUserView.as_view(), name="view"),

    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('jwt-auth/', obtain_jwt_token),
    path('jwt-refresh/', obtain_jwt_token),
]
