
from django.contrib import admin
from django.urls import path, include
from bond.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", homeView, name="home"),
    path("pesquisar", pesquisaView, name="pesquisar"),
    path("filtros", filtrosView, name="filtros"),
    path("login", loginView, name="login"),
    path("logout", logoutView, name="logout"),
    path("painel-controle", painelView, name="painel"),
    path("cel/<id>", celUnicoView, name="cel"),
    path("celulares", celularesView, name="celulares"),
    path("suporte", suporteView, name="suporte"),
    path("servicos", servicosView, name="servicos"),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
    




