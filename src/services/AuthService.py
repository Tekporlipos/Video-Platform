import re

from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
from src.utils.responseEntity import error_response, success_response


class AuthService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthService, cls).__new__(cls)
        return cls._instance

    def register(self, db, User, EmailService, EmailVerification, data, logger=None):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Define a regex pattern for password validation
        password_pattern = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_=+{}[\]|;:,.<>?/~])[A-Za-z\d!@#$%^&*()-_=+{}[\]|;:,'
            r'.<>?/~]{8,}$')

        # Password complexity requirements
        if not re.match(password_pattern, password):
            return error_response(
                'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase '
                'letter, one digit, and one special character',
                status_code=400, logger=logger)

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return error_response('Email already exists', status_code=400, logger=logger)

        # Create new user
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        # Generate and store email verification token
        email_verification = self.generate_email_verification_token(db, EmailVerification, new_user)
        self.send_email_verification(EmailService, email_verification, email)
        return success_response('User registered successfully. Check your email for verification.', status_code=201,
                                logger=logger)

    def login(self, JWTService, User, data, logger=None):
        jwt_service = JWTService()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return error_response('Missing email or password', status_code=400, logger=logger)

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            return error_response('Invalid email or password', status_code=401, logger=logger)

        # Generate JWT token (example)
        token = jwt_service.generate_jwt_token(user.id)

        return success_response('Login successful', data={'token': token}, logger=logger)

    def logout(self, logger=None):
        # just log since we will be using JWT for auth
        return success_response('Logout successful', logger=logger)

    def forgot_password(self, db, User, PasswordResetToken, data, logger=None):
        email = data.get('email')

        if not email:
            return error_response('Missing email', status_code=400, logger=logger)

        user = User.query.filter_by(email=email).first()

        if not user:
            return error_response('User not found', status_code=404, logger=logger)

        # Generate and store password reset token
        password_reset_token = self.generate_password_reset_token(db, PasswordResetToken, user.id)

        # Send email with password reset link (example)
        self.send_password_reset_email(user.email, password_reset_token.token)

        return success_response('Password reset link sent to your email', logger=logger)

    def reset_password(self, db, PasswordResetToken, User, data, logger=None):
        email = data.get('email')
        token = data.get('token')
        new_password = data.get('new_password')

        if not email or not token or not new_password:
            return error_response('Missing email, token, or new password', status_code=400, logger=logger)

        # Verify password reset token
        password_reset_token = PasswordResetToken.query.filter_by(email=email, token=token).first()

        if not password_reset_token or password_reset_token.expires_at < datetime.utcnow():
            return error_response('Invalid or expired token', status_code=400, logger=logger)

        # Update user's password
        user = User.query.filter_by(email=email).first()
        user.password_hash = generate_password_hash(new_password)

        db.session.delete(password_reset_token)
        db.session.commit()

        return success_response('Password reset successfully', logger=logger)

    def generate_email_verification_token(self, db, EmailVerification, user):
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=1)

        email_verification = EmailVerification(
            user_id=user.id,  # Use user.id instead of user
            token=token,
            expires_at=expires_at
        )

        db.session.add(email_verification)
        db.session.commit()

        return email_verification

    def verify_email(self, db, EmailVerification, User, token, logger=None):
        # Verify email verification token and update user's email verified status
        email_verification = EmailVerification.query.filter_by(token=token).first()

        if not email_verification or email_verification.expires_at < datetime.utcnow():
            return error_response('Invalid or expired verification token', status_code=400, logger=logger)

        user = User.query.get(email_verification.user_id)
        if not user:
            return error_response('User not found', status_code=404, logger=logger)

        user.email_verified = True  # Assuming you have an 'email_verified' field in your User model
        db.session.delete(email_verification)
        db.session.commit()

        return success_response('Email verified successfully', logger=logger)

    def generate_password_reset_token(self, db, PasswordResetToken, user_email):
        # Implement password reset token generation logic (example)
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=24)

        password_reset_token = PasswordResetToken(
            email=user_email,
            token=token,
            expires_at=expires_at
        )

        db.session.add(password_reset_token)
        db.session.commit()

        return password_reset_token

    def get_user_by_id(self, db, User, user_id, logger=None):
        try:
            user = db.session.query(User).get_or_404(user_id)

            if not user:
                return error_response('User not found', status_code=404, logger=logger)
            return success_response('User retrieved successfully', user.to_json(), logger=logger)

        except Exception as e:
            return error_response(str(e), logger=logger, logger_type="error")

    @jwt_required(optional=True)
    def get_user(self, db, User, logger=None):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return error_response('Authorization header is missing or invalid', status_code=401, logger=logger)
        try:
            user = db.session.query(User).get_or_404(current_user_id)
            if not user:
                return error_response('UnAuthorize access', status_code=401, logger=logger)
            return success_response('User retrieved successfully', user.to_json(), logger=logger)

        except Exception as e:
            return error_response(str(e), logger=logger, logger_type="error")

    def send_password_reset_email(self, EmailService, email, token):
        email_services = EmailService()
        # Construct the body of the email
        body = f"""
        <p>Hello,</p>
        <p>You have requested to reset your password. Please click the link below to reset your password:</p>
        <p>{token}</p>
        <p>If you did not request this reset, please ignore this email.</p>
        <p>Thank you.</p>
        """
        email_services.send_email(email, "Password Reset Request", body)

    def send_email_verification(self, EmailService, email_verification, email):
        email_services = EmailService()

        # Construct the body of the email
        body = f"""
        <p>Hello,</p>
        <p>Thank you for registering with us. Please click the link below to verify your email address:</p>
        <p>{email_verification.token}</p>
        <p>If you did not register with us, please ignore this email.</p>
        <p>Thank you.</p>
        """
        email_services.send_email(email, "Email Verification", body)
