from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from .forms import CadastroForm


def cadastro_view(request):

    if request.method == 'POST':

        form = CadastroForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    else:

        form = CadastroForm()

    return render(
        request,
        'usuarios/cadastro.html',
        {
            'form': form
        }
    )


def login_view(request):

    erro = None

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.tipo_usuario == 'leitor':

                return redirect(
                    'bibliotecas_leitor'
                )

            return redirect(
                'painel_bibliotecario'
            )

        else:

            erro = 'Usuário ou senha inválidos.'

    return render(
        request,
        'usuarios/login.html',
        {
            'erro': erro
        }
    )


def logout_view(request):

    logout(request)

    return redirect('index')