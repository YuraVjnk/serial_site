from django.contrib import admin


from .models import Serials, Platforms, ImagesSerial, Genres


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
