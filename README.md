[![CI](https://github.com/KauaVDSB/ERP-Umoya/actions/workflows/ci.yml/badge.svg)](https://github.com/KauaVDSB/ERP-Umoya/actions/workflows/ci.yml) [![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/KauaVDSB/ERP-Umoya/releases/tag/v0.1.0) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# ERP-Umoya

**ERP-Umoya** é um sistema modular de gestão empresarial, construído em Python com Flask e Supabase para Storage.

---

## 📑 Sumário

* [Funcionalidades](#-funcionalidades)
* [Estrutura do Projeto](#-estrutura-do-projeto)
* [Instalação & Configuração](#-instalação--configuração)
* [Variáveis de Ambiente](#-variáveis-de-ambiente)
* [Executando a Aplicação](#-executando-a-aplicação)
* [Testes Automatizados](#-testes-automatizados)
* [Changelog](#-changelog)
* [Contribuindo](#-contribuindo)
* [Autor](#-autor)
* [License](#-license)

---

## 🚀 Funcionalidades

* **Estrutura Modular**: Flask Blueprints para separação de responsabilidades.
* **Modelagem Relacional**: SQLAlchemy com migrações Alembic.
* **CRUD de Inventário**: Itens, Entidades, Categorias (muitos-para-muitos), imagens no Supabase Storage.
* **Upload de Arquivos**: Suporte a uploads seguros e limpeza de temporários.
* **Formulários Robustos**: Flask-WTF com validações e feedback de erros.
* **Testes**: `pytest` para health-check, clientes e inventário.
* **Segurança**: CSRF nativo, configuração de limites de upload.

---

## 📁 Estrutura do Projeto

```bash
.
├── .github/workflows    # CI & lint
├── migrations           # Alembic migrations
├── src/app              # Package principal
│   ├── blueprints       # Módulos da aplicação (auth, cliente, inventory...)
│   ├── services         # Lógica de negócio e integrações
│   ├── extensions.py    # Instâncias de db, migrate
│   ├── config.py        # Configurações por ambiente
│   └── wsgi.py          # Entry-point do Flask
├── tests                # Testes automatizados
├── .env.example         # Exemplo de variáveis de ambiente
├── .flaskenv            # Configuração Flask CLI
├── README.md            # Documentação do projeto
├── CHANGELOG.md         # Histórico de versões
├── LICENSE              # Licença MIT
└── requirements.txt     # Dependências Python
```

---

## ⚙️ Instalação & Configuração

1. **Clone o repositório**

   ```bash
   git clone https://github.com/KauaVDSB/ERP-Umoya.git
   cd ERP-Umoya
   ```
2. **Configurar virtualenv**

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # macOS/Linux
   .venv\Scripts\activate       # Windows
   ```
3. **Instalar dependências**

   ```bash
   pip install -r requirements.txt
   ```
4. **Variáveis de ambiente**

   * Copie `.env.example` para `.env` e defina:

     * `DATABASE_URL`
     * `SUPABASE_URL`
     * `SUPABASE_KEY`
     * `SECRET_KEY`
     * `FLASK_ENV`
     * `MAX_CONTENT_LENGTH`
5. **Aplicar migrações**

   ```bash
   flask db upgrade
   ```

---

## 🌐 Variáveis de Ambiente

| Variável             | Descrição                                      |
| -------------------- | ---------------------------------------------- |
| DATABASE\_URL        | URI de conexão com o banco (Postgres/Supabase) |
| SUPABASE\_URL        | URL do projeto Supabase                        |
| SUPABASE\_KEY        | Chave API do Supabase                          |
| SECRET\_KEY          | Chave secreta do Flask (CSRF)                  |
| FLASK\_ENV           | `development` ou `production`                  |
| MAX\_CONTENT\_LENGTH | Tamanho máximo de upload (em bytes)            |

---

## ▶️ Executando a Aplicação

```bash
flask run
```

**Acesse** `http://127.0.0.1:5000/inventory/items`

---

## 🧪 Testes Automatizados

```bash
pytest -q
```

---

## 📜 Changelog

Veja [CHANGELOG.md](CHANGELOG.md) para histórico de versões.

---

## 🤝 Contribuindo

Pull requests são bem-vindos para melhorias e correções!

---

## ✉️ Autor

**KauaVDSB**

* GitHub: [https://github.com/KauaVDSB](https://github.com/KauaVDSB)
* LinkedIn: [https://linkedin.com/in/kaua-vdsb](https://linkedin.com/in/kaua-vdsb)

---

## 📄 License

Distribuído sob a Licença MIT. Veja [LICENSE](LICENSE).
