import schedule
import time
from sync_glpi import sincronizar

def iniciar_agendador():
    schedule.every(5).minutes.do(sincronizar)
    print("⏳ Job de sincronização agendado a cada 5 minutos.")

    while True:
        schedule.run_pending()
        time.sleep(1)
