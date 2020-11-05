from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('view/<int:pk>', views.RetrieveUserView.as_view(), name="view"),
    path('list/', views.ListUserView.as_view(), name="list")
]
