from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import jsonify

jwt = JWTManager()


class JWTService:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        jwt.init_app(app)

    def generate_jwt_token(self, user_id):
        return create_access_token(identity=user_id)

