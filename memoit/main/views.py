from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import *
from .models import *
import os
from memoit.settings import BASE_DIR, MEDIA_ROOT
from django.utils.html import strip_tags
from datetime import datetime
from django.utils.timezone import make_aware
import shutil
from main.emails.emails import welcome_email


# start page view (logo), this shows when user is not logged in
def start(request):
    if request.user.is_authenticated:
        return redirect('main:homepage')
    return render(request, 'main/start.html')


# main desktop view of app, it shows all notes of logged user sorted by modified/created date
def homepage(request):
    # if user is authenticated - collect all of notes from database and sort them by date
    if request.user.is_authenticated:
        notes = [x for x in Note.objects.all() if x.author.username == request.user.username]
        notes_list = [x for x in NoteList.objects.all() if x.author.username == request.user.username]
        list_items = {}
        for item in notes_list:
            list_items[item.id] = item.content.split('|')
        notes_picture = [x for x in NotePicture.objects.all() if x.author.username == request.user.username]
        notes_all = [*notes, *notes_list, *notes_picture]
        notes_all.sort(key=lambda x: x.published, reverse=True)
        # if user don't have any notes, show a message
        if len(notes_all) == 0:
            messages.info(request, 'You don\'t have any notes, create one!')
        # render view by passing dict with all notes to template
        return render(request, 'main/home.html', context={'NotesAll': notes_all,
                                                          'list_items': list_items})

    # if user force to go to desktop view but is not logged in it redirects to start page and show info message
    else:
        messages.info(request, 'You need to log in to access your memos')
        return redirect('main:login')


# register page, checks if username or email exists already in a database
def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, f'Email {email} is taken')
                return redirect('main:register')
            # if there is unique user, it creates an entry in database and create unique folder to store images
            user = form.save()
            path_temp = os.path.join(os.path.join('main', 'media', 'pics_uploaded'), '')
            path = os.path.join(BASE_DIR, '') + path_temp + username
            if not os.path.isdir(path):
                os.mkdir(path)
            # after success in registering - log in user and redirect to homepage
            messages.success(request, f'New Account created: {username}')
            messages.info(request, f'You are now logged in as: {username}')
            welcome_email(user)
            login(request, user)
            return redirect('main:homepage')
        # if there is invalid form - display errors and refresh page and form
        else:
            for field, errors in form.errors.items():
                stripped_errors = strip_tags(errors)
                messages.error(request, f"{stripped_errors}")
            return redirect('main:register')
    # if request is GET, load the form and render register page
    else:
        form = NewUserForm
        return render(request, 'main/register.html',
                      context={'form': form})


# login view, user can log in with email or username
def login_request(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.clean_username()
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is None:
                user = User.objects.all().filter(email=username)
            if user is not None:
                # if data is valid, log in user and check if folder for media exists
                login(request, user)
                messages.info(request, f'You are now logged in as: {username}')
                path_temp = os.path.join(os.path.join('main', 'media', 'pics_uploaded'), '')
                path = os.path.join(BASE_DIR, '') + path_temp + username
                if not os.path.isdir(path):
                    os.mkdir(path)
                if user.is_staff:
                    messages.info(request, f'You have superuser privileges')
                return redirect('main:homepage')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    # if request is GET, load the form and render log in page
    form = EmailAuthenticationForm()
    form.fields['username'].label = "Username or Email"
    return render(request,
                  'main/login.html',
                  {'form': form})


# logout view - redirects to start page after logout
def logout_request(request):
    logout(request)
    return redirect('main:start')


# account view - display all of user information in table form for easy management
def account(request):
    if request.user.is_authenticated:
        user = request.user
        notes = [x for x in Note.objects.all() if x.author.username == request.user.username]
        notes_list = [x for x in NoteList.objects.all() if x.author.username == request.user.username]
        notes_picture = [x for x in NotePicture.objects.all() if x.author.username == request.user.username]
        notes_all = [*notes, *notes_list, *notes_picture]
        notes_all.sort(key=lambda x: x.published, reverse=True)
        lengths = [len(notes), len(notes_list), len(notes_picture), len(notes_all)]
        return render(request, 'main/account.html', {'user': user,
                                                     'lengths': lengths,
                                                     'NotesAll': notes_all})

    # if user force to go to desktop view but is not logged in it redirects to start page
    else:
        return redirect('main:homepage')


# help page with information about app
def help(request):
    return render(request, 'main/help.html')


# create note page, view depends on note type
def create_note(request, note_type):
    # render page with form adequately to note type request
    if request.method == 'POST':
        if note_type == '1':
            form = NoteForm(request.POST)
        elif note_type == '2':
            form = NoteListForm(request.POST)
        elif note_type == '3':
            form = NotePictureForm(request.POST, request.FILES)
        if form.is_valid():
            if note_type != '3':
                theme_data = form.cleaned_data.get('theme')
            title_data = form.cleaned_data.get('title')
            content_data = form.cleaned_data.get('content')
            naive_datetime = datetime.now()
            time_data = make_aware(naive_datetime)
            if note_type == '1':
                obj = Note(title=title_data, content=content_data, theme=theme_data,
                           published=time_data, author=request.user)
            elif note_type == '2':
                obj = NoteList(title=title_data, content=content_data, theme=theme_data,
                               published=time_data, author=request.user)
            elif note_type == '3':
                picture_data = form.cleaned_data.get('picture')
                obj = NotePicture(title=title_data, content=content_data,
                                  published=time_data, picture=picture_data, author=request.user, )

            # if form is valid - create new note with given information and redirect to homepage
            obj.save()
            messages.info(request, f'You have created new {title_data} note')
        return redirect('main:homepage')

    # if request is GET, load the form and render create page
    if note_type == '1':
        form = NoteForm()
    if note_type == '2':
        form = NoteListForm()
    elif note_type == '3':
        form = NotePictureForm()
    return render(request,
                  'main/create.html',
                  {'form': form, 'note_type': note_type})


# update note page - similar to create page,
# but it loads information from database and pass it info form before rendering
def update_note(request, note_id, note_type, redirect_type):
    if request.method == 'POST':
        if note_type == '1':
            form = NoteForm(request.POST)
            obj = Note.objects.get(id=note_id)
        elif note_type == '2':
            form = NoteListForm(request.POST)
            obj = NoteList.objects.get(id=note_id)
        elif note_type == '3':
            form = NotePictureFormUpdate(request.POST, request.FILES or None)
            obj = NotePicture.objects.get(id=note_id)
        if form.is_valid():
            title_data = form.cleaned_data.get('title')
            content_data = form.cleaned_data.get('content')
            naive_datetime = datetime.now()
            time_data = make_aware(naive_datetime)
            obj.title = title_data
            obj.content = content_data
            obj.published = time_data
            if note_type != '3':
                theme_data = form.cleaned_data.get('theme')
                obj.theme = theme_data
            if note_type == '3':
                if form.cleaned_data.get('picture') is not None:
                    picture_data = form.cleaned_data.get('picture')
                    obj.picture = picture_data
            obj.save()
            messages.info(request, f'You have updated {title_data} note')
            if redirect_type == 'home':
                return redirect('main:homepage')
            if redirect_type == 'account':
                return redirect('main:account')

    if note_type == '1':
        note_given = Note.objects.get(id=note_id)
        theme_given = note_given.theme
        form = NoteForm(initial={
            'title': note_given.title,
            'content': note_given.content,
            'theme': note_given.theme,
        })
    elif note_type == '2':
        note_given = NoteList.objects.get(id=note_id)
        theme_given = note_given.theme
        form = NoteListForm(initial={
            'title': note_given.title,
            'content': note_given.content,
            'theme': note_given.theme,
        })
    elif note_type == '3':
        note_given = NotePicture.objects.get(id=note_id)
        form = NotePictureFormUpdate(initial={
            'title': note_given.title,
            'content': note_given.content,
            'picture': note_given.picture,
        })
        theme_given = 1
    return render(request,
                  'main/update.html',
                  {'form': form, 'note_type': note_type, 'theme': theme_given, })


# delete note view, redirects to page from which note was deleted
def delete_note(request, note_id, note_type, redirect_type):
    if note_type == '1':
        obj = Note.objects.get(id=note_id)
        messages.warning(request, f'Note {obj.title} deleted')
        obj.delete()
    elif note_type == '2':
        obj = NoteList.objects.get(id=note_id)
        messages.warning(request, f'Note List {obj.title} deleted')
        obj.delete()
    elif note_type == '3':
        obj = NotePicture.objects.get(id=note_id)
        os.remove(os.path.join(MEDIA_ROOT, str(obj.picture)))
        messages.warning(request, f'Note Picture {obj.title} deleted')
        obj.delete()
    if redirect_type == 'home':
        return redirect('main:homepage')
    if redirect_type == 'account':
        return redirect('main:account')


# delete account along with all stored media
def delete_account(request):
    if request.user.is_authenticated:
        username = request.user.username
        path_temp = os.path.join(os.path.join('main', 'media', 'pics_uploaded'), '')
        path = os.path.join(BASE_DIR, '') + path_temp + username
        if os.path.isdir(path):
            shutil.rmtree(path)
        request.user.delete()
        messages.warning(request, f"The user {username} is deleted")
    return redirect('main:start')


# delete all of user notes in one click
def delete_all(request):
    if request.user.is_authenticated:
        notes = [x for x in Note.objects.all() if x.author.username == request.user.username]
        notes_list = [x for x in NoteList.objects.all() if x.author.username == request.user.username]
        notes_picture = [x for x in NotePicture.objects.all() if x.author.username == request.user.username]
        notes_all = [*notes, *notes_list, *notes_picture]
        for note in notes_all:
            if note.type == 3:
                os.remove(os.path.join(MEDIA_ROOT, str(note.picture)))
            note.delete()
        messages.warning(request, "All notes deleted deleted")
    return redirect('main:homepage')
