# Generated by Django 4.1 on 2023-03-30 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_club_create_at_alter_club_club_genre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='favourites',
            field=models.TextField(null=True),
        ),
    ]
