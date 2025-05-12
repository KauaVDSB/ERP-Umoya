# ERP-Umoya

**ERP-Umoya** é um sistema modular de gestão empresarial, desenvolvido em Python com Flask. Este projeto tem como objetivo ser flexível, escalável e adaptável a diferentes cenários empresariais.

---

## **Funcionalidades Implementadas**
- **Configuração do projeto:**
  - Estrutura modular usando Flask com Blueprints.
  - Gerenciamento de banco de dados com SQLAlchemy.
  - Migrações com Alembic.
  - Variáveis de ambiente com suporte a `.flaskenv` e `.env`.

- **Modelagem de dados:**
  - Entidades principais:
    - User
    - Cliente
    - Produto
    - Pedido
    - ItemPedido
    - Estoque

- **Rotas criadas:**
  - `/health`: Health-check básico.
  - `/clientes`: Listagem de clientes (vazia ou preenchida).

- **Testes automatizados:**
  - Configuração de banco de dados SQLite em memória para testes.
  - Testes de health-check e listagem de clientes com pytest.

### **Requisitos**
- **Dependências principais:**
  - Python 3.9
  - Flask
  - SQLAlchemy
  - Alembic
  - pytest
  - pytest-flask

### **Instalação**
1. Clone o repositório:
   ```bash
   git clone https://github.com/KauaVDSB/ERP-Umoya.git
   cd ERP-Umoya
   ```

2. Configure o ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` baseado em `.env.example`.
   - Certifique-se de definir o `DATABASE_URL` corretamente.

5. Inicialize o banco de dados:
   ```bash
   flask db upgrade
   ```

6. Execute o servidor:
   ```bash
   flask run
   ```

7. (Opcional) Rode os testes:
   ```bash
   pytest -q
   ```

### **Próximos Passos**
- Expandir o sistema com módulos adicionais (vendas, estoque, financeiro).
- Implementar autenticação e controle de acesso.

---

*Atualização: 11/05/2025*
