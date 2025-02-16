from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path
from pydantic import EmailStr
from typing import List, Dict, Any
import logging
from app.core.config import settings
import os
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        # Get the absolute path to the email_templates directory
        self.templates_dir = Path(__file__).parent.parent / 'email_templates'

        # Ensure the templates directory exists
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir))
        )

        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            TEMPLATE_FOLDER=self.templates_dir,
            VALIDATE_CERTS=True
        )

        self.fast_mail = FastMail(self.conf)

    async def send_welcome_email(self, email: str, name: str) -> bool:
        """
        Send welcome email to newly registered users using a template
        """
        try:
            logger.info(f"Attempting to send welcome email to {email}")

            # Load and render the template
            template = self.env.get_template('welcome.html')
            html_content = template.render(
                name=name,
                email=email,
                support_email="welcome@touristai.online",
                website_url="https://touristai.online"
            )

            message = MessageSchema(
                subject="Welcome to TouristAI - Let's Explore Morocco Together!",
                recipients=[email],
                body=html_content,
                subtype="html"
            )

            await self.fast_mail.send_message(message)
            logger.info(f"Welcome email sent successfully to {email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send welcome email to {email}: {str(e)}")
            logger.error(f"SMTP Settings used: Server={settings.MAIL_SERVER}, Port={settings.MAIL_PORT}")
            return False

    async def send_google_welcome_email(self, email: str, name: str) -> bool:
        """
        Send welcome email to users who registered with Google
        """
        try:
            logger.info(f"Attempting to send Google welcome email to {email}")

            # Load and render the template
            template = self.env.get_template('google_welcome.html')
            html_content = template.render(
                name=name,
                email=email,
                support_email="welcome@touristai.online",
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
            logger.error(f"SMTP Settings used: Server={settings.MAIL_SERVER}, Port={settings.MAIL_PORT}")
            return False

    async def test_email_connection(self) -> bool:
        """
        Test the email connection settings
        """
        try:
            test_message = MessageSchema(
                subject="TouristAI Email Test",
                recipients=[settings.MAIL_USERNAME],
                body="This is a test email to verify the SMTP connection is working.",
                subtype="plain"
            )

            await self.fast_mail.send_message(test_message)
            logger.info("Test email sent successfully")
            return True
        except Exception as e:
            logger.error(f"Email connection test failed: {str(e)}")
            return False


# Create singleton instance
email_service = EmailService()