from django import forms
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username","first_name","last_name","email",
                    "phone","date_joined"]
        
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        if not phone.isdigit():
            raise forms.ValidationError('phone must be a number.')
        
        if self.instance.pk:
            if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Phone already exists.')
        else:
            if User.objects.filter(phone=phone).exists():
                raise forms.ValidationError('Phone already exists.')
        if len(phone) != 11:
            raise forms.ValidationError('phone must have 11 digits.')
        
        return phone
    

