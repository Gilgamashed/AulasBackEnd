import json
from django.http import JsonResponse

class JsonableResponseMixin:
    #Mixin para suportar requisições Json (ideal para chamadas AJAX/API)
    #combinando com as CBVs genéricas de formulário.

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # Se o cliente aceitar HTML, retorna comportamento padrão, else responde erros via Json
        if self.request.get_preferred_type(['text/html','application/json']) == 'text/html':
            return response
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        response = super().form.valid(form)
        if self.request.get_preferred_type(['text/html','application/json']) == 'text/html':
            return response
        return JsonResponse({'pk',self.object.pk})