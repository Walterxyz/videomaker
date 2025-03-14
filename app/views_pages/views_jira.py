import shutil, os, time
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render


@login_required
def jira(request):
    path = "//funcional.local/arquivos/Banco de Dados/JIRA/"
    folders = []
    try:
        for folder in os.listdir(path):
            folder_path = os.path.join(path, folder)
            if os.path.isdir(folder_path):
                folder_modification_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getmtime(folder_path)))
                folders.append({'folder_name': folder, 'modification_time': folder_modification_time})
    except:
        folders.append({'folder_name': 'Caminho de rede Inacessivel', 'modification_time': ''})
    return render(request, 'jira.html', {'folders': folders})


@login_required
def show_files(request):
    if request.method == 'POST':
        folder = request.POST.get('folder')
        path = "//funcional.local/arquivos/Banco de Dados/JIRA/" + folder
        path = os.path.realpath(path)
        os.startfile(path)
    return JsonResponse({'status': True})

@login_required
def create_folder(request):
    if request.method == 'POST':
        folder = request.POST.get('folder')
        path = "//funcional.local/arquivos/Banco de Dados/JIRA/" + folder
        try:
            os.mkdir(path)
        except:
            return JsonResponse({'status': False})
    return JsonResponse({'status': True})

@login_required
def reorganize(request):
    return JsonResponse({'status': False})
    # source_path = "//funcional.local/arquivos/Banco de Dados/JIRA/"
    # target_path = "//funcional.local/arquivos/Banco de Dados/JIRA/JIRA_"

    # for folder in os.listdir(source_path):
    #     folder_path = os.path.join(source_path, folder)
    #     if os.path.isdir(folder_path) and 'JIRA' not in folder and '00.' not in folder:
    #         folder_modification_time = datetime.fromtimestamp(os.path.getmtime(folder_path)).year
    #         target_folder = target_path + str(folder_modification_time)
    #         os.makedirs(target_folder, exist_ok=True)
    #         print(folder_path, target_folder)
    #         shutil.move(folder_path, target_folder)
    #         return JsonResponse({'status': True})