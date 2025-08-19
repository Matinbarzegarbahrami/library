from django.urls import path, include
from . import views
app_name = "admin"

urlpatterns = [
    path('user-list/', views.AllUsersListAPIView.as_view(), name="users-list"),
    path('user/<str:username>/', views.UserDetailAPIView.as_view(), name="user-detail"),
    path('reports/', views.ReportListAPIView.as_view(), name="report-list")
]
