# Generated by Django 4.0.4 on 2022-05-17 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serials', '0008_serials_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serials',
            name='main_image',
            field=models.FileField(default='No image', upload_to=''),
        ),
    ]