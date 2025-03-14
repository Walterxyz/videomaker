import requests, re, os, shutil, paramiko, pymssql, random, time
from json import loads
from pprint import pprint
from getpass import getpass 
import subprocess

local_key_path = ''

def get_users(s):
    servers = {
        'dev': {'user': 'kafka', 'pass': 'K@fk@1K@fk@'},
        'qa': {'user': 'kafka', 'pass': 'K@fk@1K@fk@'},
        'uat': {'user': 'kafka', 'pass': 'K@fk@1K@fk@'},
        'prd': {'user': 'kafka', 'pass': 'K@fk@'},
        'html': {'user': 'kafka', 'pass': 'K@fk@1K@fk@DEVQA'},
        'prd2': {'user': 'kafka', 'pass': 'K@fk@'},
    }
    return servers[s]

def get_servers(find, retorna):
    servers = {
    'dev': {'schemaregistry': [ {'ip': '10.40.129.3', 'name': 'vmzokshbru01dev'}, {'ip': '10.40.129.6', 'name': 'vmzokshbru02dev'}, {'ip': '10.40.129.9', 'name': 'vmzokshbru03dev'} ], 'zookeeper': [ {'ip': '10.40.129.3', 'name': 'vmzokshbru01dev'}, {'ip': '10.40.129.6', 'name': 'vmzokshbru02dev'}, {'ip': '10.40.129.9', 'name': 'vmzokshbru03dev'} ], 'kafka': [ {'ip': '10.40.129.4', 'name': 'vmkfbrobru01dev'}, {'ip': '10.40.129.7', 'name': 'vmkfbrobru02dev'}, {'ip': '10.40.129.12', 'name': 'vmkfbrobru03dev'}, {'ip': '10.40.129.13', 'name': 'vmkfbrobru04dev'} ], 'kafkaconnect': [ {'ip': '10.40.129.2', 'name': 'vmkfconbru01dev'}, {'ip': '10.40.129.5', 'name': 'vmkfconbru02dev'}, {'ip': '10.40.129.8', 'name': 'vmkfconbru03dev'} ] },
    'qa': {'schemaregistry': [ {'ip': '10.60.129.3', 'name': 'vmzokshbru01qa'}, {'ip': '10.60.129.6', 'name': 'vmzokshbru02qa'}, {'ip': '10.60.129.9', 'name': 'vmzokshbru03qa'} ], 'zookeeper': [ {'ip': '10.60.129.3', 'name': 'vmzokshbru01qa'}, {'ip': '10.60.129.6', 'name': 'vmzokshbru02qa'}, {'ip': '10.60.129.9', 'name': 'vmzokshbru03qa'} ], 'kafka': [ {'ip': '10.60.129.4', 'name': 'vmkfbrobru01qa'}, {'ip': '10.60.129.7', 'name': 'vmkfbrobru02qa'}, {'ip': '10.60.129.12', 'name': 'vmkfbrobru03qa'} ], 'kafkaconnect': [ {'ip': '10.60.129.2', 'name': 'vmkfconbru01qa'}, {'ip': '10.60.129.5', 'name': 'vmkfconbru02qa'}, {'ip': '10.60.129.8', 'name': 'vmkfconbru03qa'} ] },
    'uat': {'schemaregistry': [ {'ip': '10.80.129.3', 'name': 'vmzokshbru01uat'}, {'ip': '10.80.129.6', 'name': 'vmzokshbru02uat'}, {'ip': '10.80.129.9', 'name': 'vmzokshbru03uat'} ], 'zookeeper': [ {'ip': '10.80.129.3', 'name': 'vmzokshbru01uat'}, {'ip': '10.80.129.6', 'name': 'vmzokshbru02uat'}, {'ip': '10.80.129.9', 'name': 'vmzokshbru03uat'} ], 'kafka': [ {'ip': '10.80.129.4', 'name': 'vmkfbrobru01uat'}, {'ip': '10.80.129.7', 'name': 'vmkfbrobru02uat'}, {'ip': '10.80.129.12', 'name': 'vmkfbrobru03uat'} ], 'kafkaconnect': [ {'ip': '10.80.129.2', 'name': 'vmkfconbru01uat'}, {'ip': '10.80.129.5', 'name': 'vmkfconbru02uat'}, {'ip': '10.80.129.8', 'name': 'vmkfconbru03uat'} ] },
    'prd': {'schemaregistry': [ {'ip': '192.168.134.240', 'name': 'kafkasr01'}, {'ip': '192.168.134.230', 'name': 'kafkasr02'} ], 'zookeeper': [ {'ip': '192.168.134.229', 'name': 'zookeeper01'}, {'ip': '192.168.134.234', 'name': 'zookeeper02'}, {'ip': '192.168.134.235', 'name': 'zookeeper03'} ], 'kafka': [ {'ip': '192.168.134.224', 'name': 'kafka01'}, {'ip': '192.168.134.226', 'name': 'kafka02'}, {'ip': '192.168.134.228', 'name': 'kafka03'}, {'ip': '192.168.134.239', 'name': 'kafka04'}, {'ip': '192.168.134.114', 'name': 'kafka05'}, {'ip': '192.168.134.120', 'name': 'kafka06'}, {'ip': '192.168.134.116', 'name': 'kafka07'}, {'ip': '192.168.134.117', 'name': 'kafka08'} ], 'kafkaconnect': [ {'ip': '192.168.134.236', 'name': 'kafkaCon01'}, {'ip': '192.168.134.237', 'name': 'kafkaCon02'}, {'ip': '192.168.134.231', 'name': 'kafkaCon03'}, {'ip': '192.168.134.11', 'name': 'kafkaCon04'}, {'ip': '192.168.134.118', 'name': 'kafkaCon05'}, {'ip': '192.168.134.119', 'name': 'kafkaCon06'} ] },
    'html':{ 'schemaregistry':[ { 'ip':'192.168.182.32', 'name':'zookeepper01hml' }, { 'ip':'192.168.182.36', 'name':'zookeepper02hml' }, { 'ip':'192.168.182.39', 'name':'zookeepper03hml' } ], 'zookeeper':[ { 'ip':'192.168.182.32', 'name':'zookeepper01hml' }, { 'ip':'192.168.182.36', 'name':'zookeepper02hml' }, { 'ip':'192.168.182.39', 'name':'zookeepper03hml' } ], 'kafka':[ { 'ip':'192.168.182.33', 'name':'kafkabroker01hml' }, { 'ip':'192.168.182.35', 'name':'kafkabroker02hml' }, { 'ip':'192.168.182.37', 'name':'kafkabroker03hml' } ], 'kafkaconnect':[ { 'ip':'192.168.182.31', 'name':'kafkacon01hml' }, { 'ip':'192.168.182.34', 'name':'kafkacon02hml' }, { 'ip':'192.168.182.38', 'name':'kafkacon03hml' } ] },
    'prd2': {'schemaregistry': [ {'ip': '192.168.129.15', 'name': 'vmkafssp201prd'},  {'ip': '192.168.129.16', 'name': 'vmkafssp202prd'},  {'ip': '192.168.129.17', 'name': 'vmkafssp203prd'} ],  'zookeeper': [ {'ip': '192.168.129.18', 'name': 'vmkafzsp201prd'},  {'ip': '192.168.129.19', 'name': 'vmkafzsp202prd'},  {'ip': '192.168.129.20', 'name': 'vmkafzsp203prd'} ],  'kafka': [ {'ip': '192.168.129.8', 'name': 'vmkafbsp201prd'},  {'ip': '192.168.129.9', 'name': 'vmkafbsp202prd'},  {'ip': '192.168.129.10', 'name': 'vmkafbsp203prd'},  {'ip': '192.168.129.11', 'name': 'vmkafbsp204prd'},  {'ip': '192.168.129.12', 'name': 'vmkafbsp205prd'},  {'ip': '192.168.129.13', 'name': 'vmkafbsp206prd'},  {'ip': '192.168.129.14', 'name': 'vmkafbsp207prd'} ],  'kafkaconnect': [ {'ip': '192.168.129.5', 'name': 'vmkafcsp201prd'},  {'ip': '192.168.129.6', 'name': 'vmkafcsp202prd'},  {'ip': '192.168.129.7', 'name': 'vmkafcsp203prd'} ] },
    }
    busca = []
    cred = {}
    for s in servers:
        for con in servers[s]['kafkaconnect']:
            if(find.lower() == con['name'].lower() or find.lower() == con['ip'].lower()):
                busca = servers[s][retorna]
                cred = get_users(s)
                
    result = []
    for b in busca:
        result.append(b['name'])
    
    return {'credentials': cred, 'servers': result}
    

def get_columns(server, user, pwd, base, table):
    conn = pymssql.connect(server=server, user=user, password=pwd, database=base, autocommit=True)
    cursor = conn.cursor()

    cursor.execute(''' SELECT NAME FROM SYS.COLUMNS WHERE OBJECT_ID = OBJECT_ID('{}') AND NAME NOT LIKE 'rowversion' '''.format(table))
    columns = []
    for n in cursor.fetchall():
        columns.append(n[0])
    conn.close()
    return ','.join(columns)

def lista(s):
    res = requests.get('http://{}:8083/connectors/'.format(s))
    result = res.json()
    return result

def filtra(s):
    res = requests.get('http://{}:8083/connectors?expand=info&expand=status'.format(s))
    result = res.json()
    return result
    
def save(arq, data, caminho):
    if(not os.path.exists(caminho)):
        os.makedirs(caminho)
    path = caminho + arq + '.txt'
    with open(path, 'w+') as file:
        file.write(str(data))
        file.close

#     server_username = input('login ssh: ') #'user_dba.infra'
#     server_pass = getpass('senha ssh: ') #'func@2021'
def run_sudo_server(command, server_address):
    global local_key_path
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=server_address,
                username='walter.silva',
                key_filename=local_key_path,
                port=15022,
                timeout=600)
    session = ssh.get_transport().open_session()
    session.set_combine_stderr(True)
    session.get_pty()
    session.exec_command("sudo bash -c \"" + command + "\"")
    stdout = session.makefile('rb', -1)
    return stdout.read().decode("utf-8")

def server_format(config):
    if('connection.url' not in config):
        user = config['database.user']
        pwd = config['database.password']
        server = config['database.server.name'].split('.')[0]
        base = config['database.server.name'].split('.')[1]
        table = config['table.whitelist'].split('.')[1]
    elif('${file:' not in config['connection.url']):
        table = config['table.name.format']
        config = config['connection.url'].split('//')[1]
        user = config.split(';')[2].split('=')[1]
        pwd = config.split(';')[3].split('=')[1]
        server = config.split(';')[0].split('.')[0]
        base = config.split(';')[1].split('=')[1]
    else:
        return None
    if server == 'VMPLTDBBRU01QA':
        server = 'PLANTQA'
    return {'user': user, 'pwd': pwd, 'server': server, 'base': base, 'table': table}
    

def valida_info(info, u):
    server = info.split('.')[0]
    base = info.split('.')[1]
    schema = info.split('.')[2]
    table = info.split('.')[3]
    print(u['user'], u['pass'])
    conn = pymssql.connect(server=server, user=u['user'], password=u['pass'], database=base)
    cursor = conn.cursor()

    cursor.execute(''' 
    select @@SERVERNAME, DB_NAME(), sh.name sh, tab.name tab
    from sys.tables tab
    join sys.schemas sh on tab.schema_id = sh.schema_id
    where tab.name = '{}'
    '''.format(table))
    
    dados = cursor.fetchone() 
    conn.close()
    
    return dados

def get_pk(server, user, pwd, base, table):
    conn = pymssql.connect(server=server, user=user, password=pwd, database=base)
    cursor = conn.cursor()

    cursor.execute(''' 
    select col.[name]
    from sys.tables tab
    join sys.indexes pk on tab.object_id = pk.object_id and pk.is_primary_key = 1
    join sys.index_columns ic on ic.object_id = pk.object_id and ic.index_id = pk.index_id
    join sys.columns col on pk.object_id = col.object_id and col.column_id = ic.column_id
    where tab.name = '{}'
    '''.format(table))
    
    columns = []
    for n in cursor.fetchall():
        columns.append(n[0])
    conn.close()

    return ','.join(columns)
        
def recria_cdc(dados, cdc):
    if('connection.url' not in dados['config']  and cdc):
        config = server_format(dados['config'])
        if(not config):
            return False
        conn = pymssql.connect(server=config['server'], user=config['user'], 
                               password=config['pwd'], database=config['base'], autocommit=True)
        cursor = conn.cursor()
        
        cursor.execute('''
                use {use}
                if((select cast(is_cdc_enabled as char(1)) from sys.databases WHERE name = DB_NAME()) <> 1)
                    exec sys.sp_cdc_enable_db
                
                use {use}
                exec sys.sp_cdc_disable_table @source_schema = 'dbo'
                                    , @source_name = '{tab}'
                                    , @capture_instance = 'all';
                                    
                use {use}
                exec sys.sp_cdc_enable_table @source_schema = 'dbo'
                                    , @source_name = '{tab}'
                                    , @role_name = NULL;
        
        '''.format(use=config['base'], tab=config['table']))
        
        conn.close()

        print('CDC recriado para base: {}.dbo.{}'.format(config['base'], config['table']))
        
        return False
    else:
        config = server_format(dados['config'])
        if(config):
            return get_columns(config['server'], config['user'], config['pwd'], config['base'], config['table'])
        else:
            return False
        
def drop_topic(s, topic):
    print('Conectando no servidor...')
    bootstrap = get_servers(s, 'kafka')['servers'][0]
    cmd = '''
    /opt/kafka/bin/kafka-topics.sh --bootstrap-server {s}:9092 --delete --topic {t}'''.format(s = bootstrap, t = topic)
    run_sudo_server(cmd, bootstrap)
    print('Topico excluido: {}'.format(topic))
        
def recreate_topic(s, topic, change = False):
    print('Conectando no servidor...')
    bootstrap = get_servers(s, 'kafka')['servers'][0]
    topicnum = random.randint(0, 9)
    if change:
        if topic[-1].isdigit():
            topicnew = topic[:-2] + '-' + str(topicnum)
        else:
            topicnew = topic + '-' + str(topicnum)
    else:
        topicnew = topic

    cmd = '''
    /opt/kafka/bin/kafka-topics.sh --bootstrap-server {s}:9092 --delete --topic {t}\n
    /opt/kafka/bin/kafka-topics.sh --bootstrap-server {s}:9092 --create --partitions 6 --replication-factor 3 --topic {tn}'''.format(s = bootstrap, t = topic, tn = topicnew)
    run_sudo_server(cmd, bootstrap)
    print('Topico recriado: {}'.format(topic))
    return topicnew
    
def show_topics(s):
    bootstrap = get_servers(s, 'kafka')['servers'][0]
    cmd = '''/opt/kafka/bin/kafka-topics.sh --bootstrap-server {s}:9092 --list'''.format(s=bootstrap)
    res = [{'Topicos': l.strip()} for l in run_sudo_server(cmd, bootstrap).splitlines() if '[sudo]' not in l]
    return res

def clear_topics(s):
    bootstrap = get_servers(s, 'kafka')['servers'][0]
    cmd = '''/opt/kafka/bin/kafka-topics.sh --bootstrap-server {s}:9092 --list'''.format(s=bootstrap)
    topicos = run_sudo_server(cmd, bootstrap).split('\r\n')
    dados = filtra(s)
    topicos_con = []
    for conector in dados.keys():
        for config in dados[conector]['info']['config']:
            if 'topic' in config:
                topicos_con.append(dados[conector]['info']['config'][config])

    cmd = '''/opt/kafka/bin/kafka-topics.sh --bootstrap-server {s}:9092 --delete --topic {t}\n'''
    command = ''
    for topico in topicos:
        if topico.count('.') > 2:
            if topico not in topicos_con:
                command += cmd.format(s = bootstrap, t = topico)
    print(command)
    if command:
        print('Excluindo tópicos nao usados...')
        run_sudo_server(command, bootstrap)
        print('Tópicos excluidos')
        return {'topicos': [command] }
    return {'topicos': []}

def recreate(s, conector, dados, newname = False, deleta = True, changetopic = False, cdc = False, topic = False):
    try:
        columns = recria_cdc(dados, cdc)
    except:
        columns = False
        
    if(columns):
        dados['config']['fields.whitelist'] = columns

    print(dados['config'])
    if deleta:
        requests.delete('http://{}:8083/connectors/{}'.format(s, conector))

    if topic:
        if('database.history.kafka.topic' in dados['config']):
            dados['config']['database.history.kafka.topic'] = recreate_topic(s, dados['config']['database.history.kafka.topic'], changetopic)
        if('database.kafka.topic' in dados['config']):     
            dados['config']['database.kafka.topic'] = recreate_topic(s, dados['config']['database.kafka.topic'], changetopic)
        if('topics' in dados['config']):
            dados['config']['topics'] = recreate_topic(s, dados['config']['topics'], changetopic)

    if newname:
        dados['name'] = newname

    res = requests.post('http://{}:8083/connectors/'.format(s), json=dados)
    res = res.json()
    if('name' in res):
        print('Conector: {} recriado'.format(dados['name']))
        if newname:
            return dados
        else:
            return True
    else:
        print('Erro ao recriar o conector: {}'.format(dados['name']))
        return False

def rename_con(s, conector, dados, caminho):
    connew = conector
    if re.search(r'v\d$', conector):
        num = int(conector[-1]) + 1
        connew = conector[:-2] + 'v' + str(num)
    else:
        connew = conector + '_v2'
    feito = recreate(s, conector, dados, connew, True, False, False, False)
    if feito:
        if os.path.exists(caminho+conector+'.txt'):
            os.remove(caminho+conector+'.txt')
        save(connew, feito, caminho)
    return connew 

def formata_con(data):
    data = data['info']
    if('tasks' in data):
        del data['tasks']
    if('type' in data):
        del data['type']
    if('name' in data['config']):
        del data['config']['name']
    return data

def action(comando, s, conector, task, dados, caminho, state = False):
    if(dados):
        dados = formata_con(dados[conector])
        
    if(comando == 'show_details'):
        return {'state': state, 'conector': conector, 'task': task['id'], 'task_state': task['state'], 'config': str(dados['config']), 'trace': task['trace'] if 'trace' in task else ''}
        
    if(comando == 'show'):
        return {'state': state, 'conector': conector, 'task': task['id'], 'task_state': task['state']}

    if(comando == 'show_rm_topic_log'):
        topic = ''
        if('database.history.kafka.topic' in dados['config']):
            topic = dados['config']['database.history.kafka.topic']
        if('database.kafka.topic' in dados['config']):     
            topic = dados['config']['database.kafka.topic']
        if('topics' in dados['config']):
            topic = dados['config']['topics']
        if topic[-1].isdigit():
            topic = topic[:-2]
        topic = topic.split('.')[-1]
        return {'Comandos': 'rm -fr $(ls | grep \'.{}-\') '.format(topic)}
    
    if(comando == 'validate_columns'):
        retorno = {'Conector': ''}
        if(dados['connector.class'] == 'io.confluent.connect.jdbc.JdbcSinkConnector'):
            config = server_format(dados['config'])
            if(not config):
                return False
            server_destino = dados['config']['topics'].split('.')[0]
            base_destino = dados['config']['topics'].split('.')[1]
            tabela_destino = dados['config']['topics'].split('.')[-1]
            cols_origem = get_columns(config['server'], config['user'], config['pwd'], config['base'], config['table'])
            cols_destino = get_columns(server_destino, config['user'], config['pwd'], base_destino, tabela_destino)
            if(cols_origem != cols_destino and cols_destino != dados['config'].get('fields.whitelist','')):
                retorno = {'conector': '{} com colunas incorretas'.format(conector)}
                recreate(s, conector, dados)
            else:
                retorno = {'conector': '{} com colunas corretas'.format(conector)}
        return retorno

        
    if(comando == 'restart'):
        requests.post('http://{}:8083/connectors/{}/tasks/{}/restart'.format(s, conector, task['id']))
        return { 'conector': f'{conector} reiniciado' }

        
    if(comando == 'pause'):
        requests.put('http://{}:8083/connectors/{}/pause'.format(s, conector))
        return { 'conector': f'{conector} pausado' }

        
    if(comando == 'resume'):
        requests.put('http://{}:8083/connectors/{}/resume'.format(s, conector))
        return { 'conector': f'{conector} iniciado' }
        
    if(comando == 'delete'):
        requests.delete('http://{}:8083/connectors/{}'.format(s, conector))
        return {'conector': f'{conector} deletado'}
    
    if(comando == 'recreate'):
        if recreate(s, conector, dados):
            return {'conector': conector, 'status': 'Recriado!'}
        else:
            return {'conector': conector, 'status': 'Erro ao Recriar'}

    if(comando == 'show_topics'):
        return show_topics(s)

    if(comando == 'clear_topics'):
        return {'Topicos': clear_topics(s)}

    if(comando == 'rename_connector'):
        return {'conector': conector, 'novo_conector': rename_con(s, conector, dados, caminho)}
        
    if(comando == 'drop_topics'):
        if('database.history.kafka.topic' in dados['config']):
            drop_topic(s, dados['config']['database.history.kafka.topic'])
        if('database.kafka.topic' in dados['config']):     
            drop_topic(s, dados['config']['database.kafka.topic'])
        if('topics' in dados['config']):
            drop_topic(s, dados['config']['topics'])

        
    if(comando == 'edit_connector'):
        if conector != '':
            print('Conector: {} '.format(conector))
            print('Task: {} Status: {}'.format(task['id'], task['state']))
            if('trace' in task):
                print('Trace: {} '.format(task['trace']))
            pprint('Config: {}'.format(str(dados['config'])))
            print('')
        connovo = config
        requests.delete('http://{}:8083/connectors/{}'.format(s, conector))
        res = requests.post('http://{}:8083/connectors/'.format(s), json=loads(connovo))
        res = res.json()
        return {'conector': conector, 'status': 'Editado!'}
        
    
    if(comando == 'create_not_exists'):
        filtro = conector
        conectores = lista(s)
        retorno = []
        for file in os.listdir(caminho):
            if os.path.isfile(os.path.join(caminho, file)):
                conector = file.replace('.txt','')
                if(conector not in conectores):
                    if filtro:
                        if filtro == conector:
                            with open(caminho+file) as fil:
                                for f in fil:
                                    data = loads(str(f.replace("'", "\"")))
                                    retorno.append(action('recreate', s, conector, task, data, caminho))
                                    
                    else:
                        with open(caminho+file) as fil:
                            for f in fil:
                                data = loads(str(f.replace("'", "\"")))
                                retorno.append(action('recreate', s, conector, task, data, caminho))
        return retorno
    
    
    if(comando == 'delete_not_in_disk'):
        conectores = lista(s)
        filecon = []
        for file in os.listdir(caminho):
            filecon.append(file.replace('.txt', ''))
        
        for conector in conectores:
            if conector not in filecon:
                print(conector)
                # requests.delete('http://{}:8083/connectors/{}'.format(s, conector))
                            
    if(comando == 'recreate_from_disk'):
        retorno = []
        for file in os.listdir(caminho):
            if os.path.isfile(os.path.join(caminho, file)):
                if(file.replace('.txt','') == conector):
                    with open(caminho+file) as fil:
                        for f in fil:
                            data = loads(str(f.replace("'", "\"")))
                            print(data)
                            retorno.append(action('recreate', s, conector, task, data, caminho))
        return retorno
    
    if(comando == 'create_in_disk'):
        save(conector, dados, caminho)
        return {'conector': conector, 'dados': dados, 'caminho': caminho, 'status': 'OK'}
        
    if(comando == 'check_duplicate'):
        conectores = lista(s)
        retorno = []
        for conector in conectores:
            if conector[-1].isdigit():
                if conector[:-2] in conectores:
                    retorno.append(action('delete', s, conector, 0, None, '', ''))
        return retorno
        # for conector in conectores:
        #     for conector2 in conectores:
        #         if conector[-1].isdigit() and conector2[-1].isdigit() and conector != conector2 and conector[:-2] == conector2[:-2]:
        #             del conectores[conectores.index(conector)]
        #             del conectores[conectores.index(conector2)]
        #             action('delete', s, conector, 0, None, '')


    if(comando == 'new_connector'):
        info_origem = input('Digite os dados da tabela de origem no formato: servidor.base.schema.tabela \n')
        info_destino = input('Digite os dados da tabela de destino no formato: servidor.base.schema.tabela \n')
        if(len(info_origem.split('.')) != 4 or len(info_destino.split('.')) != 4):
            print('Digite os dados corretamente da tabela corretamente')
        else:
            info_origem = valida_info(info_origem, get_servers(s, 'kafka')['credentials'])
            info_destino = valida_info(info_destino, get_servers(s, 'kafka')['credentials'])
            if(info_origem and info_destino):
                titulo = '_'.join(info_origem)
                o_server, o_base, o_schema, o_tabela = info_origem
                d_server, d_base, d_schema, d_tabela = info_destino
                n = get_servers(s, 'kafka')
                auth = n['credentials']
                bootstrap = ','.join(f'{w}:9092' for w in n['servers'])
                schemaregistry = ','.join(f'http://{w}:8081' for w in get_servers(s, 'schemaregistry')['servers'])
                pks = get_pk(o_server, auth['user'], auth['pass'], o_base, o_tabela)
                titulo_origem = 'Origem_{}'.format(titulo)
                titulo_destino = 'Destino_{}'.format(titulo)
                origem = {'name': titulo_origem, 'config': {'connector.class': 'io.confluent.connect.jdbc.JdbcSourceConnector', 'table.name.format': o_tabela, 'tasks.max': '1', 'database.history.kafka.topic': 'dbhistory.{}.{}.{}'.format(o_server, o_base, o_tabela), 'database.history.kafka.bootstrap.servers': bootstrap, 'time.precision.mode': 'connect', 'connection.url': 'jdbc:sqlserver://{}.funcional.local;databaseName={};user={};password={}'.format(o_server,o_base,auth['user'],auth['pass']), 'table.whitelist': '{}.{}'.format(o_schema, o_tabela), 'value.converter.schema.registry.url': schemaregistry, 'database.hostname': '{}.funcional.local'.format(o_server), 'value.converter': 'io.confluent.connect.avro.AvroConverter', 'key.converter': 'io.confluent.connect.avro.AvroConverter', 'key.converter.schema.registry.url': schemaregistry, 'snapshot.mode': 'initial_schema_only'}}
                destino = {'name': titulo_destino, 'config': {'connector.class': 'io.confluent.connect.jdbc.JdbcSinkConnector', 'table.name.format': d_tabela, 'tasks.max': '1', 'topics': '.'.join(info_destino), 'value.converter.schema.registry.url': schemaregistry, 'fields.whitelist': get_columns(d_server, auth['user'], auth['pass'], d_base, d_tabela), 'delete.enabled': 'true', 'auto.create': 'true', 'connection.url': 'jdbc:sqlserver://{}.funcional.local;databaseName={};user={};password={}'.format(d_server,d_base,auth['user'],auth['pass']), 'value.converter': 'io.confluent.connect.avro.AvroConverter', 'insert.mode': 'upsert', 'pk.mode': 'record_key', 'key.converter': 'io.confluent.connect.avro.AvroConverter', 'key.converter.schema.registry.url': schemaregistry, 'pk.fields': pks }}
                recreate(s, titulo_origem, origem)
                save(titulo_origem, origem, caminho)
                recreate(s, titulo_destino, destino)
                save(titulo_destino, destino, caminho)
        

def main(s, filtro = '', funcao = None, endswith = True):
    caminho = '/home/pymanager/kafka/{}/'.format(s)
    print('kafka')
    
    retorno = []
    if(funcao == 'create_not_exists'):
        retorno = action(funcao, s, filtro, None, None, caminho)
        print('Criacao executada.')
        return retorno

        
    if(funcao == 'delete_not_in_disk'):
        retorno = action(funcao, s, filtro, None, None, caminho)
        return retorno
    
    if(funcao == 'create_in_disk'):
        if(os.path.exists(caminho)):
            shutil.rmtree(caminho)
    
    if funcao in ('new_connector', 'check_duplicate', 'show_topics', 'clear_topics'):
        retorno = action(funcao, s, filtro, None, None, caminho)
        print('Fim')
        return retorno
    
    if(filtro == '' and funcao != 'create_in_disk'):
        filtro = funcao
        
    caminho_filtro = '{}{}/'.format(caminho, filtro)
    if(os.path.exists(caminho_filtro)):
        shutil.rmtree(caminho_filtro)
    conectores = filtra(s)

    for conector in conectores:
        if(len(conectores[conector]['status']['tasks']) == 0):
            conectores[conector]['status']['tasks'] = [{'id': 'Connector', **conectores[conector]['status']['connector']}]
        
        state = conectores[conector]['status']['connector']['state']
        for task in conectores[conector]['status']['tasks']:

            if endswith:
                fil = conector.lower().endswith(filtro.lower())
            else:
                fil = filtro.lower() in conector.lower()

            if(filtro == funcao or filtro.lower() == task['state'].lower() or filtro.lower() == state.lower() or fil):
                if(funcao):
                    retorno.append(action(funcao, s, conector, task, conectores, caminho, state))
                if(filtro != funcao):
                    save(conector, formata_con(conectores[conector]), caminho_filtro)
    if retorno:
        return retorno
                
            
        
    print('Fim')



#################################################################
# Alterar conforme necessidade no main conforme exemplo abaixo  #
#                                                               #
# main(                                                         #
#     'nome_do_servidor_do_connector' ex: 'vmkfconbru01qa'      #
#     ,                                                         #
#     aqui digitar filtro por status ou o nome do conector      #
#     ou o final do nome de um conector                         #
#     para ignorar o filtro deixe vazio                         #
#     ex: caso coloque 'VMBNFBRU01QA_Benefit_dbo_cad_prod_ean'  #
#     ele irá pegar sua origem e destino                        #
#     ,                                                         #
#     aqui digite a função                                      #
#     escolha entre elas                                        #
#     'show': Exibe os conectores                               #
#     'show_details': Exibe os conectores e detalhes            #
#     'restart': reinicia os conectores                         #
#     'recreate': recria os conectores a partir deles mesmo     #
#     'recreate_from_disk': recria os conectores a partir       #
#     dos salvos em disco                                       #
#     'create_in_disk': salva os conectores em uma pasta        #
#     no disco                                                  #
#     'create_not_exists': Cria conectores no servidor          #
#     que só existem em disco                                   #
#     'validate_columns': Para comparar as colunas de           #
#     origem e destino que estao sendo replicadas nos           #
#     conectores de destino                                     #
#     Atualmente gravando em C:\Kafka_Conectores\               #
#     'show_rm_topic_log': no broker remover                    #
#                          da pasta /data/kafka/log/            #
# )                                                             #
# Sugestao de uso:                                              #
# Primeiro gere os arquivos em disco                            #
# main('server', '', 'create_in_disk')                          #
# Depois disso já terá o backup de todos os conectores          #
#################################################################

