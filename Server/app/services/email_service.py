import socket
import time
import uuid
from pathlib import Path
import logging
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import smtplib
from typing import Optional
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configure socket default timeout
socket.setdefaulttimeout(60)


class EmailService:
    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / 'email_templates'
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        # Initialize service with Namecheap Private Email settings
        self.smtp_config = {
            'host': 'mail.privateemail.com',
            'port': 587,
            'username': settings.MAIL_USERNAME,
            'password': settings.MAIL_PASSWORD,
            'use_tls': True,
            'timeout': 60
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
        """Create and return an SMTP connection with enhanced error handling for production"""
        try:
            logger.info(f"Attempting to connect to SMTP server: {self.smtp_config['host']}:{self.smtp_config['port']}")

            # Create SMTP connection with extended timeout
            smtp = smtplib.SMTP(
                self.smtp_config['host'],
                self.smtp_config['port'],
                timeout=self.smtp_config['timeout']
            )

            # Enable debug output
            smtp.set_debuglevel(2)

            # Initial EHLO with server address
            try:
                fqdn = socket.getfqdn()
                smtp.ehlo(fqdn)
            except:
                # Fallback to basic EHLO if FQDN fails
                smtp.ehlo()

            # Start TLS encryption with enhanced security
            if self.smtp_config['use_tls']:
                logger.debug("Starting TLS encryption")
                context = ssl.create_default_context()
                context.check_hostname = True
                context.verify_mode = ssl.CERT_REQUIRED

                try:
                    smtp.starttls(context=context)
                    smtp.ehlo()  # Second EHLO after TLS
                except Exception as tls_error:
                    logger.error(f"TLS error: {str(tls_error)}")
                    # Fallback to basic TLS if enhanced security fails
                    smtp.starttls()
                    smtp.ehlo()

            # Login with retry mechanism
            max_retries = 3
            retry_delay = 2
            last_error = None

            for attempt in range(max_retries):
                try:
                    logger.debug(f"Login attempt {attempt + 1} for user: {self.smtp_config['username']}")
                    smtp.login(self.smtp_config['username'], self.smtp_config['password'])
                    logger.info("Successfully authenticated with SMTP server")
                    break
                except smtplib.SMTPAuthenticationError as auth_error:
                    last_error = auth_error
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    raise
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    raise

            if last_error:
                raise last_error

            # Verify connection is alive
            smtp.noop()

            # Set socket options for stability
            smtp.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

            return smtp

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication failed: {str(e)}")
            raise
        except ssl.SSLError as e:
            logger.error(f"SSL/TLS error: {str(e)}")
            raise
        except socket.gaierror as e:
            logger.error(f"DNS lookup failed: {str(e)}")
            raise
        except socket.timeout as e:
            logger.error(f"Connection timeout: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to create SMTP connection: {str(e)}")
            raise

    async def send_welcome_email(self, email: str, name: str) -> bool:
        """Send welcome email with enhanced production error handling"""
        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                logger.info(f"Preparing welcome email for {email} (Attempt {attempt + 1}/{max_retries})")

                # Create message
                msg = MIMEMultipart('alternative')
                msg['Subject'] = "Welcome to TouristAI - Let's Explore Morocco Together!"
                msg['From'] = f"TouristAI Morocco <{self.smtp_config['username']}>"
                msg['To'] = email
                msg['Message-ID'] = f"<{uuid.uuid4()}@touristai.online>"
                msg['Date'] = formatdate(localtime=True)
                msg['Return-Path'] = self.smtp_config['username']

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
                            <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                                <p>Best regards,<br>The TouristAI Team</p>
                            </div>
                        </div>
                    </body>
                </html>
                """

                # Add plain text version
                text = f"""
                Welcome to TouristAI, {name}!

                Thank you for joining TouristAI, your personal guide to exploring the wonders of Morocco!

                Start planning your Moroccan adventure today!

                Best regards,
                The TouristAI Team
                """

                part1 = MIMEText(text, 'plain')
                part2 = MIMEText(html, 'html')

                msg.attach(part1)
                msg.attach(part2)

                try:
                    with self._create_smtp_connection() as smtp:
                        logger.info(f"Sending welcome email to {email}")

                        try:
                            # Send with explicit MAIL FROM and RCPT TO
                            smtp.sendmail(
                                from_addr=self.smtp_config['username'],
                                to_addrs=[email],
                                msg=msg.as_string()
                            )

                            # Verify connection is still alive
                            smtp.noop()
                            logger.info(f"Welcome email sent successfully to {email}")
                            return True

                        except smtplib.SMTPRecipientsRefused as e:
                            logger.error(f"Recipients refused for {email}: {str(e)}")
                            if attempt < max_retries - 1:
                                time.sleep(retry_delay)
                                continue
                            return False

                        except smtplib.SMTPDataError as e:
                            logger.error(f"Data error while sending to {email}: {str(e)}")
                            if attempt < max_retries - 1:
                                time.sleep(retry_delay)
                                continue
                            return False

                        except Exception as e:
                            logger.error(f"Unexpected error during message sending to {email}: {str(e)}")
                            if attempt < max_retries - 1:
                                time.sleep(retry_delay)
                                continue
                            return False

                except smtplib.SMTPServerDisconnected as e:
                    logger.error(f"Server disconnected while sending to {email}: {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    return False

                except Exception as e:
                    logger.error(f"Connection error while sending to {email}: {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    return False

            except Exception as e:
                logger.error(f"Email preparation error for {email}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return False

        logger.error(f"All retry attempts failed for {email}")
        return False

    async def send_google_welcome_email(self, email: str, name: str) -> bool:
        """Send welcome email for Google-authenticated users"""
        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                logger.info(f"Preparing Google welcome email for {email} (Attempt {attempt + 1}/{max_retries})")

                msg = MIMEMultipart('alternative')
                msg['Subject'] = "Welcome to TouristAI - Your Google Account is Connected!"
                msg['From'] = f"TouristAI Morocco <{self.smtp_config['username']}>"
                msg['To'] = email
                msg['Message-ID'] = f"<{uuid.uuid4()}@touristai.online>"
                msg['Date'] = formatdate(localtime=True)
                msg['Return-Path'] = self.smtp_config['username']

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
                            <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                                <p>Best regards,<br>The TouristAI Team</p>
                            </div>
                        </div>
                    </body>
                </html>
                """

                text = f"""
                Welcome to TouristAI, {name}!

                Your Google account has been successfully connected to TouristAI!

                Start your Moroccan journey today!

                Best regards,
                The TouristAI Team
                """

                part1 = MIMEText(text, 'plain')
                part2 = MIMEText(html, 'html')

                msg.attach(part1)
                msg.attach(part2)

                try:
                    with self._create_smtp_connection() as smtp:
                        logger.info(f"Sending Google welcome email to {email}")

                        try:
                            # Send with explicit MAIL FROM and RCPT TO
                            smtp.sendmail(
                                from_addr=self.smtp_config['username'],
                                to_addrs=[email],
                                msg=msg.as_string()
                            )

                            # Verify connection is still alive
                            smtp.noop()
                            logger.info(f"Google welcome email sent successfully to {email}")
                            return True

                        except smtplib.SMTPRecipientsRefused as e:
                            logger.error(f"Recipients refused for {email}: {str(e)}")
                            if attempt < max_retries - 1:
                                time.sleep(retry_delay)
                                continue
                            return False

                        except smtplib.SMTPDataError as e:
                            logger.error(f"Data error while sending to {email}: {str(e)}")
                            if attempt < max_retries - 1:
                                time.sleep(retry_delay)
                                continue
                            return False

                        except Exception as e:
                            logger.error(f"Unexpected error during message sending to {email}: {str(e)}")
                            if attempt < max_retries - 1:
                                time.sleep(retry_delay)
                                continue
                            return False

                except smtplib.SMTPServerDisconnected as e:
                    logger.error(f"Server disconnected while sending to {email}: {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    return False

                except Exception as e:
                    logger.error(f"Connection error while sending to {email}: {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    return False

            except Exception as e:
                logger.error(f"Email preparation error for {email}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return False

        logger.error(f"All retry attempts failed for {email}")
        return False

    async def test_connection(self) -> bool:
        """Test the email connection settings"""
        try:
            with self._create_smtp_connection() as smtp:
                smtp.noop()
                logger.info("SMTP connection test successful")
                return True
        except Exception as e:
            logger.error(f"SMTP connection test failed: {str(e)}")
            return False


# Create singleton instance
email_service = EmailService()