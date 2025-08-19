from django.shortcuts import render, get_object_or_404

from user.models import User
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser


class AllUsersListAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        users = User.objects.all().order_by("-is_active", "-username")
        serializer = AllUserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response({"message":"user deleted"}, status=status.HTTP_200_OK)
    
    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserDetailSerializer(user,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportListAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, requset):
        report = Report.objects.all().order_by('-date')
        serializer = AllReportsSerializer(report, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReportDetailAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, id):
        report = get_object_or_404(Report, id=id)
        serializer = AllReportsSerializer(report, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        report = get_object_or_404(Report, id=id)
        report.delete()
        return Response({"message":"report has deleted"}, status=status.HTTP_200_OK)

