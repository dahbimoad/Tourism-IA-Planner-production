from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path
import logging
from app.core.config import settings
from jinja2 import Environment, FileSystemLoader
from email.utils import formatdate, make_msgid
import time
import asyncio
logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / 'email_templates'
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.env = Environment(loader=FileSystemLoader(str(self.templates_dir)))

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
        try:
            logger.info(f"Attempting to send welcome email to {email}")

            template = self.env.get_template('welcome.html')
            html_content = template.render(
                name=name,
                email=email,
                support_email=settings.MAIL_USERNAME,
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
            return False

    async def send_google_welcome_email(self, email: str, name: str) -> bool:
        try:
            logger.info(f"Attempting to send Google welcome email to {email}")

            template = self.env.get_template('google_welcome.html')
            html_content = template.render(
                name=name,
                email=email,
                support_email=settings.MAIL_USERNAME,
                website_url="https://touristai.online"
            )

            # Create unique message ID and date
            msg_id = make_msgid(domain='touristai.online')
            date = formatdate(time.time(), localtime=True)

            # Add enhanced headers for better deliverability
            message = MessageSchema(
                subject="Welcome to TouristAI - Your Google Account is Connected!",
                recipients=[email],
                body=html_content,
                subtype="html",
                headers={
                    "Message-ID": msg_id,
                    "Date": date,
                    "From": f"{settings.MAIL_FROM_NAME} <{settings.MAIL_USERNAME}>",
                    "X-Priority": "3",
                    "X-MSMail-Priority": "Normal",
                    "Importance": "Normal",
                    "X-Mailer": "TouristAI Service",
                    "List-Unsubscribe": f"<mailto:{settings.MAIL_USERNAME}?subject=unsubscribe>",
                    "Precedence": "bulk",
                    "X-Auto-Response-Suppress": "OOF, AutoReply",
                    "Auto-Submitted": "auto-generated",
                    "X-Report-Abuse": f"Please report abuse here: mailto:{settings.MAIL_USERNAME}",
                    "Feedback-ID": "welcome-email:touristai:google-signup:1"
                }
            )

            # Add a small delay to prevent rate limiting
            await asyncio.sleep(1)

            await self.fast_mail.send_message(message)
            logger.info(f"Google welcome email sent successfully to {email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send Google welcome email to {email}: {str(e)}")
            return False

    async def test_email_connection(self) -> bool:
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