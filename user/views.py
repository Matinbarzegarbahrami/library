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

class CreatBookAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ManageBookAPIView(APIView):
    def put(self, request, id):
        user = request.user
        book = get_object_or_404(Books, id=id)

        if user != book.owner:
            return Response({"message": "You are not the owner of this post"}, status=status.HTTP_403_FORBIDDEN)

        serializer = BookSerializer(instance=book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = request.user
        book = get_object_or_404(Books, id=id)
        if user == book.owner:
            book.delete()
            return Response({"message":"book was deleted"}, status=status.HTTP_404_NOT_FOUND)

class AllbooksAPIView(APIView):
    def get(self,request):
        books = Books.objects.all().order_by('-created')
        serializer = AllBooksSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DetailBookAPIView(APIView):
    def get(self, request, id):
        book = get_object_or_404(Books, id=id)
        return Response(
            {
            "owner": str(book.owner),
            "authur": str(book.authur),
            "genre": [str(b.name) for b in book.genre.all()],
            "name": book.name,
            "summery": book.summery,
            "user_point": book.user_point
            }
        )
        
# endregion

# region viewbase
def all_users(request):
    users = User.objects.filter(is_active=True)
    return render(request, "all-users.html", {'users':users})
# endregion