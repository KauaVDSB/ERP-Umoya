from flask import Blueprint, jsonify
from app.models import Cliente

cliente_bp = Blueprint("cliente", __name__, url_prefix="/clientes")


@cliente_bp.route('', methods=["GET"])
def listar_clientes():
    """
    GET /clientes
    retorna uma listagem de todos os clientes em JSON.
    """

    clientes = Cliente.query.all()

    resultado = [
        {
            "id": c.id,
            "nome": c.nome,
            "email": c.email,
            "telefone": c.telefone,
            "endereco": c.endereco,
        }
        for c in clientes
    ]

    return jsonify(resultado), 200
