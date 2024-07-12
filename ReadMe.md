### Project Title: Video Platform

#### Project Objective
The objective of this project is to develop a bespoke video platform for Paul Leonard, a video creator, who wants a branded platform to upload and share videos exclusively for his business. The platform should provide user authentication, video navigation, sharing capabilities, and administrative features for video management.

#### Customer Requirements

**User Functionality:**
1. **Signup & Login:**
   - Users can create an account using email and password.
   - Account verification via email to ensure security and validity.
   - Password reset feature for recovering lost passwords.

2. **Video Navigation:**
   - Users can navigate through video pages.
   - Each page displays one video at a time.
   - Next and previous buttons allow users to load the next or previous video page.

3. **Video Sharing:**
   - Users can share links to specific video pages.
   - A share button on each video page facilitates sharing.

4. **Video Player Controls:**
   - Common control buttons (play, pause, volume control, fullscreen) for video playback.

5. **Branding:**
   - The business logo is prominently displayed on each video page.

**Admin Functionality:**
- **Video Upload:**
  - Admins can upload videos with titles and descriptions.
  - Uploaded videos are managed through administrative privileges.

#### Deliverables

1. **Web Application Source Code:**
   - Hosted on GitHub with Git flow implementation (branches for features, development, and production).
   - README file detailing setup instructions, dependencies, and usage guidelines.

2. **ER Diagram of Database Design:**
   - Entity-Relationship (ER) diagram illustrating the database schema.
   - Tables for users, videos, and associated metadata.

3. **Deployed Link:**
   - A link to the deployed web application for testing and demonstration purposes.

### Detailed Documentation

#### Technology Stack
- **Backend:** Python, Flask framework, SQLAlchemy for ORM.
- **Database:** MySQL or PostgreSQL.
- **Authentication:** Flask JWT Extended for user authentication.
- **Email Service:** SMTP configuration for sending verification and password reset emails.
- **Deployment:** Docker for containerization, AWS or Heroku for cloud deployment.

#### Project Structure

```
video_platform/
│
├── app.py               # Flask application initialization and configuration
│
├── config.py            # Configuration settings (database URI, JWT secret, email server)
│
├── instance/
│   ├── config.py        # Environment-specific configurations (not included in repository)
│   └── logger.py        # Logging configuration for the application
│
├── migration/
│   └── base.py          # Database setup and migration scripts
│
├── routes/
│   └── api.py           # API endpoints for user authentication and video management
│
├── src/
│   ├── models/
│   │   ├── UserModel.py            # User model for authentication
│   │   ├── VideoModel.py           # Video model for video data storage
│   │   └── EmailVerificationModel.py # Model for email verification tokens
│   │
│   ├── services/
│   │   ├── AuthService.py         # Service for user authentication logic
│   │   ├── VideoService.py        # Service for video CRUD operations
│   │   ├── EmailService.py        # Service for sending emails (verification, password reset)
│   │   └── JWTService.py          # Service for JWT token handling
│   │
│   └── utils/
│       ├── httpMethod.py          # HTTP method constants
│       └── database.py            # Database utility functions
│
├── static/
│   └── videos/            # Folder for storing uploaded videos (static files)
│
├── templates/            # HTML templates (if using server-side rendering)
│
├── tests/                # Unit tests for API endpoints and services
│
├── .gitignore            # Git ignore file
├── Dockerfile            # Docker configuration for containerizing the application
└── README.md             # Project documentation including setup, usage, and ER diagram
```

Certainly! Below is an updated section specifically outlining the API endpoints and including the health endpoint for your Video Platform project documentation:

### API Endpoints

#### Authentication (`auth_blueprint`):

- **Register User**
  - `POST /api/v1/register`
  - Description: Registers a new user with email, username, and password.
  - Request Body:
    ```json
    {
      "email": "user@example.com",
      "username": "username",
      "password": "password"
    }
    ```
  - Response:
    - Success: 200 OK
    - Error: 400 Bad Request, 409 Conflict (if username or email already exists)

- **Login User**
  - `POST /api/v1/login`
  - Description: Logs in a user with email and password, returns JWT token.
  - Request Body:
    ```json
    {
      "email": "user@example.com",
      "password": "password"
    }
    ```
  - Response:
    - Success: 200 OK with JWT token
    - Error: 401 Unauthorized

- **Logout User**
  - `POST /api/v1/logout`
  - Description: Logs out the currently logged-in user (requires JWT token).
  - Request Header:
    ```json
    {
      "Authorization": "Bearer <JWT_TOKEN>"
    }
    ```
  - Response:
    - Success: 200 OK
    - Error: 401 Unauthorized

- **Forgot Password**
  - `POST /api/v1/forgot-password`
  - Description: Initiates the process to reset the user's password by sending a reset email.
  - Request Body:
    ```json
    {
      "email": "user@example.com"
    }
    ```
  - Response:
    - Success: 200 OK, Email sent for password reset
    - Error: 404 Not Found (if email not found)

- **Reset Password**
  - `POST /api/v1/reset-password`
  - Description: Resets the user's password after verifying the reset token.
  - Request Body:
    ```json
    {
      "token": "reset_token",
      "password": "new_password"
    }
    ```
  - Response:
    - Success: 200 OK, Password successfully reset
    - Error: 400 Bad Request (if token invalid or expired)

- **Verify Email**
  - `GET /api/v1/verify-email/<token>`
  - Description: Verifies the user's email address after registration.
  - Response:
    - Success: Redirect to login page or success message
    - Error: 404 Not Found (if token invalid)

#### Video Management (`video_blueprint`):

### Upload Video

- **Endpoint**
  - `POST /api/v1/video`
  - Description: Allows admin users to upload a new video.
  - Request Body:
    - **Content Type:** `multipart/form-data`
    - **Form Fields:**
      - `title`: Title of the video (string)
      - `description`: Description of the video (string)
      - `file`: Video file to upload (multipart file)
    - Example:
      ```html
      <form method="post" enctype="multipart/form-data">
        <label for="title">Title:</label><br>
        <input type="text" id="title" name="title" value="Video Title"><br>
        <label for="description">Description:</label><br>
        <textarea id="description" name="description">Video Description</textarea><br>
        <input type="file" id="video_file" name="file"><br><br>
        <input type="submit" value="Submit">
      </form>
      ```
  - Response:
    - Success: 200 OK, Video uploaded successfully
    - Error: 401 Unauthorized (if not admin)


- **Get All Videos**
  - `GET /api/v1/video`
  - Description: Retrieves all videos available on the platform.
  - Response:
    - Success: 200 OK with list of videos
    - Error: 404 Not Found (if no videos found)

- **Get Video by ID**
  - `GET /api/v1/video/<video_id>`
  - Description: Retrieves a specific video by its unique ID.
  - Response:
    - Success: 200 OK with video details
    - Error: 404 Not Found (if video not found)

- **Get Videos by User ID**
  - `GET /api/v1/video/user/<user_id>`
  - Description: Retrieves videos uploaded by a specific user.
  - Response:
    - Success: 200 OK with list of user's videos
    - Error: 404 Not Found (if user has no videos or not found)

- **Get Videos by Share ID**
  - `GET /api/v1/video/share/<share_id>`
  - Description: Retrieves videos shared via a specific link ID.
  - Response:
    - Success: 200 OK with list of shared videos
    - Error: 404 Not Found (if share ID not found)

- **Update Video by ID**
  - `PATCH /api/v1/video/<video_id>`
  - Description: Updates details of a specific video (requires JWT token).
  - Request Body:
    ```json
    {
      "title": "Updated Title",
      "description": "Updated Description"
    }
    ```
  - Response:
    - Success: 200 OK, Video updated successfully
    - Error: 401 Unauthorized, 404 Not Found (if video or user not authorized)

- **Delete Video by ID**
  - `DELETE /api/v1/video/<video_id>`
  - Description: Deletes a specific video from the platform (requires JWT token).
  - Response:
    - Success: 200 OK, Video deleted successfully
    - Error: 401 Unauthorized, 404 Not Found (if video or user not authorized)

#### Health Endpoint

- **Check Health**
  - `GET /api/v1/health/`
  - Description: Endpoint to check the health status of the application.
  - Response:
    - Success: 200 OK, Health status: OK
    - Error: 404 Not Found (if endpoint not found)

#### Database Design (ER Diagram)

- **User Table:**
  - `id`, `email`, `password_hash`, `is_verified`, `verification_token`

- **Video Table:**
  - `id`, `title`, `description`, `video_url`, `uploaded_by`, `share_link`

- **EmailVerification Table:**
  - `id`, `email`, `token`, `created_at`

#### Deployment and Hosting

- **Deployment Options:**
  - Docker containerization for environment consistency.
  - Cloud deployment on RENDER.
