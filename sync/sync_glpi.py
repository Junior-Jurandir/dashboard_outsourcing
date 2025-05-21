import requests
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Chamado, db
import logging
from typing import Dict, List, Any, Optional
from config import app_config, app_active

config = app_config[app_active]

# Configurações
GLPI_URL: str = config.GLPI_URL
APP_TOKEN: str = config.APP_TOKEN
USER_TOKEN: str = config.USER_TOKEN
DB_URL: str = config.SQLALCHEMY_DATABASE_URI

# Logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Banco
engine = create_engine(DB_URL)
db.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def iniciar_sessao() -> Dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "App-Token": APP_TOKEN
    }
    body = {
        "user_token": USER_TOKEN
    }
    try:
        r = requests.post(f"{GLPI_URL}/initSession", headers=headers, json=body, verify=False)
        r.raise_for_status()
        sessao = r.json()
        headers["Session-Token"] = sessao["session_token"]
        logger.info("Sessão iniciada com sucesso.")
        return headers
    except requests.RequestException as e:
        logger.error(f"Erro ao iniciar sessão na API GLPI: {e}")
        raise

def encerrar_sessao(headers: Dict[str, str]) -> None:
    try:
        requests.get(f"{GLPI_URL}/killSession", headers=headers, verify=False)
        logger.info("Sessão encerrada com sucesso.")
    except requests.RequestException as e:
        logger.error(f"Erro ao encerrar sessão na API GLPI: {e}")

def obter_ultima_data(session: Session) -> str:
    ultimo: Optional[Chamado] = session.query(Chamado).order_by(Chamado.date_mod.desc()).first()
    if ultimo and ultimo.date_mod:
        return ultimo.date_mod.strftime("%Y-%m-%d %H:%M:%S")
    return "2025-01-01 00:00:00"

def buscar_chamados(headers: Dict[str, str], data_mod: str) -> List[Dict[str, Any]]:
    params = {
        "criteria[0][field]": "15",  # date_mod
        "criteria[0][searchtype]": "morethan",
        "criteria[0][value]": data_mod
    }
    try:
        response = requests.get(f"{GLPI_URL}/search/Ticket", headers=headers, params=params, verify=False)
        response.raise_for_status()
        chamados = response.json().get("data", [])
        logger.info(f"{len(chamados)} chamados encontrados após {data_mod}.")
        return chamados
    except requests.RequestException as e:
        logger.error(f"Erro ao buscar chamados na API GLPI: {e}")
        return []

def obter_detalhes_chamado(headers: Dict[str, str], chamado_id: int) -> Dict[str, Any]:
    try:
        r = requests.get(f"{GLPI_URL}/Ticket/{chamado_id}", headers=headers, verify=False)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        logger.error(f"Erro ao obter detalhes do chamado {chamado_id}: {e}")
        return {}

def obter_grupo_tecnico(headers: Dict[str, str], chamado_id: int) -> Optional[int]:
    url = f"{GLPI_URL}/Ticket/{chamado_id}/Group_Ticket/"
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        grupos = response.json()
        for grupo in grupos:
            if grupo.get("type") == 2:  # Grupo técnico atribuído
                return grupo.get("groups_id")
        return None
    except requests.RequestException as e:
        logger.warning(f"Erro ao obter grupo técnico do chamado {chamado_id}: {e}")
        return None

def salvar_chamados(session: Session, headers: Dict[str, str], chamados: List[Dict[str, Any]]) -> None:
    for item in chamados:
        try:
            chamado_id = int(item["id"])
            dados = obter_detalhes_chamado(headers, chamado_id)
            if not dados:
                continue

            grupo_tecnico_id = obter_grupo_tecnico(headers, chamado_id)

            chamado = session.get(Chamado, chamado_id)
            if not chamado:
                chamado = Chamado(id=chamado_id)

            chamado.Titulo = dados.get("name")
            chamado.Descricao = dados.get("content")
            chamado.Status = dados.get("status")
            chamado.Prioridade = dados.get("priority")
            chamado.ID_categoria_itil = dados.get("itilcategories_id")
            chamado.ID_grupo_tecnico = grupo_tecnico_id
            chamado.ID_requerente = dados.get("users_id_recipient")
            chamado.DT_criacao = datetime.fromisoformat(dados["date"]) if dados.get("date") else None
            chamado.DT_mod = datetime.fromisoformat(dados["date_mod"]) if dados.get("date_mod") else None
            chamado.DT_sync = datetime.utcnow()

            session.merge(chamado)
        except Exception as e:
            logger.error(f"Erro ao salvar chamado {item.get('id')}: {e}")
    try:
        session.commit()
        logger.info("Chamados salvos com sucesso no banco de dados.")
    except Exception as e:
        logger.error(f"Erro ao commitar sessão no banco de dados: {e}")
        session.rollback()

def sincronizar() -> None:
    try:
        headers = iniciar_sessao()
    except Exception:
        logger.error("Falha ao iniciar sessão. Sincronização abortada.")
        return

    with SessionLocal() as db:
        try:
            ultima_data = obter_ultima_data(db)
            logger.info(f"Sincronizando chamados modificados após: {ultima_data}")
            chamados = buscar_chamados(headers, ultima_data)
            salvar_chamados(db, headers, chamados)
        except Exception as e:
            logger.error(f"Erro durante a sincronização: {e}")
        finally:
            encerrar_sessao(headers)
            logger.info("Sincronização concluída.")

if __name__ == "__main__":
    sincronizar()
