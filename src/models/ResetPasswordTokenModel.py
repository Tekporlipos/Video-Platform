from app import db


class PasswordResetToken(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    token = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<PasswordResetToken(email={self.email}, token={self.token}, created_at={self.created_at})>"
