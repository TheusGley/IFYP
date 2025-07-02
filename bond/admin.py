from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Anuncio)
admin.site.register(Customuser)
admin.site.register(Carrinho)
admin.site.register(Produto_Carrinho)
admin.site.register(Avaliacao)


