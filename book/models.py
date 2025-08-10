from django.db import models
from user.models import User
class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    def __str__(self):
        return self.name

class Authur(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField()
    def __str__(self):
        return self.name

class Books(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="book_owner")
    authur = models.ForeignKey(Authur, on_delete=models.CASCADE, related_name="book_authur")
    genre = models.ManyToManyField(Genre, related_name="book_genre")
    name = models.CharField(max_length=100)
    summery = models.TextField()
    user_point = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name