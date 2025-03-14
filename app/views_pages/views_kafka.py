from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import json
from ..kafka_functions import main, recreate


@login_required
def gerenciador_kafka(request):
    ambientes = {
        'ambientes': ['prd', 'prd2', 'uat', 'dev', 'qa']
    }
    functions = {
        'functions': ['show', 'show_details', 'restart', 'recreate', 'pause', 'resume', 'recreate_from_disk', 'edit_connector', 'drop_topics', 'delete', 'create_in_disk', 'create_not_exists', 'validate_columns', 'show_rm_topic_log', 'rename_connector', 'show_topics', 'clear_topics', 'check_duplicate', 'new_connector']
    }
    return render(request, 'gerenciador_kafka.html', {**ambientes, **functions})

@login_required
def get_ambiente(request):
    ambiente = request.GET.get('ambiente')
    serversl = request.GET.get('server')
    servers = {
        'servers':{
            'dev': {'schemaregistry': [ {'ip': '10.40.129.3', 'name': 'vmzokshbru01dev'}, {'ip': '10.40.129.6', 'name': 'vmzokshbru02dev'}, {'ip': '10.40.129.9', 'name': 'vmzokshbru03dev'} ], 'zookeeper': [ {'ip': '10.40.129.3', 'name': 'vmzokshbru01dev'}, {'ip': '10.40.129.6', 'name': 'vmzokshbru02dev'}, {'ip': '10.40.129.9', 'name': 'vmzokshbru03dev'} ], 'kafka': [ {'ip': '10.40.129.4', 'name': 'vmkfbrobru01dev'}, {'ip': '10.40.129.7', 'name': 'vmkfbrobru02dev'}, {'ip': '10.40.129.12', 'name': 'vmkfbrobru03dev'}, {'ip': '10.40.129.13', 'name': 'vmkfbrobru04dev'} ], 'kafkaconnect': [ {'ip': '10.40.129.2', 'name': 'vmkfconbru01dev'}, {'ip': '10.40.129.5', 'name': 'vmkfconbru02dev'}, {'ip': '10.40.129.8', 'name': 'vmkfconbru03dev'} ] },
            'qa': {'schemaregistry': [ {'ip': '10.60.129.3', 'name': 'vmzokshbru01qa'}, {'ip': '10.60.129.6', 'name': 'vmzokshbru02qa'}, {'ip': '10.60.129.9', 'name': 'vmzokshbru03qa'} ], 'zookeeper': [ {'ip': '10.60.129.3', 'name': 'vmzokshbru01qa'}, {'ip': '10.60.129.6', 'name': 'vmzokshbru02qa'}, {'ip': '10.60.129.9', 'name': 'vmzokshbru03qa'} ], 'kafka': [ {'ip': '10.60.129.4', 'name': 'vmkfbrobru01qa'}, {'ip': '10.60.129.7', 'name': 'vmkfbrobru02qa'}, {'ip': '10.60.129.12', 'name': 'vmkfbrobru03qa'} ], 'kafkaconnect': [ {'ip': '10.60.129.2', 'name': 'vmkfconbru01qa'}, {'ip': '10.60.129.5', 'name': 'vmkfconbru02qa'}, {'ip': '10.60.129.8', 'name': 'vmkfconbru03qa'} ] },
            'uat': {'schemaregistry': [ {'ip': '10.80.129.3', 'name': 'vmzokshbru01uat'}, {'ip': '10.80.129.6', 'name': 'vmzokshbru02uat'}, {'ip': '10.80.129.9', 'name': 'vmzokshbru03uat'} ], 'zookeeper': [ {'ip': '10.80.129.3', 'name': 'vmzokshbru01uat'}, {'ip': '10.80.129.6', 'name': 'vmzokshbru02uat'}, {'ip': '10.80.129.9', 'name': 'vmzokshbru03uat'} ], 'kafka': [ {'ip': '10.80.129.4', 'name': 'vmkfbrobru01uat'}, {'ip': '10.80.129.7', 'name': 'vmkfbrobru02uat'}, {'ip': '10.80.129.12', 'name': 'vmkfbrobru03uat'} ], 'kafkaconnect': [ {'ip': '10.80.129.2', 'name': 'vmkfconbru01uat'}, {'ip': '10.80.129.5', 'name': 'vmkfconbru02uat'}, {'ip': '10.80.129.8', 'name': 'vmkfconbru03uat'} ] },
            'prd': {'schemaregistry': [ {'ip': '192.168.134.240', 'name': 'kafkasr01'}, {'ip': '192.168.134.230', 'name': 'kafkasr02'} ], 'zookeeper': [ {'ip': '192.168.134.229', 'name': 'zookeeper01'}, {'ip': '192.168.134.234', 'name': 'zookeeper02'}, {'ip': '192.168.134.235', 'name': 'zookeeper03'} ], 'kafka': [ {'ip': '192.168.134.224', 'name': 'kafka01'}, {'ip': '192.168.134.226', 'name': 'kafka02'}, {'ip': '192.168.134.228', 'name': 'kafka03'}, {'ip': '192.168.134.239', 'name': 'kafka04'}, {'ip': '192.168.134.114', 'name': 'kafka05'}, {'ip': '192.168.134.120', 'name': 'kafka06'}, {'ip': '192.168.134.116', 'name': 'kafka07'}, {'ip': '192.168.134.117', 'name': 'kafka08'} ], 'kafkaconnect': [ {'ip': '192.168.134.236', 'name': 'kafkaCon01'}, {'ip': '192.168.134.237', 'name': 'kafkaCon02'}, {'ip': '192.168.134.231', 'name': 'kafkaCon03'}, {'ip': '192.168.134.11', 'name': 'kafkaCon04'}, {'ip': '192.168.134.118', 'name': 'kafkaCon05'}, {'ip': '192.168.134.119', 'name': 'kafkaCon06'} ] },
            'prd2': {'schemaregistry': [ {'ip': '192.168.129.15', 'name': 'vmkafssp201prd'},  {'ip': '192.168.129.16', 'name': 'vmkafssp202prd'},  {'ip': '192.168.129.17', 'name': 'vmkafssp203prd'} ],  'zookeeper': [ {'ip': '192.168.129.18', 'name': 'vmkafzsp201prd'},  {'ip': '192.168.129.19', 'name': 'vmkafzsp202prd'},  {'ip': '192.168.129.20', 'name': 'vmkafzsp203prd'} ],  'kafka': [ {'ip': '192.168.129.8', 'name': 'vmkafbsp201prd'},  {'ip': '192.168.129.9', 'name': 'vmkafbsp202prd'},  {'ip': '192.168.129.10', 'name': 'vmkafbsp203prd'},  {'ip': '192.168.129.11', 'name': 'vmkafbsp204prd'},  {'ip': '192.168.129.12', 'name': 'vmkafbsp205prd'},  {'ip': '192.168.129.13', 'name': 'vmkafbsp206prd'},  {'ip': '192.168.129.14', 'name': 'vmkafbsp207prd'} ],  'kafkaconnect': [ {'ip': '192.168.129.5', 'name': 'vmkafcsp201prd'},  {'ip': '192.168.129.6', 'name': 'vmkafcsp202prd'},  {'ip': '192.168.129.7', 'name': 'vmkafcsp203prd'} ] },
        }
    }
    servers = servers['servers'][ambiente][serversl]
    return JsonResponse({'servers': servers})


@login_required
def recreate_connector(request):
    server = request.POST.get('server')
    conector = request.POST.get('filter')
    config = request.POST.get('config')
    config = {'name': conector, 'config': json.loads(config)}
    r = recreate(server, conector, config)
    if r:
        return JsonResponse({'conector': conector, 'status': 'Criado!'})
    else:
        return JsonResponse({'conector': conector, 'status': 'Erro ao criar!'})

def __state(state):
        if state == 'RUNNING':
            return f'<span class="text-success">{state}</span>'
        elif state == 'FAILED':
            return f'<span class="text-danger">{state}</span>'
        elif state == 'STOPPED':
            return f'<span class="text-danger">{state}</span>'
        else:
            return f'<span class="text-info">{state}</span>'
        
@login_required
def actions(request):
    server = request.GET.get('server')
    filtro = request.GET.get('filter')
    funcao = request.GET.get('function')
    
    original_list = main(s=server, filtro=filtro, funcao=funcao, endswith=True) 
    
    # failed_entries = [entry for entry in original_list if entry['state'] == 'FAILED' or entry['task_state'] == 'FAILED']
    if original_list:
        original_list = sorted(original_list, key=lambda x: (x.get('state') != 'FAILED', x.get('task_state') != 'FAILED', x.get('state'), x.get('task_state')))

    new_dict = {}
    if original_list:
        for item in original_list:
            try:
                for key, value in item.items():
                    if key not in new_dict:
                        new_dict[key] = []
                    if key in ('connector', 'conector'):
                        value = value.split(' ')[0]
                    new_dict[key].append(value)
            except:
                if item not in new_dict:
                    new_dict[item] = []
                new_dict[item].append(original_list[item])
    else:
        new_dict = {'conector': ['Nenhum dado retornado'], 'state': [''], 'task_state': ['']}
        

    if funcao in ('show', 'show_details'):
        for index, state in enumerate(new_dict['state']):
            new_dict['state'][index] = __state(state)
        for index, tstate in enumerate(new_dict['task_state']):
            new_dict['task_state'][index] = __state(tstate)

    return JsonResponse(new_dict)
