from django.http import JsonResponse
from ..tasks import restart_service, space_disks
from ..models import Servidor
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import render_to_string
from jobs import jobs
from django.core import serializers
import json

# Listar Servidores
@login_required
def servidores(request):
    servidores = Servidor.objects.all().order_by('status')
    context = {'servidores': servidores}
    return render(request, 'servidores.html', context)

@login_required
def atualizar_status_servidores(request):
    servidores = Servidor.objects.all().order_by('status')
    for serv in servidores:
        if serv.cpu:
            try:
                serv.cpuinfo = serv.cpu.splitlines()[0].split('load average: ')[1]
            except IndexError:
                ...
        if serv.memory:
            try:
                serv.memoriainfo = serv.memory.splitlines()[1].split('   ')[-1].strip()
            except IndexError:
                ...
        if serv.disk:
            try:
                filter_lines = [l for l in serv.disk.splitlines() if l[-1] == '/']
                if filter_lines:
                    filter_lines = [l for l in filter_lines[0].split(' ') if l != '']
                    serv.usoinfo = filter_lines[-2]
                    serv.dispinfo = filter_lines[-3]
            except IndexError:
                ...

    context = {'servidores': servidores}
    html = render_to_string('partials/status_servidores_partial.html', context)
    return JsonResponse({'html': html})

@login_required
def reiniciar_servico(request):
    print('reiniciando serviço')
    servico = request.POST.get('servico')
    servidor = request.POST.get('servidor')
    usuario = request.POST.get('user')
    pwd = request.POST.get('pwd')
    serv = Servidor.objects.get(nome=servidor, service=servico)
    serv.pwd = pwd
    serv.usuario = usuario
    status = restart_service(serv)
    return JsonResponse({'status': status})

@login_required
def obter_detalhes_servico(request):
    servico = request.POST.get('servico')
    servidor = request.POST.get('servidor')
    usuario = request.POST.get('user')
    pwd = request.POST.get('pwd')
    serv = Servidor.objects.get(nome=servidor, service=servico)
    serv.pwd = pwd
    serv.usuario = usuario
    result_servidor = space_disks(serv)
    result_servidor.cpu = result_servidor.cpu.replace('\n', '<br>') 
    result_servidor.disk = result_servidor.disk.replace('\n', '<br>') 
    result_servidor.memory = result_servidor.memory.replace('\n', '<br>') 
    servidor_json = serializers.serialize('json', [result_servidor])
    servidor_dict = json.loads(servidor_json)
    return JsonResponse({'status': True, 'servidor': servidor_dict})

@login_required
def atualizar_todos_detalhes(request):
    usuario = request.POST.get('usuario')
    pwd = request.POST.get('password')
    servidores = Servidor.objects.all()
    for servidor in servidores:
        servidor.usuario = usuario
        servidor.pwd = pwd
        try:
            space_disks(servidor)
        except:
            print('Erro ao atualizar detalhes do servidor', servidor)
    return JsonResponse({'status': True})

@login_required
def atualizar_conexao(request):
    servidor = request.GET.get('servidor')
    servico = request.GET.get('servico')
    jobs.atualizar_conexoes(Servidor, {'nome': servidor, 'service': servico})
    return JsonResponse({'status': True})

@login_required
def atualizar_conexoes(request):
    jobs.atualizar_conexoes(Servidor)
    return JsonResponse({'status': True})
