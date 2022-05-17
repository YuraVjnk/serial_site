from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models import Avg, Q
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from .forms import *
from .models import *
from .utils import DataMixin


class SerialList(DataMixin, ListView):
    model = Serials
    template_name = 'serials/list_of_serials.html'
    context_object_name = 'serials'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        genres = Genres.objects.all()
        c_def = self.get_user_context(title='Главная страница', genres=genres)
        return context | c_def

    def get_queryset(self):
        return Serials.objects.order_by('pk').select_related('platform').prefetch_related('serials')


class PageViews(DataMixin, View):

    def get(self, request, slug_title):
        form = CommentForm()
        tv_show = Serials.objects.prefetch_related('comment').get(slug=slug_title)
        avg = tv_show.comment.all().aggregate(Avg('rating'))
        comments = Comment.objects.filter(serial_id=tv_show.pk)
        context = self.get_user_context(form=form, serial=tv_show, comments=comments, avg=avg['rating__avg'])
        return render(request, 'serials/serial_page.html', context=context)

    def post(self, request, slug_title):
        form = CommentForm(request.POST)
        tv_show = Serials.objects.get(slug=slug_title)
        current_page = reverse_lazy('page-view', args=[slug_title])
        if form.is_valid():
            obj = form.save(commit=False)
            obj.serial_id = tv_show.pk
            obj.save()
            return redirect(current_page)
        comments = Comment.objects.filter(serial_id=tv_show.pk)
        context = self.get_user_context(form=form, serial=tv_show, comments=comments)
        return render(request, 'serials/serial_page.html', context=context)


class GenresView(ListView):
    model = Genres
    template_name = 'includes/genres.html'
    context_object_name = 'genres'


class SerialByGenres(DataMixin, ListView):
    model = Serials
    template_name = 'serials/genre.html'
    context_object_name = 'genre'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        genres = Genres.objects.all()
        c_def = self.get_user_context(title='Топ десять', genres=genres)
        return context | c_def

    def get_queryset(self):
        return Serials.objects.filter(Q(genre_id=self.kwargs['genre_id']))


class Top10View(DataMixin, ListView):
    model = Serials
    template_name = 'serials/top_10.html'
    context_object_name = 'serials'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Топ десять')
        return context | c_def

    def get_queryset(self):
        return Serials.objects.order_by('-rating')[:5]


class AddingTvShows(DataMixin, CreateView):
    form_class = AddingTvShow
    template_name = 'serials/adding.html'
    success_url = reverse_lazy('home-page')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавте сериал')
        return context | c_def


class Registration(DataMixin, CreateView):
    form_class = UserRegistration
    template_name = 'serials/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return context | c_def

    def form_valid(self, form):
        new_user = form.save()
        login(self.request, new_user)
        return redirect('home-page')


class UserLogin(DataMixin, LoginView):
    form_class = Login
    template_name = 'serials/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Вход')
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('home-page')


def logout_user(request):
    logout(request)
    return redirect('home-page')
