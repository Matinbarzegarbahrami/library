from django import forms
from .models import *
# clean point book

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = "__all__"

class AuthurForm(forms.ModelForm):
    class Meta:
        model = Authur
        fields = "__all__"

class BooksForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = "__all__"
    
    def clean_user_point(self):
        user_point = self.cleaned_data.get("user_point")
        
        if user_point is None:
            raise forms.ValidationError("Point is required.")
        
        if not (0 <= user_point <= 10):
            return user_point
        else:
            raise forms.ValidationError("point is between 0 to 10")

