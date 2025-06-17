"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path

from app import views
from app.views import BaseHelloView, ServerInfoView, WelcomeView, PeopleView, book_list, book_list_json, book_create

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello", BaseHelloView.as_view(), name='hello'),
    path("server-info", ServerInfoView.as_view(), name="server-info" ),
    path("welcome/", WelcomeView.as_view(), name="welcome"),
    path("people/", PeopleView.as_view(), name="people"),
    path("books-json/", book_list_json),
    path("books/", book_list, name='books'),
    path("books-add/", book_create),
]

