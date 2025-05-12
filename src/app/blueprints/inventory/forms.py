from time import time
from werkzeug.utils import secure_filename
from flask import flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

from .models import Entidade, Item


from app import db, SUPABASE_URL, supabase


class ItemForm(FlaskForm):
    entidade = SelectField("Entidade", coerce=int, validators=[DataRequired()])

    codigo = StringField("Código", validators=[DataRequired(), Length(max=20)])
    codigo_barra = StringField("Código de barra", validators=[Length(max=50)])

    nome = StringField("Nome do Produto", validators=[DataRequired(), Length(max=100)])
    descricao = StringField("Descrição do Produto", validators=[DataRequired(), Length(max=255)])
    imagem = FileField("Imagem do Produto")

    unidade = SelectField(
        "Unidade", choices=[("UN", "Un"), ("CX", "Caixa"), ("M2", "Metro²")], 
        validators=[DataRequired()]
    )
    comprimento = DecimalField("Comprimento", places=3, validators=[NumberRange(min=0)])
    largura = DecimalField("Largura", places=3, validators=[NumberRange(min=0)])
    profundidade = DecimalField("Profundidade", places=3, validators=[NumberRange(min=0)])
    submit = SubmitField("Salvar")

    
    @staticmethod
    def generate_unique_filename(filename):
        """Gera um nome único para o arquivo."""
        return f"{str(db.func.now())}_{secure_filename(filename)}"

    def get_imagem_url(self):
        imagem = self.imagem.data
        imagem_url = None

        if imagem and imagem.filename:
            unique_filename = self.generate_unique_filename(imagem.filename)

            # Envia para o Supabase Storage
            caminho_arquivo = f"produtos/{unique_filename}"
            imagem_bytes = imagem.read()

            # Upload
            supabase.storage.from_("produtos").upload(
                caminho_arquivo, imagem_bytes
            )  # VARIAVEL DE AMBIENTE

            # Gera url pública para a imagem
            imagem_url = f"{SUPABASE_URL}/storage/v1/object/public/produtos/{unique_filename}"  # VARIAVEL DE AMBIENTE
        return imagem_url



    def save(self):
        entidade_id = self.entidade.data
        imagem_url = self.get_imagem_url()
        
        item = Item(
            entidade=Entidade.query.get(entidade_id),
            codigo=self.codigo.data,
            codigo_barra=self.codigo_barra.data,
            nome=self.nome.data,
            descricao=self.descricao.data,
            imagem_url=imagem_url,
            unidade=self.unidade.data,
            comprimento=self.comprimento.data,
            largura=self.largura.data,
            profundidade=self.profundidade.data,
        )
        print("ta rodando")


        db.session.add(item)
        db.session.commit()


    def update(self, item):
        try:
            for field in ItemForm(obj=item):
                if field.name != "imagem":
                    setattr(item, field.name, field.data)
                if self.imagem_url.data and self.imagem.data_url.filename:
                    if item.imagem_url:
                        try:
                            supabase.storage.from_("produtos").remove(
                                ["produtos/" + item.imagem.split("/")[-1]]
                            )
                        except Exception as e:
                            flash(f"Erro ao excluir arquivo de imagem no Supabase: {e}")
                    
                    imagem_url = self.get_imagem_url()
                    item.imagem_url = imagem_url

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar item: {e}")

            
    def delete(self, item):
        if item.imagem_url:
            try:
                supabase.storage.from_("produtos").remove(
                    ["produtos/" + item.imagem_url.split("/")[-1]]
                )  # VARIAVEL DE AMBIENTE
            except Exception as e:
                flash(f"Erro ao excluir arquivo de imagem no Supabase: {e}")

        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"success": True}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "error": str(e)}), 500
