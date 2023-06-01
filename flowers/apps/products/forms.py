from django import forms
from django.contrib.auth.forms import AuthenticationForm

from apps.products.models import Reviews, Comments


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('name', 'text')
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
