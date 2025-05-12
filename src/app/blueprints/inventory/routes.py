from flask import render_template, redirect, url_for, flash, request
from . import bp
from .forms import ItemForm
from .models import Item, Entidade




@bp.route("/items")
def list_items():
    entidade_id = request.args.get("entidade", type=int)
    items = Item.query.filter_by(entidade_id=entidade_id) if entidade_id else Item.query
    return render_template("list.html", items=items.all())


@bp.route("/item/new", methods=["GET", "POST"])
def new_item():
    form = ItemForm()
    form.entidade.choices = [(e.id,e.nome) for e in Entidade.query.all()]

    print("Método:", request.method)
    print("Form data:", form.data)
    print("Form errors:", form.errors)

    if form.validate_on_submit():
        form.save()
        print("Item criado com sucesso!", "success")  # Trocar por jsonify para aplicar alerts com js
        return redirect("/inventory/items")
    return render_template("detail.html", form=form)


@bp.route("/item/<int:id>/edit", methods=["GET", "POST"])
def edit_item(id):
    item = Item.query.get_or_404(id)
    form = ItemForm(obj=item)
    form.entidade.choices = [(e.id,e.nome) for e in Entidade.query.all()]
    
    if form.validate_on_submit():
        form.update(item)
        flash("Item atualizado com sucesso!", "success")
        return redirect(url_for("inventory.list_items", entidade=item.entidade_id))
    return render_template("detail.html", form=form, item=item)


@bp.route("/item/<int:id>/delete", methods=["POST"])
def delete_item(id):
    item = Item.query.get_or_404(id)
    form = ItemForm()

    return form.delete(item)

