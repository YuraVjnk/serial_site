from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django.core.exceptions import ValidationError
from mptt.forms import TreeNodeChoiceField

from .models import *
from django import forms


class AddingTvShow(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['platform'].empty_label = 'Канал не выбран'
        self.fields['genre'].empty_label = 'Канал не выбран'

    class Meta:
        model = Serials
        fields = ['title', 'rating', 'genre', 'details', 'platform', 'main_image', ]
        labels = {
            'title': 'Название',
            'rating': 'Рейтинг',
            'details': 'Описание',
            'main_image': "Добавить фотографию",
            'platform': 'Канал',
            'genre': 'Жанр'
        }


class AddingSerie(forms.ModelForm):

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 40:
            raise ValidationError('Длина названия превышает 40 символов')
        return title

    def clean_details(self):
        details = self.cleaned_data['details']
        if len(details) < 10:
            raise ValidationError('Минимальная длина отзыва 10 символов')
        return details

    class Meta:
        model = Series
        fields = ['title', 'details', 'image', 'episode_rating']
        labels = {
            'title': 'Название',
            'episode_rating': 'Рейтинг',
            'details': 'Описание',
            'image': "Добавить фотографию",
        }

        error_messages = {'episode_rating':
            {
                'max_value': 'Максимальное значение Рейтнга - 10',
                'min_value': 'Максимальное значение Рейтнга - 10'
            },
            'title': {
                'required': 'Данное поле обязательно к заполнению'
            },
        }


class AddingPhoto(forms.ModelForm):
    class Meta:
        model = ImagesSerial
        fields = ['photos']


class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].widget.attrs.update({'class': 'd-none'})
        self.fields['parent'].required = False
        self.fields['parent'].label = ''

    class Meta:
        model = Comment
        fields = ['username', 'email', 'comment', 'parent', 'rating']
        labels = {
            'username': 'Имя Пользователя:',
            'email': 'Почтовый ящик:',
            'comment': 'Отзыв:',
            'rating': "Рейтинг:",
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
        fields = ['username', 'email', 'password1', 'password2']


class Login(AuthenticationForm):
    username = forms.CharField(
        label='Имя Пользователя',
        widget=forms.TextInput(attrs={'cols': 40, 'row': 10}))
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'cols': 40, 'row': 10}))
