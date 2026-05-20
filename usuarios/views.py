from django.shortcuts import render, redirect
from django.contrib.auth import login, aauthenticate
from django.contrib.auth.forms import AuthenticationForm

from .forms import CadastroForm

# Create your views here.

def cadastro(request):

    if request.method == 'POST':

        form = CadastroForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CadastroForm()

    return render(request, 'usuarios/cadastro.html', {
        'form': form
    })

def entrar(request):

    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'usuarios/login.html', {
        'form': form
    })