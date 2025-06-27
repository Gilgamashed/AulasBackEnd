from django import forms
from .models import Book, Chore


class BookForm(forms.ModelForm):
    class Meta:         #classe interna para configurar o formulário
        model = Book
        fields = ['title', 'author','pages','published_date'] #quais campos do model serão expostos no formulário
        widgets = {                                     #permite customizar os tipos de campo
            'published_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),

        }
        help_texts = {'pages':'Informe um número inteiro maior que 10.','published_date':'Use o formato YYYY-MM-DD.'}
        labels = {
            'title' : 'Título',
            'author' : 'Autor',
            'pages' : 'Páginas',
            'published_date' : 'Data de Publicação'
        }

    def __init__(self, *args, **kwargs):               #validação
        super().__init__(*args, **kwargs)
        self.fields['published_date'].input_formats = ['%Y-%m-%d']

class ChoreForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ['title', 'description','due_date','done']
        widgets = {
            'description': forms.TextInput(attrs={"required": False}), #????
            'due_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'done':forms.CheckboxInput(),
        }
        help_texts = {'due_date':'Use o formato YYYY-MM-DD.'}
        labels = {
            'title' : 'Título',
            'description' : 'Descrição',
            'due_date' : 'Data de Entrega',
            'done' : 'Concluído?'
        }
    def __init__(self, *args, **kwargs):               #validação
        super().__init__(*args, **kwargs)
        self.fields['due_date'].input_formats = ['%Y-%m-%d']
        self.fields['description'].required = False


class ContactForm(forms.Form):
    name = forms.CharField(label="Seu nome", max_length=100)
    email = forms.EmailField(label="E-mail")
    message = forms.CharField(label="Mensagem", widget=forms.Textarea)