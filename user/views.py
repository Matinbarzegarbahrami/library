from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import *
from .forms import *
from .serilizers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema,  OpenApiExample, OpenApiResponse   

# region DRF
class AllUsersAPIView(APIView):
    @extend_schema(
        request=AllUsersList,
        responses={201: AllUsersList},
        description = "this api is for get all users list"
    )
    def get(self, request):
        users = User.objects.filter(is_active=True)
        serializer = AllUsersList(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDeatailAPIView(APIView):
    @extend_schema(
        request=UsersDetailSerializer,
        responses={201: UsersDetailSerializer},
        description = "this api is for get user detail"
    )
    def get(self, request, username):
        user = get_object_or_404(User,username=username)
        serializer = UsersDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreatBookAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=BookSerializer,
        responses={201: BookSerializer},
        description = "this api is for create new post"
    )
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ManageBookAPIView(APIView):
    permission_classes=[IsAuthenticated]
    
    @extend_schema(
        request=BookSerializer,
        responses={201: BookSerializer},
        description = "this api is for update and delete posts"
    )
    
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
    @extend_schema(
        request=AllBooksSerializer,
        responses={201: AllBooksSerializer},
        description = "this api is for create new post"
    )
    def get(self,request):
        books = Books.objects.all().order_by('-created')
        serializer = AllBooksSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DetailBookAPIView(APIView):
    @extend_schema(
        request = AllBooksSerializer,
        responses={201: AllBooksSerializer},
        description = "this api is for get detail of book"
    )
    def get(self, request, id):
        book = get_object_or_404(Books, id=id)
        serializer = AllBooksSerializer(book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchBookAPIView(APIView):
    @extend_schema(
        request=AllBooksSerializer,
        responses={201: AllBooksSerializer},
        description = "this api is for search in posts"
    )
    def get(self, request, query):
        books = Books.objects.filter(Q(authur__name__icontains=query)|
                                    Q(name__icontains=query)|
                                    Q(summery__icontains=query))
        serializer = AllBooksSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FilterByGenreAPIView(APIView):
    @extend_schema(
        request=AllBooksSerializer,
        responses={201: AllBooksSerializer},
        description = "this api is for filter by genre"
    )
    def get(self, request, query):
        books = Books.objects.filter(genre__name=query)
        serializer = AllBooksSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class ProfileAPIView(APIView):
    @extend_schema(
        description = "if user loged in, return user information",
        responses={
            200: OpenApiResponse(response=ProfileSerializer, description="user profile"),
            401: OpenApiResponse(description="Need for authentication")
        },
        examples=[
            OpenApiExample
                (
                "succses",
                value=
                    {
                    "username": "username",
                    "first_name": "name",
                    "last_name": "last name",
                    "bio":  "book lover",
                    "books": 
                        [
                            {
                                "id": 1,
                                "owner": "username",
                                "authur": 
                                    {
                                    "id": 1,
                                    "name": "authur",
                                    "slug": "authur"
                                    },
                                "genre": [
                                    {
                                        "id": 1,
                                        "name": "action",
                                        "slug": "action"
                                    }
                                ],
                                "name": "book name",
                                "summery": "story about book",
                                "user_point": 10
                            },
                        ]
                    },response_only=True
                )
        ],
        tags=["Profile"]
        )
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"message": "please log in first"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EditProfileAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def put(self, request):
        user = request.user
        serializer = EditProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        
        
class ChangeUsernameAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def put(self, request):
        user = request.user
        serializer = EditusernameSeriaizer(user, data=request.data)

        if serializer.is_valid():
            new_username = serializer.validated_data.get("username")
            if user.username == new_username:
                return Response({"message":"The new and old usernames are the same."})
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class ChangePasswordAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def put(self, request):
        user = request.user
        serializer = EditusernameSeriaizer(user, data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data.get("password"))
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# endregion

# region viewbase
def all_users(request):
    users = User.objects.filter(is_active=True)
    return render(request, "all-users.html", {'users':users})
# endregion