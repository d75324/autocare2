# Generated by Django 5.1 on 2024-10-05 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_profile_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='/mysite_box/media/default.jpg', upload_to='users/', verbose_name='Imagen'),
        ),
    ]
