import json
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from ..models import Expurgo, AcessoServidores
from ..tasks import try_connection
from ..expurgo import ExpurgoApp
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils import timezone

@login_required
def expurgo(request):
    return render(request, 'expurgo.html')


@login_required
def atualizar_tabelas(request):
    servidores = Expurgo.objects.all()
    html = render_to_string('partials/expurgo_tables.html', {'servidores': servidores})
    return JsonResponse({'html': html})

@login_required
def validar_tabelas(request):
    expurgo = ExpurgoApp()
    expurgo.validar_tabelas()
    return JsonResponse({'status': True})

@login_required
def deletar_selecionadas(request):
    ids = request.POST.getlist('deletar[]')
    
    for id in ids:
        expurgo = Expurgo.objects.get(id=id)
        expurgo.deletado = True
        expurgo.datahoradeleted = timezone.now()
        expurgo.save()

    return JsonResponse({'status': True})

