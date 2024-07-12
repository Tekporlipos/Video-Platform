from flask_mail import Mail, Message

mail = Mail()


class EmailService:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        mail.init_app(app)

    def send_email(self, to, subject, body):
        msg = Message(subject=subject, recipients=[to], body=body)
        try:
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
