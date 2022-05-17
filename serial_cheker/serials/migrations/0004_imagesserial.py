# Generated by Django 4.0.4 on 2022-05-12 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serials', '0003_alter_serials_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagesSerial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photos', models.ImageField(upload_to='')),
                ('serial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serials.serials')),
            ],
        ),
    ]