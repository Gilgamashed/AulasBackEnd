from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:         #classe interna para configurar o formulário
        model = Book
        fields = ['title', 'author','pages','published_date'] #quais campos do model serão expostos no formulário
        labels = {
            'title' : 'Título',
            'author' : 'Autor',
            'pages' : 'Páginas',
            'published_date' : 'Data de Publicação'
        }
        widgets = {                                     #permite customizar os tipos de campo
            'published_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }