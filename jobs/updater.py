from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import atualizar_conexoes
from app.tasks import atualiza_status_slot


def att_servers(servers):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: atualizar_conexoes(servers), 'interval', minutes=10)
    scheduler.start()

def att_slots(servers):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: atualiza_status_slot(servers), 'interval', minutes=1)
    scheduler.start()