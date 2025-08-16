from django.urls import path, include
from . import views
from rest_framework_simplejwt import views as jwt_views

app_name = "config"

urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('login/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('signup/', views.SignupAPIView.as_view(), name="signup")
]
