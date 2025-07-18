from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login,logout
from .models import *
from .forms import *
from django.contrib import messages

def homeView(request):
    
    celulares_destaque = Anuncio.objects.filter(visualizacao__gte=100)
    celulares_visualizados = Anuncio.objects.filter(visualizacao__gte=100)
    celular_mais_visualizado = celulares_visualizados.order_by('-visualizacao').first()
    imagem = ImagemAnuncio.objects.filter(anuncio=celular_mais_visualizado)
    
    context= {
        'imagem': imagem.first(),
        'celular_mais_visualizado': celular_mais_visualizado,
        'celulares_destaque':celulares_destaque
        
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
        anuncios = Anuncio.objects.all()
        error_message=None
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


def cadastroView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone') # Campo de telefone adicionado
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # --- Validações ---
        if not all([username, email, phone, password, confirm_password]):
            messages.error(request, "Por favor, preencha todos os campos.")
            return render(request, 'cadastro.html', {'error_message': "Por favor, preencha todos os campos."})

        if password != confirm_password:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'cadastro.html', {'error_message': "As senhas não coincidem."})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já existe. Escolha outro.")
            return render(request, 'cadastro.html', {'error_message': "Nome de usuário já existe. Escolha outro."})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Este email já está cadastrado.")
            return render(request, 'cadastro.html', {'error_message': "Este email já está cadastrado."})

        # Adicione validações de senha mais complexas aqui se necessário (ex: comprimento mínimo, caracteres especiais)
        if len(password) < 6: # Exemplo de validação de comprimento mínimo
            messages.error(request, "A senha deve ter no mínimo 6 caracteres.")
            return render(request, 'cadastro.html', {'error_message': "A senha deve ter no mínimo 6 caracteres."})
            
        # Você pode adicionar uma validação básica para o formato do telefone, se quiser.
        # Ex: import re; if not re.match(r'^\(\d{2}\)\s\d{4,5}-\d{4}$', phone): ...

        try:
            # --- Criação do Usuário ---
            user = User.objects.create_user(username=username, email=email, password=password)
            # Se você tiver um CustomUser model e/ou campos extras como 'phone',
            # você precisará salvá-los após a criação do usuário base.
            # Ex: user.phone = phone
            #     user.save()
            
            messages.success(request, "Sua conta foi criada com sucesso! Faça login para continuar.")
            return redirect('login') # Redireciona para a página de login
            
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao criar a conta: {e}")
            return render(request, 'cadastro.html', {'error_message': f"Ocorreu um erro ao criar a conta: {e}"})

    return render(request, 'cadastro.html')
    

def logoutView(request):
    logout(request)
    
    return redirect('home', )




def painelView(request):
    anuncios = Anuncio.objects.filter(usuario=request.user)
    

    
    context = {
        'anuncios': anuncios,
    }
    
    return render(request, 'painel.html',context )


def anuncioView(request):

    if request.method == 'POST':
        usuario = request.user
        nome = request.POST.get('nome')
        ram = request.POST.get('ram')
        camera = request.POST.get('camera')
        armazenamento = request.POST.get('armazenamento')
        bateria = request.POST.get('bateria')
        bv_desc = request.POST.get('bv_desc')
        descricao = request.POST.get('descricao')
        imagens = request.FILES.getlist('imagens') 
        marca = request.POST.get('marca')
        condicao = request.POST.get('condicao')
        valor = request.POST.get('valor')

        # Criando o anúncio corretamente
        anuncio = Anuncio.objects.create(
            usuario=usuario,
            nome=nome,
            bv_desc=bv_desc,
            descricao=descricao,
            armazenamento=armazenamento,
            meomoria=ram,
            camera=camera,
            bateria=bateria,
            marca=marca,
            condicao=condicao,
            valor=valor
        )

    # Criando todas as imagens relacionadas ao anúncio
        for imagem in imagens:
            ImagemAnuncio.objects.create(
                anuncio=anuncio,
                imagem=imagem
            )

        return redirect('painel')

    context = {

    }
    return render (request, 'publicar-anuncio.html', context)




def editarView(request, id):
    anuncio = get_object_or_404(Anuncio, id=id)
    imagens_anteriores = ImagemAnuncio.objects.filter(anuncio=anuncio)

    if request.method == 'POST':
        form = AnuncioForm(request.POST, instance=anuncio)
        
        imagens = [
            request.FILES.get('imagem1'),
            request.FILES.get('imagem2'),
            request.FILES.get('imagem3'),
            request.FILES.get('imagem4'),
        ]
        print(form.is_valid())
        if form.is_valid():
            anuncio = form.save(commit=False)
            anuncio.usuario = request.user
            anuncio.save()

            # Substitui imagens somente se novas foram enviadas
            if any(imagem for imagem in imagens if imagem):
                # Apaga imagens antigas
                for img in imagens_anteriores:
                    img.imagem.delete(save=False)
                    img.delete()
                
                # Salva novas imagens
                for imagem in imagens:
                    if imagem:
                        ImagemAnuncio.objects.create(anuncio=anuncio, imagem=imagem)

            return redirect('painel')
        elif  not form.is_valid():
            print(form.errors) 
    else:
        form = AnuncioForm(instance=anuncio)

    return render(request, 'editar-anuncio.html', {
        'form': form,
        'anuncio': anuncio,
        'id': id,
    })


def celUnicoView(request, id):
    
    try: 
        celular_unico = Anuncio.objects.get(id=id)
        imagens  = ImagemAnuncio.objects.filter(anuncio=celular_unico)
        celular_unico.visualizacao += 1
        celular_unico.save()
        error_message = ""
        
    except Anuncio.DoesNotExist:
        error_message = 'Celular não encontrado.'
        celular_unico= None
        

    
    context = {
        'error_message': error_message,
        'celular_unico': celular_unico,
        'imagens':imagens,
    }
    return render(request, 'celUnico.html', context )

def celularesView(request):
    anuncios = Anuncio.objects.prefetch_related('imagens').all()
    
    context = {
        'celulares': anuncios,
    }
    return render(request, 'celulares.html',context )


def suporteView(request):
    
    perguntas = PerguntasFrequentes.objects.all()
    
    context = {
        "perguntas": perguntas,
    }
    
    return render(request, 'suporte.html', context )


def servicosView(request):
    
    return render(request, 'servicos.html', )


