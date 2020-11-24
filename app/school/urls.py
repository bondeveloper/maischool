from django.urls import path
from school.views import CreateCategoryView, UpdateCategoryView, \
                         ListCategoryView, DestroyCategoryView, \
                         ViewCategoryView, CreateSchoolView, ListSchoolView, \
                         UpdateSchoolView, DeleteSchoolView, \
                         RetrieveSchoolAPIView

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
    path('category/<int:pk>/view/', ViewCategoryView.as_view(),
         name='category-view'),
    path('create/', CreateSchoolView.as_view(), name="create"),
    path('', ListSchoolView.as_view(), name="list"),
    path('<int:pk>/update/', UpdateSchoolView.as_view(), name="update"),
    path('<int:pk>/delete/', DeleteSchoolView.as_view(), name="delete"),
    path('<int:pk>/', RetrieveSchoolAPIView.as_view(), name="retrieve"),
]
