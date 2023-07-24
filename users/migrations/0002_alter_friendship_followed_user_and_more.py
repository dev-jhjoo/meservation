# Generated by Django 4.2.2 on 2023-07-24 00:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='followed_user',
            field=models.ForeignKey(db_column='followed_user_uuid', on_delete=django.db.models.deletion.CASCADE, related_name='followed_user_uuid', to=settings.AUTH_USER_MODEL, to_field='uuid'),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='following_user',
            field=models.ForeignKey(db_column='following_user_uuid', on_delete=django.db.models.deletion.CASCADE, related_name='following_user_uuid', to=settings.AUTH_USER_MODEL, to_field='uuid'),
        ),
    ]