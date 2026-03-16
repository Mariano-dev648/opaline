from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente, Endereco


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('clientes:minha_conta')

    if request.method == 'POST':
        nome = request.POST.get('first_name')
        sobrenome = request.POST.get('last_name')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'cadastro.html')

        if Cliente.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return render(request, 'cadastro.html')

        if cpf and Cliente.objects.filter(cpf=cpf).exists():
            messages.error(request, 'Este CPF já está cadastrado.')
            return render(request, 'cadastro.html')

        cliente = Cliente.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=nome,
            last_name=sobrenome,
            cpf=cpf,
            telefone=telefone,
        )
        login(request, cliente)
        messages.success(request, f'Bem-vinda, {nome}! Sua conta foi criada com sucesso. ✨')
        return redirect('clientes:minha_conta')

    return render(request, 'cadastro.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('clientes:minha_conta')

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        cliente = authenticate(request, username=email, password=senha)

        if cliente:
            login(request, cliente)
            next_url = request.GET.get('next', 'clientes:minha_conta')
            return redirect(next_url)
        else:
            messages.error(request, 'E-mail ou senha incorretos.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('produtos:home')


@login_required(login_url='/clientes/login/')
def minha_conta(request):
    pedidos = request.user.pedidos.order_by('-criado_em')[:5]
    enderecos = request.user.enderecos.all()
    return render(request, 'minha_conta.html', {
        'pedidos': pedidos,
        'enderecos': enderecos,
    })


@login_required(login_url='/clientes/login/')
def adicionar_endereco(request):
    if request.method == 'POST':
        Endereco.objects.create(
            cliente=request.user,
            nome_destinatario=request.POST.get('nome_destinatario'),
            cep=request.POST.get('cep'),
            logradouro=request.POST.get('logradouro'),
            numero=request.POST.get('numero'),
            complemento=request.POST.get('complemento', ''),
            bairro=request.POST.get('bairro'),
            cidade=request.POST.get('cidade'),
            estado=request.POST.get('estado'),
        )
        messages.success(request, 'Endereço adicionado com sucesso!')
        return redirect('clientes:minha_conta')
    return render(request, 'adicionar_endereco.html')