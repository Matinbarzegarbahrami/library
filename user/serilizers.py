from rest_framework import serializers
from .models import *
from book.models import *   


# region book 
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']

class AuthurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authur
        fields = ['id', 'name', 'slug']

class BookSerializer(serializers.ModelSerializer):
    authur = serializers.SlugRelatedField(
        queryset=Authur.objects.all(),
        slug_field='name'
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Books
        fields = ['id', 'owner', 'authur', 'genre', 'name', 'summery', 'user_point']
        read_only_fields = ['owner']

    def validate_user_point(self, value):
        if not (0 <= value <= 10):
            raise serializers.ValidationError("point must be between 0 and 10.")
        return value

class AllBooksSerializer(serializers.ModelSerializer):
    authur = serializers.SlugRelatedField(
        queryset=Authur.objects.all(),
        slug_field='name'
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Books
        fields = ['id', 'owner', 'authur', 'genre', 'name', 'summery', 'user_point']
        read_only_fields = ['id', 'owner', 'authur', 'genre', 'name', 'summery', 'user_point']

class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    authur = AuthurSerializer(read_only=True)
    owner = serializers.StringRelatedField()

    class Meta:
        model = Books
        fields = ['id', 'owner', 'authur', 'genre', 'name', 'summery', 'user_point']

# endregion

# region user

class UsersDetailSerializer(serializers.ModelSerializer):
    book_owner = BookDetailSerializer(many=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'bio', "book_owner"]

class AllUsersList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'bio']

# endregion