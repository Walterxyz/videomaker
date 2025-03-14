import os
import json
import psycopg2
import requests
import re
from datetime import datetime, timedelta, date
from tabulate import tabulate
from .models import Expurgo, AcessoServidores
from django.utils import timezone


class ExpurgoApp:
    def __init__(self):
        self.servers = AcessoServidores.objects.filter(engine='postgresql')

    def validar_tabelas(self):
        print('iniciando')
        for conexao in self.servers:
                connection = psycopg2.connect(host=conexao.servidor, database=conexao.base, user=conexao.usuario, password=conexao.decrypt_password())
                cursor = connection.cursor()
                
                query = "SELECT datname, d.*  FROM pg_catalog.pg_database d WHERE datname NOT IN ('cloudsqladmin', 'postgres', 'template1', 'template0');"
                cursor.execute(query)
                resultados = cursor.fetchall()
        
                for row in resultados:
                    conn = psycopg2.connect(host=conexao.servidor, database=row[0], user=conexao.usuario, password=conexao.decrypt_password())
                    cur = conn.cursor()
                    cur.execute("SELECT schemaname, tablename, ROUND(pg_total_relation_size(schemaname || '.' || tablename) / 1048576.0, 2) AS size_mb FROM pg_tables WHERE (tablename ~ 'tmp.*') or (tablename ~ 'bkp.*');")
                    res = cur.fetchall()
                    for tb in res:
                        base = row[0]
                        tabela = tb[1]
                        
                        numbers = re.sub(r'\D', '', tabela)
                        current_date = datetime.now()
                        current_year = datetime.now().year
                        year_index = False
                        final_date = None
                        try:
                            year_index = numbers.index(str(current_year))
                            if year_index:
                                data_na_tabela = numbers[year_index:year_index+8]   
                                date_object = datetime.strptime(data_na_tabela, "%Y%m%d")
                                if 'bkp' in tabela:
                                    final_date = date_object + timedelta(days=90)
                                else:
                                    final_date = date_object + timedelta(days=30)
                        except:
                            final_date = current_date + timedelta(days=60)

                        final_date = timezone.make_aware(final_date, timezone.get_current_timezone())

                        expurgo_instance, created = Expurgo.objects.get_or_create(
                            servidor=conexao,
                            base=base,
                            tabela=tabela,
                            defaults={
                                'tamanhomb': tb[2],
                                'deletado': False,
                                'datahoradeleted': None,
                                'datahoratodelete': final_date
                            }
                        )
                        if not created:
                            expurgo_instance.tamanhomb = tb[2]
                            expurgo_instance.deletado = False
                            expurgo_instance.datahoradeleted = None
                            expurgo_instance.datahoratodelete = final_date
                            expurgo_instance.save()

        print('fim')
        return True

                    
                            
