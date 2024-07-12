from sqlalchemy.orm import relationship
from app import db


class EmailVerification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='email_verifications')
    token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return (f"<EmailVerification(id={self.id}, user_id={self.user_id}, token={self.token}, "
                f"expires_at={self.expires_at}, created_at={self.created_at}, updated_at={self.updated_at})>")
