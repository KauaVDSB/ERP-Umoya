from flask import Blueprint

bp = Blueprint(
    "inventory",
    __name__,
    url_prefix="/inventory",
    template_folder="templates/inventory",
    static_folder="static",
)

from . import routes  # noqa: F401,E402
