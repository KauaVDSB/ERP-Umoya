from flask import flash, jsonify
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DecimalField,
    FileField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional

# from .models import Entidade, Item
from app.services.supabase_service import (
    upload_file_to_supabase_and_get_url,
    delete_file_from_supabase,
)
from app.blueprints.inventory.inventory_services import (
    create_item,
    update_item,
    delete_item,
)


class ItemForm(FlaskForm):
    entidade = SelectField(
        "Entidade", coerce=int, choices=[], validators=[DataRequired()]
    )

    categorias = SelectMultipleField(
        "Categorias", coerce=int, choices=[], validators=[Optional()]
    )

    codigo = StringField("Código", validators=[DataRequired(), Length(max=20)])
    codigo_barra = StringField("Código de barra", validators=[Length(max=50)])

    nome = StringField(
        "Nome do Produto", validators=[DataRequired(), Length(max=100)]
    )
    descricao = StringField(
        "Descrição do Produto", validators=[Optional(), Length(max=255)]
    )
    imagem = FileField("Imagem do Produto")

    unidade = SelectField(
        "Unidade",
        choices=[("UN", "Un"), ("CX", "Caixa"), ("M2", "Metro²")],
        validators=[DataRequired()],
    )
    # Campos numéricos opcionais com default predefinido
    comprimento = DecimalField(
        "Comprimento (m)",
        places=3,
        default=0,
        validators=[Optional(), NumberRange(min=0)],
    )
    largura = DecimalField(
        "Largura (m)",
        places=3,
        default=0,
        validators=[Optional(), NumberRange(min=0)],
    )
    profundidade = DecimalField(
        "Profundidade (m)",
        places=3,
        default=0,
        validators=[Optional(), NumberRange(min=0)],
    )
    submit = SubmitField("Salvar")

    def save(self):
        """
        Coleta dados do form, faz upload de imagem e cria o item via service.
        """
        data = {
            'entidade_id': self.entidade.data,
            'categoria_ids': self.categorias.data or None,
            'codigo': self.codigo.data,
            'codigo_barra': self.codigo_barra.data,
            'nome': self.nome.data,
            'descricao': self.descricao.data,
            'unidade': self.unidade.data,
            'comprimento': self.comprimento.data,
            'largura': self.largura.data,
            'profundidade': self.profundidade.data,
        }
        # Upload de imagem se houver
        image_url = upload_file_to_supabase_and_get_url(
            self.imagem.data, 'produtos'
        )
        if image_url:
            data['imagem_url'] = image_url

        # Cria o item no DB via serviço
        try:
            create_item(data)
            flash("Item criado com sucesso!", "success")
        except Exception as e:
            flash(f"Falha ao criar item: {e}", "danger")
            raise

    def update(self, item):
        """
        Atualiza campos do item e substitui imagem se necessário.
        """
        data = {
            'entidade_id': self.entidade.data,
            'categoria_ids': self.categorias.data or None,
            'codigo': self.codigo.data,
            'codigo_barra': self.codigo_barra.data,
            'nome': self.nome.data,
            'descricao': self.descricao.data,
            'unidade': self.unidade.data,
            'comprimento': self.comprimento.data,
            'largura': self.largura.data,
            'profundidade': self.profundidade.data,
        }

        # Troca de imagem
        if self.imagem.data and self.imagem.data.filename:
            if item.imagem_url:
                old_key = item.imagem_url.rsplit('/', 1)[-1]
                delete_file_from_supabase('produtos', old_key)
            new_url = upload_file_to_supabase_and_get_url(
                self.imagem.data, 'produtos'
            )
            if new_url:
                data['imagem_url'] = new_url

        # Atualiza o item via serviço
        try:
            update_item(item, data)
            flash("Item atualizado com sucesso!", "success")
        except Exception as e:
            flash(f"Falha ao atualizar item: {e}", "danger")
            raise

    def delete(self, item):
        """
        Remove o item e sua imagem do Supabase.
        """
        if item.imagem_url:
            key = item.imagem_url.rsplit('/', 1)[-1]
            delete_file_from_supabase('produtos', key)

        try:
            delete_item(item)
            return jsonify({"success": True}), 200
        except Exception as e:
            flash(f"Falha ao deletar item: {e}", "danger")
            return jsonify({"success": False, "error": str(e)}), 500
