from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.views import View
import sys
import socket

from django.views.generic import TemplateView

from app.models import Person, Book


#FBV? - CBV?
#Funcion Based View  -
#Class Based View  - aplicações mais robustas onde comportamentos mais simples de se reproduzir

#Versão FBV do código anterior
class BaseHelloView(View):
    message = "Hello, World from CBV!"
    def get(self, request):
        global message
        return JsonResponse({"message":f'{self.message}!'})

class ServerInfoView(View):
    def get(self, request):
        hostname = socket.gethostname()
        python_version = sys.version
        response = {
            "python_version": python_version ,
            "hostname": hostname
        }
        return JsonResponse(response)

class WelcomeView(TemplateView):
    template_name = "app/welcome.html"
    def get_context_data(self, **kwargs):       #esse metodo é uma sobreescrita
        context = super().get_context_data(**kwargs)
        context["name"] = self.request.GET.get("name", "Visitante")
        return context  #retorna um http response

class PeopleView(View):
    def get(self, request):
        people = Person.objects.all()
        data = [{"name": p.name, "age": p.age} for p in people]
        return JsonResponse({"people":data})

def book_list_json(request):                #FBV
    books = Book.objects.all().values()
    return JsonResponse(list(books), safe=False)    #diz pro Json q é seguro retornar uma lista

def book_list(request):                #FBV
    books = Book.objects.all()
    return render(request, "app/book_list.html", {"books":books})

def book_create(request):                #FBV
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        pages = request.POST.get("pages")
        published_date = parse_date(request.POST.get("published_date"))

        #Validação de dados
        if title and author and pages and published_date:
            Book.objects.create(
                title=title,
                author=author,
                pages=pages,
                published_date=published_date
            )
            return redirect("books")   #apos o cadastro, volta para a listagem
    return render(request,"app/book_form.html")

# Create your views here.

# esse arquivo gerencia as funções do app
# python manage.py runserver  <-- para rodar o server
# pesquisar programação orientadas a teste.
