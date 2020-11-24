from django.urls import path, include

app_name = 'account'

urlpatterns = [

    path('auth/', include('dj_rest_auth.urls'), name='auth'),
    path('auth/registration/', include('dj_rest_auth.registration.urls'),
         name='auth_registration'),
]
