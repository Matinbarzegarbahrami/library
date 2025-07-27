from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from .serilizers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated

# region DRF
class AllUsersAPIView(APIView):
    def get(self, request):
        users = User.objects.filter(is_active=True)
        serializer = AllUsersList(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDeatailAPIView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User,username=username)
        serializer = UsersDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateBookAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# endregion

# region viewbase
def all_users(request):
    users = User.objects.filter(is_active=True)
    return render(request, "all-users.html", {'users':users})
# endregion