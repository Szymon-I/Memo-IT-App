# Generated by Django 2.2.1 on 2019-06-03 09:43

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.other
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NotePicture',
            fields=[
                ('type', models.IntegerField(default=3, editable=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='Default title', max_length=100)),
                ('published', models.DateTimeField(default=datetime.datetime(2019, 6, 3, 11, 43, 8, 433396), verbose_name='date published')),
                ('content', models.CharField(blank=True, max_length=3000)),
                ('picture', models.ImageField(blank=True, default='main/media/pics_uploaded/none.png', upload_to=main.other.upload_path_handler)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Notes (picture)',
            },
        ),
        migrations.CreateModel(
            name='NoteList',
            fields=[
                ('type', models.IntegerField(default=2, editable=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='Default title', max_length=100)),
                ('published', models.DateTimeField(default=datetime.datetime(2019, 6, 3, 11, 43, 8, 433396), verbose_name='date published')),
                ('content', models.TextField(blank=True)),
                ('theme', models.IntegerField(choices=[(1, 'Dark'), (2, 'Cyan'), (3, 'Green'), (4, 'Amber'), (5, 'Purple'), (6, 'Red')], default=1)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Notes (list)',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('type', models.IntegerField(default=1, editable=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='Default title', max_length=100)),
                ('published', models.DateTimeField(default=datetime.datetime(2019, 6, 3, 11, 43, 8, 432395), verbose_name='date published')),
                ('content', models.CharField(blank=True, max_length=3000)),
                ('theme', models.IntegerField(choices=[(1, 'Dark'), (2, 'Cyan'), (3, 'Green'), (4, 'Amber'), (5, 'Purple'), (6, 'Red')], default=1)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Notes',
            },
        ),
    ]
