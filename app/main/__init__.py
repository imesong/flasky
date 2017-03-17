from flask import Blueprint
from . import views, errors
from ..models import Permissions

main = Blueprint('main', __name__)


@main.app_context_processor
def inject_permission():
    return dict(Permission=Permissions)