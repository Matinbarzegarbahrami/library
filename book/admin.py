from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Authur)
class AuthurAdmin(admin.ModelAdmin):
    list_display = ['name']
    

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['report_type']