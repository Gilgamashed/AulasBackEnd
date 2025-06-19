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
from app.views import BaseHelloView, ServerInfoView, WelcomeView, PeopleView, person_create, person_update, person_delete, BooklistView, BookCreateView, BookGetView, \
    BookUpdateView, BookDeleteView, BookListJsonView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello", BaseHelloView.as_view(), name='hello'),
    path("server-info", ServerInfoView.as_view(), name="server_info" ),
    path("welcome/", WelcomeView.as_view(), name="welcome"),

    path("people/", PeopleView.as_view(), name="people"),
    path("people-add/", person_create, name="people_add"),
    path("people-edit/<int:person_id>", person_update, name='people-edit'),
    path("person-delete/<int:person_id>", person_delete, name='person-delete'),

    path("book/json/", BookListJsonView.as_view(), name="book_list_json"),
    path("book/list/", BooklistView.as_view(), name='book_list'),
    path("book", BookCreateView.as_view(), name='book_add'),
    path("book/<int:book_id>", BookGetView.as_view(), name='book_detail'),
    path("book/delete/<int:book_id>", BookDeleteView.as_view(), name='book_delete'),
    path("book/edit/<int:book_id>", BookUpdateView.as_view(), name="book_update"),

]

