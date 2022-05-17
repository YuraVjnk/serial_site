from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

# Create your models here.
from django.urls import reverse
from pytils.translit import slugify


class Platforms(models.Model):
    platform = models.CharField(
        max_length=255)
    slug = models.SlugField(
        max_length=255)

    def __str__(self):
        return self.platform


class Genres(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('filter-genres', args=[self.pk])


class Serials(models.Model):
    title = models.CharField(
        max_length=255)
    details = models.TextField()
    rating = models.IntegerField(
        validators=[MaxValueValidator(10),
                    MinValueValidator(1)])
    platform = models.ForeignKey(
        Platforms,
        on_delete=models.CASCADE)
    budget = models.IntegerField(
        validators=[MinValueValidator(1)],
        blank=True,
        null=True)
    box_office = models.IntegerField(
        validators=[MinValueValidator(1)],
        blank=True,
        null=True)
    slug = models.SlugField(
        max_length=255)
    main_image = models.FileField(upload_to='media', default='No image')
    genre = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('page-view', args=[self.slug])


class ImagesSerial(models.Model):
    photos = models.ImageField()
    serial = models.ForeignKey(Serials, on_delete=models.CASCADE, related_name='serials', null=True, blank=True)


class Comment(MPTTModel):
    username = models.CharField(max_length=150)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    email = models.EmailField(blank=True)
    comment = models.TextField()
    rating = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    serial = models.ForeignKey(Serials, on_delete=models.CASCADE, related_name='comment')
    publish = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['publish']

    def __str__(self):
        return f'{self.username}||{self.email} - {self.comment}||{self.rating}'
