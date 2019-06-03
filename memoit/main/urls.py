"""memoit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.start, name='start'),
    path('home', views.homepage, name='homepage'),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("account/", views.account, name="account"),
    path("help/", views.help, name="help"),
    path('create/<note_type>', views.create_note, name='createNote'),
    path('delete/<redirect_type>/<note_type>/<note_id>', views.delete_note, name='deleteNote'),
    path('update/<redirect_type>/<note_type>/<note_id>', views.update_note, name='updateNote'),
    path('delete_account/', views.delete_account, name='deleteAccount'),
    path('delete_all/', views.delete_all, name='deleteAll'),
]
