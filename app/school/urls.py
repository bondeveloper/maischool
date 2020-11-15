from django.urls import path
from school.views import CreateCategoryView, UpdateCategoryView, \
                         ListCategoryView, DestroyCategoryView, \
                         ViewCategoryView

app_name = 'school'

urlpatterns = [
    path('category/', ListCategoryView.as_view(),
         name='category-list'),
    path('category/create/', CreateCategoryView.as_view(),
         name='category-create'),
    path('category/<int:pk>/update/', UpdateCategoryView.as_view(),
         name='category-update'),
    path('category/<int:pk>/delete/', DestroyCategoryView.as_view(),
         name='category-delete'),
    path('category/<int:pk>/view', ViewCategoryView.as_view(),
         name='category-view'),
]
