from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models import Avg, Q, Count
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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
        tv_show = Serials.objects.get(slug=slug_title)
        avg = tv_show.comment.all().aggregate(Avg('rating'))
        comments = Comment.objects.filter(serial_id=tv_show.pk)
        context = self.get_user_context(form=form, serial=tv_show, comments=comments, avg=avg['rating__avg'],)
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


class SerieView(DataMixin, ListView):
    model = Series
    template_name = 'serials/serie.html'
    context_object_name = 'serie'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        tv_show = Serials.objects.get(slug=self.kwargs['serial_slug'])
        rating = Series.objects.values('episode_rating').annotate(Count('pk')).filter(serial__slug=self.kwargs['serial_slug'])
        serial_title = Series.objects.values('title').distinct().filter(serial__slug=self.kwargs['serial_slug'])
        c_def = self.get_user_context(title='Серия Сериала', rating=rating, serial_title=serial_title, tv_show=tv_show)
        return context | c_def

    def get_queryset(self):
        get_object_or_404(Serials, slug=self.kwargs['serial_slug'])
        return Series.objects.filter(serial__slug=self.kwargs['serial_slug']).select_related('serial')


class SerieUpdate(DataMixin, UpdateView):
    model = Series
    template_name = 'serials/serie_update.html'
    fields = ['title', 'episode_rating', 'details', 'image',]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение')
        return context | c_def

    def get_queryset(self):
        return Series.objects.filter(serial__slug=self.kwargs['serial_slug'])

    def get_success_url(self):
        return reverse_lazy('episode', kwargs={'serial_slug': self.kwargs['serial_slug']})


class SerieDelete(DataMixin, DeleteView):
    model = Series
    template_name = 'serials/serie_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Удаление')
        return context | c_def

    def get_queryset(self):
        return Series.objects.filter(serial__slug=self.kwargs['serial_slug'])

    def get_success_url(self):
        return reverse_lazy('episode', kwargs={'serial_slug': self.kwargs['serial_slug']})



class SerieCreate(DataMixin, CreateView):
    form_class = AddingSerie
    template_name = 'serials/serie_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавте серию')
        return context | c_def

    def get_queryset(self):
        return Series.objects.filter(serial__slug=self.kwargs['serial_slug'])

    def form_valid(self, form):
        serial = form.save(commit=False)
        serial.serial = Serials.objects.get(slug=self.kwargs['serial_slug'])
        serial.save()
        series_page = reverse_lazy('episode', kwargs={'serial_slug': self.kwargs['serial_slug']})
        return redirect(series_page)


class EpisodeFilter(SerieView):

    def get_queryset(self):
        if 'episode_rating' in self.request.GET and 'title' in self.request.GET:
            return Series.objects.filter(episode_rating__in=self.request.GET.getlist('episode_rating'),
                                         title__in=self.request.GET.getlist('title'),
                                         serial__slug=self.kwargs['serial_slug'])
        elif 'episode_rating' in self.request.GET:
            return Series.objects.filter(episode_rating__in=self.request.GET.getlist('episode_rating'),
                                         serial__slug=self.kwargs['serial_slug'])
        elif 'title' in self.request.GET:
            return Series.objects.filter(title__in=self.request.GET.getlist('title'),
                                         serial__slug=self.kwargs['serial_slug'])
        else:
            return Series.objects.filter(serial__slug=self.kwargs['serial_slug']).select_related('serial')


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
