from django.shortcuts import render

def placeholder(request):
    return render(request, 'home.html')

# views serão implementadas na Fase 4
login_view = cadastro = logout_view = minha_conta = placeholder