from apps.task import task


def register_blueprint(app):
    app.register_blueprint(task.blueprint, url_prefix='/task')
