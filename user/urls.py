from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('all-users/',views.AllUsersAPIView.as_view(), name="all-user"),
    path('user/<str:username>/', views.UserDeatailAPIView.as_view(), name="user-detail"),
    path("new-book/", views.CreatBookAPIView.as_view(), name="new-book"),
    path('book/<int:id>/', views.ManageBookAPIView.as_view(), name="create-book"),
    path('book-list/', views.AllbooksAPIView.as_view(), name="all-books"),
    path('book-detail/<int:id>/', views.DetailBookAPIView.as_view(), name="detail-book"),
    path('view/all-users', views.all_users, name="all-users-view"),
]
