import multiprocessing
import time
import signal
import sys
from config import app_config, app_active
from app import create_app
from sync.job_runner import iniciar_agendador

config = app_config[app_active]

def iniciar_flask():
    create_app(config)
    config.APP.run(host=config.IP_HOST, port=config.PORT_HOST)

def iniciar_job():
    iniciar_agendador()

if __name__ == '__main__':
    flask_proc = multiprocessing.Process(target=iniciar_flask)
    job_proc = multiprocessing.Process(target=iniciar_job)

    flask_proc.start()
    job_proc.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Encerrando processos...")
        flask_proc.terminate()
        job_proc.terminate()
        flask_proc.join()
        job_proc.join()
        print("✅ Encerrado com sucesso.")
        sys.exit(0)