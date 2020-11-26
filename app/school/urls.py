from django.urls import path
from school import views

app_name = 'school'

urlpatterns = [
    path('category/', views.CategoryListAPIView.as_view(),
         name='category-list'),
    path('category/create/', views.CategoryCreateAPIView.as_view(),
         name='category-create'),
    path('category/<int:pk>/update/', views.CategoryUpdateAPIView.as_view(),
         name='category-update'),
    path('category/<int:pk>/delete/', views.CategoryDestroyAPIView.as_view(),
         name='category-delete'),
    path('category/<int:pk>/view/', views.CategoryRetrieveAPIView.as_view(),
         name='category-view'),

    path('create/', views.SchoolCreateAPIView.as_view(),
         name="create"),
    path('', views.SchoolListAPIView.as_view(), name="list"),
    path('<int:pk>/update/', views.SchoolUpdateAPIView.as_view(),
         name="update"),
    path('<int:pk>/delete/', views.SchoolDeleteAPIView.as_view(),
         name="delete"),
    path('<int:pk>/', views.SchoolRetrieveAPIView.as_view(),
         name="retrieve"),

    path('subject/create/', views.SubjectCreateAPIView.as_view(),
         name='subject-create'),
    path('subject/',  views.SubjectListAPIView.as_view(),
         name='subject-list'),
    path('subject/<int:pk>/update/', views.SubjectUpdateAPIView.as_view(),
         name='subject-update'),
    path('subject/<int:pk>/delete/', views.SubjectDestroyAPIView.as_view(),
         name='subject-delete'),
    path('subject/<int:pk>/view/', views.SubjectRetrieveAPIView.as_view(),
         name='subject-view'),
]
