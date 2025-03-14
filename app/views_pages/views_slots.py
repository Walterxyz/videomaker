from django.http import HttpResponse, JsonResponse
from ..tasks import atualiza_status_slot
from ..models import Slots, AcessoServidores
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import render_to_string
from jobs import jobs
from django.core.serializers.json import DjangoJSONEncoder
import json
import re, pytz
from django.db.models import Count, Max
from collections import defaultdict

# Listar Servidores
@login_required
def slots(request):
    slots = Slots.objects.all().order_by('status')
    context = {'slots': slots}
    return render(request, 'validar_slots.html', context)

@login_required
def consultar_slots(request):
    atualiza_status_slot(AcessoServidores.objects.filter(inslots=True))
    return JsonResponse({'success': True}, status=200)

@login_required
def atualizar_slots(request):
    slots = Slots.objects.values('servidor__apelido', 'nome', 'tamanho', 'status', 'datahora').filter(servidor__inslots=True)
    data_atualizado = slots.aggregate(Max('datahora'))['datahora__max']
    
    for slot in slots:
        num = re.findall(r'\d+', slot['tamanho'])
        slot['datahora'] = slot['datahora'].astimezone(pytz.timezone('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M:%S')
        if 'kB' in slot['tamanho'] or 'bytes' in slot['tamanho']:
            slot['class'] = 'bg-success'
        elif 'MB' in slot['tamanho']:
            if int(num[0]) < 500:
                slot['class'] = 'bg-success'
            else:
                slot['class'] = 'bg-warning text-dark'
        else:
            slot['class'] = 'bg-danger'

    slots_json = json.dumps(list(slots), cls=DjangoJSONEncoder)
    slots_json = json.loads(slots_json)
    grouped_data = defaultdict(list)

    for entry in slots_json:
        servidor = entry['servidor__apelido']
        del entry['servidor__apelido'] 

        grouped_data[servidor].append(entry)

    servidores = [{"servidor": servidor, "slots": slots} for servidor, slots in grouped_data.items()]

    context = {'servidores': servidores, 'data_atualizado': data_atualizado}
    html = render_to_string('partials/slots_partial.html', context)
    return JsonResponse({'html': html, 'data_atualizado': data_atualizado})