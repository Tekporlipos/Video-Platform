from flask import request
from flask_jwt_extended import jwt_required

from app import db, app
from src.models.EmailVerificationModel import EmailVerification
from src.models.UserModel import User
from src.services.AuthService import AuthService
from src.services.EmailService import EmailService
from src.services.JWTService import JWTService

auth_service = AuthService()


@app.route('/api/v1/register', methods=['POST'])
def register():
    return auth_service.register(db, User, EmailService, EmailVerification, request.json, app.logger)


@app.route('/api/v1/login', methods=['POST'])
def login():
    return auth_service.login(JWTService, User, request.json, app.logger)


@jwt_required()
@app.route('/api/v1/logout', methods=['POST'])
def logout():
    return auth_service.logout(app.logger)


@app.route('/api/v1/forgot-password', methods=['POST'])
def forgot_password():
    return auth_service.forgot_password(db, User, EmailVerification, request.json, app.logger)


@app.route('/api/v1/reset-password', methods=['POST'])
def reset_password():
    return auth_service.reset_password(db, EmailVerification, User, request.json, app.logger)


@app.route('/api/v1/verify-email/<token>', methods=['GET'])
def verify_email(token):
    return auth_service.verify_email(db, EmailVerification, User, token, app.logger)


@app.route('/api/v1/user', methods=['GET'])
def get_user():
    return auth_service.get_user(db, User, app.logger)


@app.route('/api/v1/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return auth_service.get_user_by_id(db, User, user_id, app.logger)
