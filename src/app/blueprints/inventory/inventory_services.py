"""
Serviços específicos para o domínio de inventário: operações CRUD de Item e Entidade.
"""

from app.extensions import db
from app.blueprints.inventory.models import Item, Entidade, Categoria


def create_item(data: dict) -> Item:
    """
    Cria um novo Item com os dados fornecidos.

    Args:
        data (dict): Dicionário contendo campos de Item, incluindo 'entidade_id', 'categoria_id' e demais.

    Returns:
        Item: Instância persistida do Item criado.
    """
    # Converte IDs em instâncias ORM
    entidade = Entidade.query.get(data.pop('entidade_id'))
    categoria_ids = data.pop('categoria_ids', [])
    item = Item(entidade=entidade, **data)

    item.categorias = (
        Categoria.query.filter(Categoria.id.in_(categoria_ids)).all()
        if categoria_ids
        else []
    )

    try:
        db.session.add(item)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return item


def update_item(item: Item, data: dict) -> Item:
    """
    Atualiza um Item existente com novos dados.

    Args:
        item (Item): Instância do Item a ser atualizada.
        data (dict): Novos valores para atributos.

    Returns:
        Item: Instância atualizada e persistida.
    """
    # Converte e remove IDs do dict data
    if 'entidade_id' in data:
        item.entidade = Entidade.query.get(data.pop('entidade_id'))
    if 'categoria_ids' in data:
        ids = data.pop("categoria_ids")
        if ids:
            item.categorias = Categoria.query.filter(
                Categoria.id.in_(ids)
            ).all()

    # Atribui campos dinamicamente
    for key, value in data.items():
        setattr(item, key, value)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return item


def delete_item(item: Item) -> None:
    """
    Remove um Item do banco.

    Args:
        item (Item): Instância a ser deletada.

    Raises:
        Exception: Se a deleção falhar.
    """
    try:
        db.session.delete(item)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
