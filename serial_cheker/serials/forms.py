from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

from .models import *
from django import forms


class AddingTvShow(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['platform'].empty_label = 'Канал не выбран'


    class Meta:
        model = Serials
        fields = ['title', 'rating', 'details', 'platform', 'main_image']
        labels = {
            'title': 'Название',
            'rating': 'Рейтинг',
            'details': 'Описание',
            'main_image': "Добавить фотографию",
            'platform': 'Канал',
        }


class AddingPhoto(forms.ModelForm):
    class Meta:
        model = ImagesSerial
        fields = ['photos']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['username', 'email', 'comment', 'rating']
        labels = {
            'username': 'Имя Пользователя',
            'email': 'Почтовый ящик',
            'comment': 'Отзыв',
            'rating': "Рейтинг",
        }


class UserRegistration(UserCreationForm):
    username = forms.CharField(
        label='Имя Пользователя',
        widget=forms.TextInput(attrs={'cols': 40, 'row': 10}))
    email = forms.EmailField(
        label='Почта',
        widget=forms.EmailInput(attrs={'cols': 40, 'row': 10}))
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'cols': 40, 'row': 10}))
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'cols': 40, 'row': 10}))
    captcha = ReCaptchaField(widget=ReCaptchaV3(attrs={'required_score': 0.85, }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'captcha']


class Login(AuthenticationForm):
    username = forms.CharField(
        label='Имя Пользователя',
        widget=forms.TextInput(attrs={'cols': 40, 'row': 10}))
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'cols': 40, 'row': 10}))
