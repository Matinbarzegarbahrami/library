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
    path('report/<int:id>/', views.ReportAPIView.as_view(), name="report"),
    path('search/<str:query>/', views.SearchBookAPIView.as_view(), name="search"),
    path('genre/<str:query>/', views.FilterByGenreAPIView.as_view(), name="genre"),
    path('view/all-users', views.all_users, name="all-users-view"),
    path('profile/', views.ProfileAPIView.as_view(), name="profile"),
    path('update-profile/', views.EditProfileAPIView.as_view(), name="edit-profile"),
    path('profile/changepassword/', views.ChangePasswordAPIView.as_view(), name="change-password"),
    path('profile/changeusername/', views.ChangeUsernameAPIView.as_view(), name="change-username"),
    
]
