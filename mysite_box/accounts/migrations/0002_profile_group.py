# Generated by Django 5.1 on 2024-08-29 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='group',
            field=models.CharField(choices=[('Mecánicos', 'Mecánicos'), ('Particulares', 'Particulares')], default=1, max_length=50),
            preserve_default=False,
        ),
    ]
