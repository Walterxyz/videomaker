from ..models import Servidor
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):    
    servidores = Servidor.objects.all().order_by('status')
    context = {'servidores': servidores}
    return render(request, 'home.html', context)

