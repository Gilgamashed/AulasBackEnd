import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.views import View
import sys
import socket

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from app.forms import BookForm
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
        return render(request, "app/person_list.html", {"people":people})

def person_list_json(request):                #FBV
    people = Person.objects.all().values()
    return JsonResponse(list(people), safe=False)

def person_create(request):                #FBV
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        if name and age:
            Person.objects.create(
                name=name,
                age=age,
            )
            return redirect("people")  # apos o cadastro, volta para a listagem
    return render(request, "app/person_form.html")

def person_update(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    if request.method == "POST":
        person.name = request.POST.get("name")
        person.age = request.POST.get("age")
        person.save()

        return redirect("people")
    return render(request, "app/person_form.html",{"person":person})

def person_delete(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    if request.method == "POST":
        person.delete()
        return redirect("people")
    return render (request,"app/person_confirm.html",{"person":person})

#----- x ----- x ----- x ----- x ----- x ----- x ----- x ----- x ----- x ----- x ----- x ----- x -----

class BookListJsonView(View):               #CBV
    def get(self, request):
        books = Book.objects.all().values()
        return JsonResponse(list(books), safe=False)

class BooklistView(ListView):
    model = Book
    template_name = "app/book_list.html"
    context_object_name = "books"

class BookCreateView(CreateView):
    model = Book
    form_class  = BookForm
    template_name = "app/book_form.html"
    success_url = reverse_lazy('book_list') #redireciona após cadastro

class BookUpdateView(UpdateView):       #pesquisar uma forma mais clean
    model = Book
    form_class = BookForm
    template_name = "app/book_form.html"
    pk_url_kwarg = "book_id"
    success_url = reverse_lazy('book_list')

"""    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        body = json.loads(request.body)

        self.object.title = body.get('title', self.object.title)
        self.object.author = body.get('author', self.object.author)
        self.object.pages = body.get('pages', self.object.pages)
        self.object.published_date = parse_date(body.get('published_date', self.object.title)) or self.object.published_date
        self.object.save()

        return JsonResponse({'message':'Book updated successfully', 'id':self.object.id})"""

class BookGetView(DetailView):
    model = Book
    template_name = "app/book_detail.html"
    context_object_name = "book"
    pk_url_kwarg = "book_id"

class BookDeleteView(DeleteView):
    model = Book
    template_name = "app/book_confirm.html"
    pk_url_kwarg = "book_id"
    success_url = reverse_lazy('book_list')


"""Legacy FBVs --

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

def book_update(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.pages = request.POST.get("pages")
        book.published_date = parse_date(request.POST.get("published_date"))
        book.save()

        return redirect("books")
    return render(request, "app/book_form.html",{"book":book})

def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("books")
    return render (request,"app/book_confirm.html",{"book":book})

"""

# esse arquivo gerencia as funções do app
# python manage.py runserver  <-- para rodar o server
# pesquisar programação orientadas a teste.
