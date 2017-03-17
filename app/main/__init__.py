from flask import Blueprint
# 这个必需放在第二行，不然编译不通过
main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permissions



@main.app_context_processor
def inject_permission():
    return dict(Permission=Permissions)