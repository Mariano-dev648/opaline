from django.shortcuts import render

def placeholder(request):
    return render(request, 'home.html')

pagar_pix = webhook_mp = sucesso = placeholder