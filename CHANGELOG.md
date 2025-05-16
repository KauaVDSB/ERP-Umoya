# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.
Este projeto segue [Semantic Versioning](https://semver.org/).

## \[0.1.0] - 2025-05-15

### Added

* Estrutura inicial de blueprint `inventory` com CRUD completo de itens, incluindo upload e gerenciamento de imagens no Supabase Storage.
* Modelos SQLAlchemy para `Entidade`, `Categoria` (incluindo relação muitos-para-muitos `Item`–`Categoria`) e `Item`.
* Formulários Flask-WTF (`ItemForm`) com validações, campos de imagem e suporte a múltiplas categorias via SelectMultipleField + Select2.
* Serviços modulados em `src/app/services`:

  * `supabase_service`: upload, geração de nome único e deleção de arquivos.
  * `file_service`: manipulação de arquivos temporários e timestamped filenames.
  * `inventory_service`: funções CRUD para `Item`.
* Templates Jinja2 para listagem, detalhe/edição e *partials* de formulários.
* Implementação de CI no GitHub Actions com:

  * Black (format check), Flake8, Pylint e Pytest (+ cobertura).
* Configurações de lint e formatação:

  * `setup.cfg`: Flask8, pytest.
  * `pyproject.toml`: Black.
  * `.pylintrc`: Pylint.
