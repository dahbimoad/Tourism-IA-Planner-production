from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path
import logging
from jinja2 import Environment, FileSystemLoader
from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / 'email_templates'
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.env = Environment(loader=FileSystemLoader(str(self.templates_dir)))

        # Simple Gmail configuration
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,  # Your Gmail address
            MAIL_PASSWORD=settings.MAIL_PASSWORD,  # Your Gmail App Password
            MAIL_FROM=settings.MAIL_USERNAME,  # Same as username for Gmail
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            TEMPLATE_FOLDER=self.templates_dir
        )
        self.fast_mail = FastMail(self.conf)

    async def send_welcome_email(self, email: str, name: str) -> bool:
        try:
            template = self.env.get_template('welcome.html')
            html_content = template.render(
                name=name,
                email=email,
                support_email=settings.MAIL_USERNAME,
                website_url="https://touristai.online"
            )

            message = MessageSchema(
                subject="Welcome to TouristAI - Your Moroccan Adventure Begins!",
                recipients=[email],
                body=html_content,
                subtype="html"
            )

            await self.fast_mail.send_message(message)
            logger.info(f"Welcome email sent successfully to {email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send welcome email to {email}: {str(e)}")
            return False

    async def send_google_welcome_email(self, email: str, name: str) -> bool:
        try:
            template = self.env.get_template('google_welcome.html')
            html_content = template.render(
                name=name,
                email=email,
                support_email=settings.MAIL_USERNAME,
                website_url="https://touristai.online"
            )

            message = MessageSchema(
                subject="Welcome to TouristAI - Your Google Account is Connected!",
                recipients=[email],
                body=html_content,
                subtype="html"
            )

            await self.fast_mail.send_message(message)
            logger.info(f"Google welcome email sent successfully to {email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send Google welcome email to {email}: {str(e)}")
            return False

    async def test_email_connection(self) -> bool:
        """Test the email connection settings"""
        try:
            message = MessageSchema(
                subject="TouristAI Email Test",
                recipients=[settings.MAIL_USERNAME],
                body="This is a test email to verify the SMTP connection is working.",
                subtype="plain"
            )
            await self.fast_mail.send_message(message)
            logger.info("Test email sent successfully")
            return True
        except Exception as e:
            logger.error(f"Email connection test failed: {str(e)}")
            return False


# Create singleton instance
email_service = EmailService()