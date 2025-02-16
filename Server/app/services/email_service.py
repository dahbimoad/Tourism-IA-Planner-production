from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path
from typing import Optional
import logging
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / 'email_templates'
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        # Namecheap Private Email SMTP Configuration
        self.smtp_config = {
            'host': 'mail.privateemail.com',
            'port': 587,
            'username': settings.MAIL_USERNAME,
            'password': settings.MAIL_PASSWORD,
            'use_tls': True,
            'timeout': 30
        }

        logger.info("Initializing Email Service with Namecheap Private Email configuration")
        self._verify_smtp_settings()

    def _verify_smtp_settings(self):
        """Verify SMTP settings are properly configured"""
        required_settings = [
            ('MAIL_USERNAME', self.smtp_config['username']),
            ('MAIL_PASSWORD', self.smtp_config['password'])
        ]

        missing_settings = [name for name, value in required_settings if not value]
        if missing_settings:
            error_msg = f"Missing required SMTP settings: {', '.join(missing_settings)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    def _create_smtp_connection(self) -> Optional[smtplib.SMTP]:
        """Create and return an SMTP connection with proper error handling for Namecheap"""
        try:
            logger.info(f"Attempting to connect to SMTP server: {self.smtp_config['host']}:{self.smtp_config['port']}")

            # Create SMTP connection with timeout
            smtp = smtplib.SMTP(
                self.smtp_config['host'],
                self.smtp_config['port'],
                timeout=self.smtp_config['timeout']
            )

            # Enable debug output for troubleshooting
            smtp.set_debuglevel(1)

            # Identify ourselves to SMTP client
            logger.debug("Sending EHLO command")
            smtp.ehlo()

            # Start TLS encryption
            if self.smtp_config['use_tls']:
                logger.debug("Starting TLS encryption")
                context = ssl.create_default_context()
                smtp.starttls(context=context)
                smtp.ehlo()

            # Login with full email address as username
            logger.debug(f"Attempting login with username: {self.smtp_config['username']}")
            smtp.login(self.smtp_config['username'], self.smtp_config['password'])
            logger.info("Successfully connected to SMTP server")

            return smtp

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication failed: {str(e)}")
            logger.error("Please verify your Namecheap Private Email credentials")
            raise
        except ssl.SSLError as e:
            logger.error(f"SSL/TLS error: {str(e)}")
            logger.error("Please verify your SSL/TLS settings")
            raise
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to create SMTP connection: {str(e)}")
            raise

    async def send_welcome_email(self, email: str, name: str) -> bool:
        """Send welcome email with enhanced error handling and logging"""
        try:
            logger.info(f"Preparing welcome email for {email}")

            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Welcome to TouristAI - Let's Explore Morocco Together!"
            msg['From'] = f"TouristAI Morocco <{settings.MAIL_FROM}>"
            msg['To'] = email

            # Create HTML content
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2ba67b;">Welcome to TouristAI, {name}!</h2>
                        <p>Thank you for joining TouristAI, your personal guide to exploring the wonders of Morocco!</p>
                        <p>With our platform, you can:</p>
                        <ul>
                            <li>Create personalized travel itineraries</li>
                            <li>Discover hidden gems across Morocco</li>
                            <li>Get AI-powered recommendations</li>
                            <li>Optimize your travel budget</li>
                        </ul>
                        <p>Start planning your Moroccan adventure today!</p>
                        <p style="margin-top: 20px;">Best regards,<br>The TouristAI Team</p>
                    </div>
                </body>
            </html>
            """

            # Add plain text alternative
            text = f"""
            Welcome to TouristAI, {name}!

            Thank you for joining TouristAI, your personal guide to exploring the wonders of Morocco!

            Start planning your Moroccan adventure today!

            Best regards,
            The TouristAI Team
            """

            msg.attach(MIMEText(text, 'plain'))
            msg.attach(MIMEText(html, 'html'))

            # Create SMTP connection and send
            with self._create_smtp_connection() as smtp:
                logger.info(f"Sending welcome email to {email}")
                smtp.send_message(msg)
                logger.info(f"Welcome email sent successfully to {email}")
                return True

        except smtplib.SMTPException as e:
            logger.error(f"SMTP error sending welcome email to {email}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending welcome email to {email}: {str(e)}")
            return False

    async def send_google_welcome_email(self, email: str, name: str) -> bool:
        """Send welcome email for Google-authenticated users"""
        try:
            logger.info(f"Preparing Google welcome email for {email}")

            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Welcome to TouristAI - Your Google Account is Connected!"
            msg['From'] = f"TouristAI Morocco <{settings.MAIL_FROM}>"
            msg['To'] = email

            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2ba67b;">Welcome to TouristAI, {name}!</h2>
                        <p>Your Google account has been successfully connected to TouristAI!</p>
                        <p>You're now ready to:</p>
                        <ul>
                            <li>Create personalized travel plans</li>
                            <li>Explore Morocco's finest destinations</li>
                            <li>Get smart travel recommendations</li>
                            <li>Save your favorite itineraries</li>
                        </ul>
                        <p>Start your Moroccan journey today!</p>
                        <p style="margin-top: 20px;">Best regards,<br>The TouristAI Team</p>
                    </div>
                </body>
            </html>
            """

            # Add plain text alternative
            text = f"""
            Welcome to TouristAI, {name}!

            Your Google account has been successfully connected to TouristAI!

            Start your Moroccan journey today!

            Best regards,
            The TouristAI Team
            """

            msg.attach(MIMEText(text, 'plain'))
            msg.attach(MIMEText(html, 'html'))

            with self._create_smtp_connection() as smtp:
                logger.info(f"Sending Google welcome email to {email}")
                smtp.send_message(msg)
                logger.info(f"Google welcome email sent successfully to {email}")
                return True

        except smtplib.SMTPException as e:
            logger.error(f"SMTP error sending Google welcome email to {email}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Google welcome email to {email}: {str(e)}")
            return False


# Create singleton instance
email_service = EmailService()
