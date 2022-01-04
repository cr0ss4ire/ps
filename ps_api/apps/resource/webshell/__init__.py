from apps.resource.webshell import webshell


def register_blueprint(app):
    app.register_blueprint(webshell.blueprint, url_prefix='/resource/webshell')
