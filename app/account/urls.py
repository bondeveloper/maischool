from django.urls import path, include

from account import views

app_name = 'account'

urlpatterns = [
    path('', views.RetrieveAccountView.as_view(), name="view"),

    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path(
        'dj-rest-auth/registration/',
        include('dj_rest_auth.registration.urls')
    ),
    path('', include('allauth.urls')),
]
