import paramiko
import time, pytz
import re
import pymssql
import psycopg2
import django.utils.timezone as timezone
from .models import Slots

def conecta(servidor):
    hostname = servidor.nome
    port = servidor.porta_ssh
    username = servidor.usuario
    password = servidor.pwd

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(hostname, port=port, username=username, password=password)
    
    chan = ssh.get_transport().open_session()
    chan.get_pty()
    chan.setblocking(1)

    return [ssh, chan]


def restart_service(servidor):
    hostname = servidor.nome
    password = servidor.pwd
    service_name = servidor.service
    ssh, chan = conecta(servidor)

    restart_command = f"sudo systemctl restart {service_name}" if service_name != 'zookeeper' else "sudo /opt/zookeeper/bin/zkServer.sh restart"

    chan.exec_command(restart_command)

    # while not chan.recv_ready():
    time.sleep(1)

    stdout = str(chan.recv(4096).decode('utf-8'))
    if re.search('[Ss]enha|[Pp]assword', stdout):
        chan.send(password + '\n')
    time.sleep(5)
        
    chan.close()
    ssh.close()

    ssh, chan = conecta(servidor)

    status_command = f"sudo systemctl status {service_name}" if service_name != 'zookeeper' else "sudo /opt/zookeeper/bin/zkServer.sh status"

    chan.exec_command(status_command)

    time.sleep(1)
    stdout = str(chan.recv(4096).decode('utf-8'))
    print(stdout)
    if re.search('[Ss]enha|[Pp]assword', stdout):
        chan.send(password + '\n')
        time.sleep(2)
        stdout = str(chan.recv(4096).decode('utf-8'))
        print(stdout)
    time.sleep(5)

    print(f'Serviço {service_name} reiniciado no servidor {hostname}')
    return True


def space_disks(servidor):
    ssh, chan = conecta(servidor)

    stdin, stdout, stderr = ssh.exec_command("free -h")
    servidor.memory = stdout.read().decode()

    # Carga da CPU
    stdin, stdout, stderr = ssh.exec_command("top -n 1 -b | head -n 10")
    servidor.cpu = stdout.read().decode()

    # Espaço em disco
    stdin, stdout, stderr = ssh.exec_command("df -h")
    servidor.disk = stdout.read().decode()
    servidor.save()
    
    return servidor


def try_connection(servidorExpurgo):
    try:
        if servidorExpurgo.engine == 'sqlserver':
            bases = [b.strip() for b in servidorExpurgo.bases.split(',')]
            for base in bases:
                pymssql.connect(host=servidorExpurgo.servidor, database=base, user=servidorExpurgo.usuario, password=servidorExpurgo.senha)
            return True
        elif servidorExpurgo.engine == 'postgresql':
            bases = [b.strip() for b in servidorExpurgo.bases.split(',')]
            for base in bases:
                psycopg2.connect(host=servidorExpurgo.servidor, database=base, user=servidorExpurgo.usuario, password=servidorExpurgo.senha)
            return True
    except:
        return False

def atualiza_status_slot(servidores):
    servidor = None
    for servidor in servidores:
        # print(f'Atualizando status dos slots do servidor {servidor.apelido}')
        bases = [b.strip() for b in servidor.bases.split(',')]
        for base in bases:
            conn = psycopg2.connect(host=servidor.servidor, database=base, user=servidor.usuario, password=servidor.decrypt_password())
            cursor = conn.cursor()

            cursor.execute('select slot_name,active, pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(),restart_lsn)) as lag_pretty from pg_replication_slots')
            res = cursor.fetchall()

            data_atual = timezone.now()
            if data_atual.tzinfo is None:
                data_atual = data_atual.astimezone(pytz.timezone('America/Sao_Paulo'))

            
            for row in res:
                slot, created = Slots.objects.update_or_create(
                    nome=row[0],
                    defaults={'status': row[1], 'tamanho': row[2], 'servidor': servidor, 'datahora': data_atual}
                )
                if not created:
                    slot.status = row[1]
                    slot.tamanho = row[2]
                    slot.datahora = data_atual
                    slot.save()
            
            cursor.close()
            conn.close()

