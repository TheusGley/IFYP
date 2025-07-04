from django.shortcuts import render, redirect
from django.db import IntegrityError

from django.contrib.auth import authenticate, login,logout
from .models import *

def homeView(request):
    
    celulares_destaque = Anuncio.objects.filter(visualizacao__gte=100)
    celular_mais_visualizado = Anuncio.objects.order_by('-visualizacao').first()
    context= {
        'celulares_destaque': celulares_destaque,
        'celular_mais_visualizado': celular_mais_visualizado,
    }
    return render(request, 'home.html', context)


def pesquisaView(request ):
    query = request.POST.get('pesquisar')
    print(f"Consulta: {query}")
    
    if query:
        anuncios = Anuncio.objects.filter(nome__icontains=query)
        error_message=None        
    else:
        error_message = "Nenhum termo de pesquisa fornecido."
        anuncios = Anuncio.objects.none()  

    print(f"Consulta: {query}")
    context = {
        'celulares': anuncios,
        'query': query,
        'error_message':error_message
    }
    
    return render(request, 'celulares.html', context)

def filtrosView(request ):
    marca= request.POST.get('marca')
    preco= request.POST.get('preco')
    condicao= request.POST.get('condicao')
    
    if marca and preco and condicao:
        anuncios = Anuncio.objects.filter(marca__icontains=marca, valor__lt=preco, condicao__contains=condicao)
        print(str(anuncios) + "1")
        error_message=None
    elif marca and preco:
        anuncios = Anuncio.objects.filter(marca__icontains=marca, valor__lte=preco)
        print(str(anuncios) + "2")
        
        error_message=None
    elif marca and condicao:
        anuncios = Anuncio.objects.filter(marca__icontains=marca, condicao__contains=condicao)
        print(str(anuncios) + "3")
        
        error_message=None  
    elif preco and condicao:
        anuncios = Anuncio.objects.filter(valor__icontains=preco, condicao__contains=condicao)
        print(str(anuncios) + "4")
        
        error_message=None  
    elif marca:
        anuncios = Anuncio.objects.filter(marca__icontains=marca)
        print(str(anuncios) + "5")
        
        error_message=None  
    elif preco:
        anuncios = Anuncio.objects.filter(valor__lte=preco)
        print(str(anuncios) + "6")
        
        error_message=None
    elif condicao:
        anuncios = Anuncio.objects.filter(condicao__contains=condicao)
        print(str(anuncios) + "7")
        
        error_message=None
    else:
        redirect('celulares')
    
    context={
        'celulares': anuncios,
        'error_message': error_message,
    }
    return render(request, 'celulares.html', context)

def loginView(request):
    
    if request.user.is_authenticated:        
            return redirect('painel')           
            

    if request.method == 'POST':
        username_or_email = request.POST.get('email')
        password = request.POST.get('password')

        # Primeira tentativa de autenticação direta
        user = authenticate(username=username_or_email, password=password)

        if user is None:  
            try:
                user_model = User.objects.get(email=username_or_email)
                user = authenticate(username=user_model.username, password=password)
                print(user)     
                if user:
                    pass
                else:
                    return render(request, 'login.html', {'error_messagem': "Credenciais inválidas"})

                # try:
                #     user_last = Confiabilidade.objects.get(user=user_model)
                #     user_last.ultimo_acesso = user_model.last_login
                #     user_last.save()
                # except Confiabilidade.DoesNotExist:
                #     pass

            except User.DoesNotExist:
                return render(request, 'login.html', {'error_messagem': "Usuário não encontrado"})
            except User.MultipleObjectsReturned:
                return render(request, 'login.html', {'error_messagem': "Vários usuários encontrados com este email"})
            except IntegrityError as e:
                return render(request, 'login.html', {'error_messagem': "Erro de integridade: " + str(e)})

        
        login(request, user)
        return redirect('painel')

    
    return render(request, 'login.html', )

def logoutView(request):
    logout(request)
    
    return redirect('home', )




def painelView(request):
    anuncios = Anuncio.objects.filter(usuario=request.user)
    
    
    context = {
        'anuncios': anuncios,
    }
    
    return render(request, 'painel.html',context )




def celUnicoView(request, id):
    
    try: 
        celular_unico = Anuncio.objects.get(id=id)
        celular_unico.visualizacao += 1
        celular_unico.save()
        error_message = ""
        
        
    except Anuncio.DoesNotExist:
        error_message = 'Celular não encontrado.'
        celular_unico= None
        
    
    context = {
        'error_message': error_message,
        'celular_unico': celular_unico,
    }
    return render(request, 'celUnico.html', context )

def celularesView(request):
    celulares = Anuncio.objects.all()    
    
    context = {
        'celulares': celulares,
    }
    return render(request, 'celulares.html',context )



def suporteView(request):
    
    return render(request, 'suporte.html', )


def servicosView(request):
    
    return render(request, 'servicos.html', )


