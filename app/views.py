from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def pagina_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Credenciais inválidas. Tente novamente."
            return render(request, 'auth/login.html', {'error_message': error_message})
    return render(request, 'auth/login.html')

