# Generated by Django 4.2.2 on 2023-07-31 07:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_delete_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('start_time', models.DateTimeField(verbose_name='start_time')),
                ('end_time', models.DateTimeField(verbose_name='end_time')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is_deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted_at')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='create_at')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='update_at')),
                ('uuid', models.ForeignKey(db_column='user_uuid', on_delete=django.db.models.deletion.CASCADE, related_name='schedules_uuid', to=settings.AUTH_USER_MODEL, to_field='uuid')),
            ],
            options={
                'verbose_name': 'Schedule',
                'verbose_name_plural': 'Schedules',
                'db_table': 'schedule',
            },
        ),
    ]