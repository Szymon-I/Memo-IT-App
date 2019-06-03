from django.contrib import admin
from .models import *

# show notes in admin page
admin.site.register(Note)
admin.site.register(NoteList)
admin.site.register(NotePicture)



