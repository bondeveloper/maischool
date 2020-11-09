from django.urls import path
from school.views import CreateCategoryView

app_name = 'school'

urlpatterns = [
    path('category/create/', CreateCategoryView.as_view(),
         name='category-create')
]
