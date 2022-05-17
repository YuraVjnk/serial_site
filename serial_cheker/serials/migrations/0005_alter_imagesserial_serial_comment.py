# Generated by Django 4.0.4 on 2022-05-15 19:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serials', '0004_imagesserial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagesserial',
            name='serial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serials', to='serials.serials'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('comment', models.TextField()),
                ('rating', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('serial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='serials.serials')),
            ],
        ),
    ]
