from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('all-users/',views.AllUsersAPIView.as_view(), name="all-user"),
    path('user/<str:username>/', views.UserDeatailAPIView.as_view(), name="user-detail"),
    path('new-book/', views.CreateBookAPIView.as_view(), name="create-book"),
    path('view/all-users', views.all_users, name="all-users-view"),
]
