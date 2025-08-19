from rest_framework import serializers
from user.models import User
from book.models import *

# <========books========>
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']


class AuthurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authur
        fields = ['id', 'name', 'slug']


class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    authur = AuthurSerializer()
    owner = serializers.StringRelatedField()
    class Meta:
        model = Books
        fields = [
            'id', 'owner', 'authur','genre',
            'name','summery', 'user_point'
        ]



class AllUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ["username","first_name", "last_name","phone",
                    "email","is_active",]

class UserDetailSerializer(serializers.ModelSerializer):
    book_owner = BookSerializer(many=True, read_only=True)
    class Meta:
        model=User
        fields = ["username","first_name", "last_name","phone",
                    "email","is_active","book_owner","is_staff"]
        read_only_fields=["username","first_name", "last_name","phone",
                        "email","book_owner"]

class AllReportsSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    class Meta:
        model=Report
        fields = ["book", "report_type", "text", "date"]
        read_only_fields = ["book", "report_type", "text", "date"]