from .route_usuario import usuario_bp
from .route_adm import adm_bp
from .route_empresa import empresa_bp
from .route_reservas import reservas_bp
from .routes_gerais import gerais_bp

def register_blueprints(app):
    app.register_blueprint(usuario_bp)
    app.register_blueprint(adm_bp)
    app.register_blueprint(empresa_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(gerais_bp)