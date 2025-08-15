from rest_framework import serializers
from .models import User
from book.models import Books, Genre, Authur
from django.utils.text import slugify

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']


class AuthurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authur
        fields = ['id', 'name', 'slug']


class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    authur = AuthurSerializer(read_only=True)
    genre_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    authur_name = serializers.CharField(write_only=True)

    class Meta:
        model = Books
        fields = [
            'id', 'owner', 'authur', 'authur_name',
            'genre', 'genre_names', 'name',
            'summery', 'user_point'
        ]
        read_only_fields = ['id', 'owner', 'authur', 'genre']

    def validate_user_point(self, value):
        if not (0 <= value <= 10):
            raise serializers.ValidationError("point must be between 0 and 10.")
        return value

    def create(self, validated_data):
        genre_names = validated_data.pop('genre_names', [])
        authur_name = validated_data.pop('authur_name')

        authur_obj, _ = Authur.objects.get_or_create(
            name=authur_name,
            defaults={'slug': authur_name.lower().replace(' ', '-')}
        )

        book = Books.objects.create(authur=authur_obj, **validated_data)

        genre_objs = []
        for g in genre_names:
            obj, _ = Genre.objects.get_or_create(
                name=g,
                defaults={'slug': slugify(g)}
            )
            genre_objs.append(obj)

        book.genre.set(genre_objs)

        return book


class AllBooksSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    authur = AuthurSerializer(read_only=True)

    class Meta:
        model = Books
        fields = ['id', 'owner', 'authur', 'genre', 'name', 'summery', 'user_point']


class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    authur = AuthurSerializer(read_only=True)
    owner = serializers.StringRelatedField()

    class Meta:
        model = Books
        fields = ['id', 'owner', 'authur', 'genre', 'name', 'summery', 'user_point']

class UsersDetailSerializer(serializers.ModelSerializer):
    book_owner = BookDetailSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'bio', "book_owner"]


class AllUsersList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'bio']


class ProfileSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'bio', 'books']

    def get_books(self, user):
        return BookDetailSerializer(user.book_owner.all(), many=True).data
