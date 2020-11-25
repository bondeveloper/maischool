from django.urls import path
from school.views import CategoryCreateAPIView, UpdateCategoryView, \
                         CategoryListAPIView, DestroyCategoryView, \
                         ViewCategoryView, SchoolCreateAPIView, \
                         SchoolListAPIView, UpdateSchoolView, \
                         DeleteSchoolView, RetrieveSchoolAPIView, \
                         SubjectCreateAPIView, SubjectListAPIView

app_name = 'school'

urlpatterns = [
    path('category/', CategoryListAPIView.as_view(),
         name='category-list'),
    path('category/create/', CategoryCreateAPIView.as_view(),
         name='category-create'),
    path('category/<int:pk>/update/', UpdateCategoryView.as_view(),
         name='category-update'),
    path('category/<int:pk>/delete/', DestroyCategoryView.as_view(),
         name='category-delete'),
    path('category/<int:pk>/view/', ViewCategoryView.as_view(),
         name='category-view'),
    path('create/', SchoolCreateAPIView.as_view(), name="create"),
    path('', SchoolListAPIView.as_view(), name="list"),
    path('<int:pk>/update/', UpdateSchoolView.as_view(), name="update"),
    path('<int:pk>/delete/', DeleteSchoolView.as_view(), name="delete"),
    path('<int:pk>/', RetrieveSchoolAPIView.as_view(), name="retrieve"),
    path('subject/create/', SubjectCreateAPIView.as_view(),
         name='subject-create'),
    path('subject/',  SubjectListAPIView.as_view(),
         name='subject-list'),
]
