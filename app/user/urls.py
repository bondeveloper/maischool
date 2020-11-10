from django.urls import path, include

from user import views

app_name = 'user'

urlpatterns = [
    path('', views.ListUserView.as_view(), name="list"),
    path('view/<int:pk>', views.RetrieveUserView.as_view(), name="view"),
]
