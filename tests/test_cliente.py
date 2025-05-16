# def test_listar_clientes_vazio(client, monkeypatch):
#     """Lista clientes em banco vazio."""
#     monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory")
#     res = client.get("/clientes")
#     assert res.status_code == 200
#     assert res.json == []
