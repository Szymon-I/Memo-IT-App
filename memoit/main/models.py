from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import uuid
from .choices import *
from .other import upload_path_handler


# base note model
class Note(models.Model):
    type = models.IntegerField(default=1, editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, default="Default title")
    published = models.DateTimeField('date published', default=datetime.now())
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.CharField(max_length=3000, blank=True)
    theme = models.IntegerField(default=1, choices=THEMES)

    # override name in Admin page
    class Meta:
        verbose_name_plural = "Notes"

    def __str__(self):
        return self.title


# model for list note
class NoteList(models.Model):
    type = models.IntegerField(default=2, editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, default="Default title")
    published = models.DateTimeField('date published', default=datetime.now())
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.TextField(blank=True)  # json parser to list
    theme = models.IntegerField(default=1, choices=THEMES)

    # override name in Admin page
    class Meta:
        verbose_name_plural = "Notes (list)"

    def __str__(self):
        return self.title


# model for note with picture
class NotePicture(models.Model):
    type = models.IntegerField(default=3, editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, default="Default title")
    published = models.DateTimeField('date published', default=datetime.now())
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.CharField(max_length=3000, blank=True)

    # picture is stored in user folder as raw, in model there is information to hashed path of picture
    picture = models.ImageField(upload_to=upload_path_handler, default='main/media/pics_uploaded/none.png', blank=True)

    # override name in Admin page
    class Meta:
        verbose_name_plural = "Notes (picture)"

    def __str__(self):
        return self.title
