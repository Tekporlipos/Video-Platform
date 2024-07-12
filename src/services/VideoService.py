import os
import uuid

from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import NoResultFound

from src.utils.responseEntity import error_response, success_response


class VideoService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VideoService, cls).__new__(cls)
        return cls._instance

    @jwt_required(optional=True)
    def create(self, db, Video, Config, secure_filename, request, logger=None):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return error_response('Authorization header is missing or invalid', status_code=401, logger=logger)

        title = request.form.get('title')
        description = request.form.get('description')

        # Check if required fields are present
        if not title or 'file' not in request.files:
            return error_response('Missing required fields: title and video file', status_code=400,
                                  logger=logger)

        try:
            # Get the uploaded file
            video_file = request.files['file']

            # Validate file type (assuming only video file types are allowed)
            allowed_extensions = {'mp4', 'avi', 'mkv', 'mov'}
            if '.' in video_file.filename and video_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                return error_response('Unsupported file type. Only video files (MP4, AVI, MKV, MOV) are allowed.',
                                      status_code=415,  # Unsupported Media Type
                                      logger=logger)

            # Generate a unique filename
            filename = secure_filename(video_file.filename)
            random_string = uuid.uuid4().hex[:6]  # Generate a random hex string of length 6
            unique_filename = f"{random_string}_{filename}"  # Append random string to filename
            file_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)

            # Save the file to your backend
            video_file.save(file_path)
            video_size = os.path.getsize(file_path)

            # Create a Video object and save to database
            video = Video(
                title=title,
                video_url=file_path,
                video_size=video_size,
                share_link=str(uuid.uuid4()),  # Corrected to str(uuid.uuid4())
                uploaded_by=current_user_id,
                description=description
            )

            db.session.add(video)
            db.session.commit()

            return success_response('Video created successfully', video.to_json(), status_code=201,
                                    logger=logger)

        except Exception as e:
            return error_response(str(e), logger=logger, logger_type="error")

    def get_videos(self, db, Video, page=1, logger=None):
        try:
            # Calculate the offset based on page and size (assuming size=1)
            offset = (page - 1) * 1

            # Query for videos based on pagination
            videos = db.session.query(Video).limit(1).offset(offset).all()

            # Count total number of videos
            total_videos = db.session.query(Video).count()

            serialized_videos = [
                video.to_json() for video in videos
            ]

            # Determine if there are next and previous pages
            has_next = page < total_videos // 1  # Assuming size=1
            has_previous = page > 1

            return success_response('Videos retrieved successfully',
                                    data={
                                        'videos': serialized_videos,
                                        'total_videos': total_videos,
                                        'current_page': page,
                                        'videos_per_page': 1,
                                        'has_next': has_next,
                                        'has_previous': has_previous
                                    },
                                    logger=logger)

        except Exception as e:
            return error_response(str(e), logger=logger, logger_type="error")

    def get_video_by_id(self, db, Video, video_id, logger=None):
        try:
            video = db.session.query(Video).filter_by(id=video_id).first()

            if not video:
                return error_response('Video not found', status_code=404, logger=logger)

            serialized_video = video.to_json()  # Serialize the video object as needed

            return success_response('Video retrieved successfully', data={'video': serialized_video}, logger=logger)

        except Exception as e:
            return error_response(str(e), logger=logger, logger_type="error")

    def get_videos_by_user_id(self, db, Video, user_id, page=1, per_page=10, logger=None):
        try:
            # Calculate the offset based on page and per_page
            offset = (page - 1) * per_page

            # Query for videos uploaded by the specified user with pagination
            videos = db.session.query(Video).filter_by(uploaded_by=user_id).limit(per_page).offset(offset).all()

            # Count total number of videos uploaded by the user
            total_videos = db.session.query(Video).filter_by(uploaded_by=user_id).count()

            serialized_videos = [
                video.to_json() for video in videos
            ]

            return success_response(f'Videos uploaded by user {user_id} retrieved successfully',
                                    data={
                                        'videos': serialized_videos,
                                        'total_videos': total_videos,
                                        'current_page': page,
                                        'videos_per_page': per_page
                                    },
                                    logger=logger)

        except Exception as e:
            return error_response(str(e), logger=logger, logger_type="error")

    def get_videos_by_share_id(self, db, Video, share_id, logger=None):
        try:
            video = db.session.query(Video).filter_by(share_link=share_id).first()

            if not video:
                return error_response('Video not found', status_code=404, logger=logger)

            serialized_video = video.to_json()  # Serialize the video object as needed

            return success_response('Video retrieved successfully', data={'video': serialized_video}, logger=logger)

        except Exception as e:
            return error_response(str(e), logger=logger, logger_type="error")

    def update_video_by_id(self, db, Video, video_id, data, logger=None):
        current_user_id = get_jwt_identity()
        try:
            video = db.session.query(Video).get_or_404(video_id)

            if not video:
                return error_response('Video not found', status_code=404, logger=logger)

            # Check if the current user is authorized to update the video
            if current_user_id != video.uploaded_by:
                return error_response('Unauthorized to update this video', status_code=403, logger=logger)

            # Update only allowed fields
            if 'title' in data:
                video.title = data['title']
            if 'description' in data:
                video.description = data['description']

            db.session.commit()

            return success_response('Video updated successfully', video.to_json(), logger=logger)

        except NoResultFound:
            return error_response('Video not found', status_code=404, logger=logger)

        except Exception as e:
            db.session.rollback()
            return error_response(str(e), logger=logger, logger_type="error")

    def delete_video_by_id(self, db, Video, video_id, logger=None):
        current_user_id = get_jwt_identity()
        try:
            video = db.session.query(Video).filter_by(id=video_id).first()

            if not video:
                return error_response('Video not found', status_code=404, logger=logger)

            # Check if the current user is authorized to delete the video
            if current_user_id != video.uploaded_by:
                return error_response('Unauthorized to delete this video', status_code=403, logger=logger)

            db.session.delete(video)
            db.session.commit()

            return success_response('Video deleted successfully', logger=logger)

        except NoResultFound:
            return error_response('Video not found', status_code=404, logger=logger)

        except Exception as e:
            db.session.rollback()
            return error_response(str(e), logger=logger, logger_type="error")
