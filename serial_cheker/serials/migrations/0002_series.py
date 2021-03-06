# Generated by Django 4.0.4 on 2022-05-18 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('title', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('serial', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='episode', to='serials.serials')),
            ],
        ),
    ]
