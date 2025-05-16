"""
Módulo de serviço com funções reutilizáveis
para interagir com Supabase.
"""

from typing import Optional
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from werkzeug.utils import secure_filename
from app import supabase, SUPABASE_URL


def generate_unique_filename(
    filename: str, timezone_key: str = "America/Recife"
) -> str:
    """
    Gera nome único baseado timestamp localizado e nome seguro

    Args:
        filename (str): Nome original do arquivo.
        timezone_key (str): Timezone para o timestamp (padrão: Recife)
    """
    try:
        tz = ZoneInfo(timezone_key)
        now = datetime.now(tz)
    except ZoneInfoNotFoundError:
        now = datetime.now(timezone.utc)

    timestamp = now.strftime("%Y%m%d%H%M%S%f")
    safe_name = secure_filename(filename)
    return f"{timestamp}_{safe_name}"


def upload_file_to_supabase_and_get_url(
    file_data, bucket: str
) -> Optional[str]:
    """
    Recebe arquivo via FileField, gera nome único, envia ao Supabase
    e retorna URL pública - ou None, caso não exista arquivo.

    Args:
        file_data: Objeto FileStorage do Flask-WTF.
        bucket (str): Nome do bucket no Supabase Storage.
    """
    if not file_data or not file_data.filename:
        return None

    unique_name = generate_unique_filename(file_data.filename)
    path = f"{bucket}/{unique_name}"
    content = file_data.read()

    supabase.storage.from_(bucket).upload(path, content)

    return f"{SUPABASE_URL}/storage/v1/object/public/{path}"


def delete_file_from_supabase(bucket: str, key: str) -> bool:
    """
    Deleta arquivo do Supabase Storage.

    Args:
        bucket (str): Nome do bucket do Supabase Storage.
        key (str): Nome relativo do arquivo (após `bucket/`)
    """

    # pylint: disable=broad-exception-caught
    try:
        supabase.storage.from_(bucket).remove([f"{bucket}/{key}"])
        return True
    except Exception as e:
        # Log de erro
        print(f"[SupabaseService] Erro ao deletar arquivo {key}: {e}")
        return False
