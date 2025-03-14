import socket
import subprocess
from ping3 import ping, verbose_ping

def atualizar_conexoes(servidores, filtro = False):
    if filtro:
        servidores = [servidores.objects.get(nome=filtro['nome'], service=filtro['service'])]
    else:
        servidores = servidores.objects.all()

    for servidor in servidores:
        status = testar_conexao(servidor.nome, servidor.porta)
        status_ping = testar_ping(servidor.nome)
        servidor.status = status
        servidor.status_ping = status_ping
        servidor.save()

def testar_conexao(servidor, porta):
    try:
        with socket.create_connection((servidor, porta), timeout=5) as conn:
            return True
    except:
        return False

def testar_ping(servidor):
    response_time = ping(servidor)
    
    if response_time is not None:
        return True
    else:
        return False