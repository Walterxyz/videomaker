from django.urls import path, include
from django.contrib.auth import views as auth_views

import app.views_pages.views_home as views_home
import app.views_pages.views_expurgo as views_expurgo
import app.views_pages.views_jira as views_jira
import app.views_pages.views_kafka as views_kafka
import app.views_pages.views_servidores as views_servidores
import app.views_pages.views_slots as views_slots
import app.views_pages.views_acessos as views_acessos

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Views de home
    path('', views_home.home, name='home'),  
    # Views de Slots
    path('slots', views_slots.slots, name='slots'),  
    path('atualizar_slots', views_slots.atualizar_slots, name='atualizar_slots'),  
    path('consultar_slots', views_slots.consultar_slots, name='consultar_slots'),  
    # Views de servidores
    path('servidores', views_servidores.servidores, name='servidores'),
    path('atualizar_status_servidores/', views_servidores.atualizar_status_servidores, name='atualizar_status_servidores'),
    path('reiniciar_servico/', views_servidores.reiniciar_servico, name='reiniciar_servico'),
    path('atualizar_conexoes/', views_servidores.atualizar_conexoes, name='atualizar_conexoes'),
    path('atualizar_conexao/', views_servidores.atualizar_conexao, name='atualizar_conexao'),
    path('obter_detalhes_servico/', views_servidores.obter_detalhes_servico, name='obter_detalhes_servico'),
    path('atualizar_todos_detalhes/', views_servidores.atualizar_todos_detalhes, name='atualizar_todos_detalhes'),
    # Views de Acessos
    path('acessos', views_acessos.acessos, name='acessos'),  
    path('atualizar_acessos', views_acessos.atualizar_acessos, name='atualizar_acessos'),  
    path('novo_servidor/', views_acessos.novo_servidor, name='novo_servidor'),
    path('ativa_slot/', views_acessos.ativa_slot, name='ativa_slot'),
    path('deletar_servidor/', views_acessos.deletar_servidor, name='deletar_servidor'),
    # Views de kafka
    path('gerenciador_kafka', views_kafka.gerenciador_kafka, name='gerenciador_kafka'),
    path('get_ambiente/', views_kafka.get_ambiente, name='get_ambiente'),
    path('actions/', views_kafka.actions, name='actions'),
    path('recreate_connector/', views_kafka.recreate_connector, name='recriar_conectores'),
    # Views de jira
    path('jira/', views_jira.jira, name='jira'),
    path('show_files/', views_jira.show_files, name='show_files'),
    path('create_folder/', views_jira.create_folder, name='create_folder'),
    path('reorganize/', views_jira.reorganize, name='reorganize'),
    # Views de expurgo
    path('expurgo/', views_expurgo.expurgo, name='expurgo'),
    path('validar_tabelas/', views_expurgo.validar_tabelas, name='validar_tabelas'),
    path('atualizar_tabelas/', views_expurgo.atualizar_tabelas, name='atualizar_tabelas'),
    path('deletar_selecionadas/', views_expurgo.deletar_selecionadas, name='deletar_selecionadas'),
]

    