from .route_usuario import usuario_bp
# from .route_adm import adm_bp
from .route_hotel import hotel_bp
from .route_reservas import reservas_bp
from .routes_gerais import gerais_bp
from .route_quartos import quarto_bp
from .route_pontos import ponto_bp


def register_blueprints(app):
    app.register_blueprint(usuario_bp)
    # app.register_blueprint(adm_bp)
    app.register_blueprint(hotel_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(gerais_bp)
    app.register_blueprint(quarto_bp)
    app.register_blueprint(ponto_bp)
