from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Serials, Platforms, ImagesSerial, Genres, Comment, Series


# Register your models here.

@admin.register(Serials)
class SerialsAdmin(admin.ModelAdmin):
    list_display = ['title', 'rating', 'budget', 'box_office', 'details', 'genre']
    list_editable = ['rating', 'budget', 'box_office', 'details']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['pk']

    def get_queryset(self, request):
        return Serials.objects.all().select_related('genre').prefetch_related('genre')


@admin.register(Platforms)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['platform']
    prepopulated_fields = {'slug': ('platform',)}


@admin.register(ImagesSerial)
class ImagesSerialAdmin(admin.ModelAdmin):
    list_display = ['pk', 'photos', 'serial']
    list_editable = ['photos', 'serial']


@admin.register(Genres)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    list_editable = ['parent']
    prepopulated_fields = {'slug': (
        'name',
    )}


@admin.register(Series)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'details', 'serial', 'episode_rating']
    list_editable = ['image', 'details', 'serial', 'episode_rating']
    prepopulated_fields = {'slug': (
        'title',
    )}


admin.site.register(Comment, MPTTModelAdmin)
