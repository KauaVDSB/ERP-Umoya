"""
Módulo de serviço para manipulação de arquivos.
Contém funções utilitárias para trabalhar com
diretórios temporários e limpeza.
"""

import os
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from werkzeug.utils import secure_filename


def generate_timestamped_filename(
    filename: str, timezone: str = "America/Recife"
) -> str:
    """
    Gera um nome de arquivo único baseado em timestamp com fuso horário.

    Args:
        filename (str): Nome original do arquivo.
        timezone (str): Identificador tzdata (ex: 'America/Recife').

    Returns:
        str: Nome composto por timestamp + nome seguro.
    """
    # Captura data-hora local com timezone
    tzinfo = ZoneInfo(timezone)
    now = datetime.now(tzinfo)
    # Formata timestamp (ano, mês, dia, hora, min, seg, microssegundos)
    ts = now.strftime("%Y%m%d%H%M%S%f")
    # Sanitiza nome original
    safe_name = secure_filename(filename)
    return f"{ts}_{safe_name}"


def save_temporary_file(file_data, tmp_folder: str) -> Optional[str]:
    """
    Salva um FileStorage em disco dentro de 'tmp_folder' e retorna o path.

    Args:
        file_data: Instância FileStorage do Flask-WTF.
        tmp_folder (str): Caminho do diretório para salvamento.

    Returns:
        str | None: Path completo do arquivo, ou None se não houver arquivo.
    """
    if not file_data or not file_data.filename:
        return None

    # Gera nome timestamped
    filename = generate_timestamped_filename(file_data.filename)
    # Caminho completo
    full_path = os.path.join(tmp_folder, filename)

    # Garante que a pasta existe
    os.makedirs(tmp_folder, exist_ok=True)

    # Salva o arquivo em disco
    file_data.save(full_path)
    return full_path


def cleanup_temp_folder(tmp_folder: str, max_age_seconds: int = 3600):
    """
    Remove arquivos em 'tmp_folder' mais antigos que 'max_age_seconds'.

    Args:
        tmp_folder (str): Diretório a limpar.
        max_age_seconds (int): Idade máxima em segundos antes de deletar.
    """
    now = datetime.now().timestamp()
    for fname in os.listdir(tmp_folder):
        path = os.path.join(tmp_folder, fname)
        # pylint: disable=broad-exception-caught
        try:
            # Verifica idade do arquivo
            if (
                os.path.isfile(path)
                and now - os.path.getmtime(path) > max_age_seconds
            ):
                os.remove(path)
        except Exception:
            # Pula arquivos que não podem ser removidos
            pass
