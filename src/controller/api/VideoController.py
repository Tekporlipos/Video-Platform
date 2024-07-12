from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from app import app, db
from src.models.VideoModel import Video
from src.services.VideoService import VideoService
from src.utils.httpMethod import HttpMethod
from instance.config import Config

video_service = VideoService()


@app.route('/api/v1/video', methods=[HttpMethod.POST])
def create_video():
    return video_service.create(db, Video, Config, secure_filename, request, app.logger)


@app.route('/api/v1/video', methods=[HttpMethod.GET])
def get_videos():
    page = request.args.get('page', default=1, type=int)
    return video_service.get_videos(db, Video, page, app.logger)


@app.route('/api/v1/video/<video_id>', methods=[HttpMethod.GET])
def get_video_by_id(video_id):
    return video_service.get_video_by_id(db, Video, video_id, app.logger)


@app.route('/api/v1/video/user/<user_id>', methods=[HttpMethod.GET])
def get_videos_by_user_id(user_id):
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=20, type=int)
    return video_service.get_videos_by_user_id(db, Video, user_id, page, size, app.logger)


@app.route('/api/v1/video/share/<share_id>', methods=[HttpMethod.GET])
def get_videos_by_share_id(share_id):
    return video_service.get_videos_by_share_id(db, Video, share_id, app.logger)


@jwt_required()
@app.route('/api/v1/video/<video_id>', methods=[HttpMethod.PATCH])
def update_video_by_id(video_id):
    return video_service.update_video_by_id(db, Video, video_id, request.json, app.logger)


@jwt_required()
@app.route('/api/v1/video/<video_id>', methods=[HttpMethod.DELETE])
def delete_video_by_id(video_id):
    return video_service.delete_video_by_id(db, Video, video_id, app.logger)
