from apps.account.models import User
from flask import Blueprint
from libs.decorators import require_permission
from libs.tools import json_response


blueprint = Blueprint(__name__, __name__)


@blueprint.route('/', methods=['GET'])
@require_permission('home_view')
def get():
    user_total = User.query.count()
    host_total = 66
    job_total = 66
    app_total = 66

    data = {'user_total': user_total,
            'host_total': host_total,
            'job_total': job_total,
            'app_total': app_total,
            }
    return json_response(data)
