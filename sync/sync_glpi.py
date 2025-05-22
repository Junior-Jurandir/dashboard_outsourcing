import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Optional
from app import db
from models import Chamado
import logging
from config import app_config, app_active

config = app_config[app_active]

# Configurações
GLPI_URL: str = config.GLPI_URL
APP_TOKEN: str = config.APP_TOKEN
USER_TOKEN: str = config.USER_TOKEN
VERIFY_SSL: bool = getattr(config, "VERIFY_SSL", True)

# Logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def iniciar_sessao() -> Dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "App-Token": APP_TOKEN
    }
    body = {
        "user_token": USER_TOKEN
    }
    try:
        r = requests.post(f"{GLPI_URL}/initSession", headers=headers, json=body, verify=VERIFY_SSL)
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
        requests.get(f"{GLPI_URL}/killSession", headers=headers, verify=VERIFY_SSL)
        logger.info("Sessão encerrada com sucesso.")
    except requests.RequestException as e:
        logger.error(f"Erro ao encerrar sessão na API GLPI: {e}")

def obter_ultima_data() -> str:
    ultimo: Optional[Chamado] = db.session.query(Chamado).order_by(Chamado.DT_mod.desc()).first()
    if ultimo and ultimo.DT_mod:
        return ultimo.DT_mod.strftime("%Y-%m-%d %H:%M:%S")
    return "2025-01-01 00:00:00"

def buscar_chamados(headers: Dict[str, str], data_mod: str) -> List[Dict[str, Any]]:
    params = {
        "criteria[0][field]": "15",  # date_mod
        "criteria[0][searchtype]": "morethan",
        "criteria[0][value]": data_mod
    }
    try:
        response = requests.get(f"{GLPI_URL}/search/Ticket", headers=headers, params=params, verify=VERIFY_SSL)
        response.raise_for_status()
        chamados = response.json().get("data", [])
        logger.info(f"{len(chamados)} chamados encontrados após {data_mod}.")
        return chamados
    except requests.RequestException as e:
        logger.error(f"Erro ao buscar chamados na API GLPI: {e}")
        return []

def obter_detalhes_chamado(headers: Dict[str, str], chamado_id: int) -> Dict[str, Any]:
    try:
        r = requests.get(f"{GLPI_URL}/Ticket/{chamado_id}", headers=headers, verify=VERIFY_SSL)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        logger.error(f"Erro ao obter detalhes do chamado {chamado_id}: {e}")
        return {}

def obter_grupo_tecnico(headers: Dict[str, str], chamado_id: int) -> Optional[int]:
    url = f"{GLPI_URL}/Ticket/{chamado_id}/Group_Ticket/"
    try:
        response = requests.get(url, headers=headers, verify=VERIFY_SSL)
        response.raise_for_status()
        grupos = response.json()
        for grupo in grupos:
            if grupo.get("type") == 2:  # Grupo técnico atribuído
                return grupo.get("groups_id")
        return None
    except requests.RequestException as e:
        logger.warning(f"Erro ao obter grupo técnico do chamado {chamado_id}: {e}")
        return None

def processar_chamado(headers: Dict[str, str], item: Dict[str, Any]) -> Optional[Chamado]:
    try:
        chamado_id = int(item["id"])
        dados = obter_detalhes_chamado(headers, chamado_id)
        if not dados:
            return None

        grupo_tecnico_id = obter_grupo_tecnico(headers, chamado_id)

        chamado = db.session.get(Chamado, chamado_id)
        if not chamado:
            chamado = Chamado(ID=chamado_id)

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

        return chamado
    except Exception as e:
        logger.error(f"Erro ao processar chamado {item.get('id')}: {e}")
        return None

def salvar_chamados(session, headers: Dict[str, str], chamados: List[Dict[str, Any]]) -> None:
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(processar_chamado, headers, item): item for item in chamados}
        for future in as_completed(futures):
            chamado = future.result()
            if chamado:
                try:
                    session.merge(chamado)
                except Exception as e:
                    logger.error(f"Erro ao salvar chamado {chamado.ID}: {e}")
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

    session = db.session
    try:
        ultima_data = obter_ultima_data()
        logger.info(f"Sincronizando chamados modificados após: {ultima_data}")
        chamados = buscar_chamados(headers, ultima_data)
        salvar_chamados(session, headers, chamados)
    except Exception as e:
        logger.error(f"Erro durante a sincronização: {e}")
    finally:
        encerrar_sessao(headers)
        logger.info("Sincronização concluída.")

if __name__ == "__main__":
    sincronizar()
