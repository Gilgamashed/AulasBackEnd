import json
import os.path
import smtplib
import ssl

import certifi
from django.core.files.storage import default_storage
from django.core.mail import send_mail, get_connection, EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.views import View
import os
import sys
import socket

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from app.forms import BookForm, ChoreForm, ContactForm
from app.mixins import JsonableResponseMixin
from app.models import Person, Book, Chore
from config import settings


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

class BookUpdateView(JsonableResponseMixin,UpdateView):       #pesquisar uma forma mais clean
    model = Book
    form_class = BookForm
    template_name = "app/book_form.html"
    pk_url_kwarg = "book_id"
    success_url = reverse_lazy('book_list')

    def put(self, request, *args, **kwargs):
        self.object= self.get_object()
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Json Invalid'}, status=400)
        #Monta os kwargs com os dados e instancia
        kwargs = self.get_form_kwargs()
        kwargs['data'] = body
        kwargs['instance'] = self.object

        form = self.get_form(**kwargs)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

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

#---------------------------------------------------------------------------------

class ChoreListView(ListView):
    model = Chore
    template_name = "app/tarefa_list.html"
    context_object_name = "tarefas"

class ChoreCreateView(CreateView):
    model = Chore
    form_class  = ChoreForm
    template_name = "app/tarefa_form.html"
    success_url = reverse_lazy('tarefa_list')

class ChoreGetView(DetailView):
    model = Chore
    template_name = "app/tarefa_detail.html"
    context_object_name = "tarefa"
    pk_url_kwarg = "tarefa_id"

class ChoreDeleteView(DeleteView):
    model = Chore
    template_name = "app/tarefa_confirm.html"
    pk_url_kwarg = "tarefa_id"
    success_url = reverse_lazy('tarefa_list')

class ChoreUpdateView(JsonableResponseMixin,UpdateView):       #pesquisar uma forma mais clean
    model = Chore
    form_class = ChoreForm
    template_name = "app/tarefa_form.html"
    pk_url_kwarg = "tarefa_id"
    success_url = reverse_lazy('tarefa_list')

    def put(self, request, *args, **kwargs):
        self.object= self.get_object()
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Json Invalid'}, status=400)
        #Monta os kwargs com os dados e instancia
        kwargs = self.get_form_kwargs()
        kwargs['data'] = body
        kwargs['instance'] = self.object

        form = self.get_form(**kwargs)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


#-------------------------------------------------------------------------------------------------------

def contact_view(request):
    form = ContactForm(request.POST or None, request.FILES or None)

    if form.is_valid():                         #valida se os campos foram preenchidos
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        file = form.cleaned_data.get('attachment')

        email_message = EmailMessage(
            subject=f'Contato de {name}',
            body=message,
            from_email=email,
            to=['projeto.minstrel@gmail.com'],
            reply_to=[email],
        )

        if file:
            if file.size > 5 * 1024 * 1024:
                raise ValueError("O arquivo é muito grande. O tamanho máximo é 5MB.")
            file_name = default_storage.save(f'uploads/{file.name}', file)
            file.seek(0)        #o .save acima leva o "ponteiro" pro fim do arquivo e envia só o fim dele.
                                #esse file.seek(0) leva o "ponteiro" pro começo do arquivo novamente.

            content_type = file.content_type
            email_message.attach(file.name, file.read(), content_type)

        email_message.send()

        context = {"success": True, 'name':name}
        return render(request,'app/contact.html',context)

    return render(request,'app/contact.html', {'form':form})    #Se for GET ele cai aqui


# esse arquivo gerencia as funções do app
# python manage.py runserver  <-- para rodar o server
# pesquisar programação orientadas a teste.
