import json
import uuid
from datetime import datetime

from app import db
from instance.config import Config


class Video(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(255), nullable=False)
    video_size = db.Column(db.Integer, nullable=False)
    share_link = db.Column(db.String(255), nullable=False)
    uploaded_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    shares = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "video_url": Config.APP_URL+'/'+self.video_url,
            "video_size": self.video_size,
            "share_link": self.share_link,
            "uploaded_by": self.uploaded_by,
            "shares": self.shares,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        },

    def __repr__(self):
        return (
            f"<Videos(id={self.id}, title={self.title}, description={self.description}, video_url={self.video_url}, "
            f"video_size={self.video_size}, share_link={self.share_link}, "
            f"uploaded_by={self.uploaded_by}, shares={self.shares}, created_at={self.created_at}, "
            f"updated_at={self.updated_at})>")
