from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('', views.ListUserView.as_view(), name="list"),
    path('detail/<int:pk>', views.RetrieveUserView.as_view(), name="detail"),
]
