from django.contrib import admin
from .models import Question

admin.site.register(Question) #Tornar a aplicação de enquetes editável no site de administração
