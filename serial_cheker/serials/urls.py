from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.SerialList.as_view(), name='home-page'),
    path('top_10/', views.Top10View.as_view(), name='top-10'),
    path('adding/', views.AddingTvShows.as_view(), name='add-page'),
    path('registration/', views.Registration.as_view(), name='registration'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('genres/', views.GenresView.as_view()),
    path('genres/<int:genre_id>/', views.SerialByGenres.as_view(), name='filter-genres'),
    path('<slug:slug_title>/', views.PageViews.as_view(), name='page-view'),
]

