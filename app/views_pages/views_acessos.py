from django.http import HttpResponse, JsonResponse
from ..tasks import try_connection
from ..models import AcessoServidores
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core import serializers
import json

# Listar Acessos
@login_required
def acessos(request):
    servidores = AcessoServidores.objects.all()
    servidores_data = serializers.serialize('json', servidores)
    return render(request, 'gerenciar_acessos.html', {'servidores': servidores_data})

@login_required
def atualizar_acessos(request):
    servidores = AcessoServidores.objects.all()
    servidores_partial = render_to_string('partials/acessos_partial.html', {'servidores': servidores})
    return HttpResponse(servidores_partial)

@login_required
def novo_servidor(request):
    if request.method == 'POST':
        dados = request.POST.get('dados')
        dados = json.loads(dados)
        servidor = AcessoServidores(**dados)
        if try_connection(servidor):
            servidor.save()
            return JsonResponse({'status': True})
    return JsonResponse({'status': False})


@login_required
def ativa_slot(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        servidor = AcessoServidores.objects.get(id=id)
        if servidor.inslots:
            servidor.inslots = False
        else:
            servidor.inslots = True
        print(servidor.inslots)
        servidor.save()
    return JsonResponse({'status': True})

@login_required
def deletar_servidor(request):
    id = request.POST.get('id')
    server = AcessoServidores.objects.get(id=id)
    server.delete()

    return JsonResponse({'status': True})