def test_listar_clientes_vazio(client):
    """Lista clientes em banco vazio."""
    res = client.get("/clientes")
    assert res.status_code == 200
    assert res.json == []
