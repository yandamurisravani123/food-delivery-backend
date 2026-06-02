import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import logger

from app.config.settings import settings


def send_otp_email(to_email: str, otp: str) -> None:
    subject = "Verify Your Account - OTP Code"

    text_body = f"""
Hello,

Thank you for registering with our platform.

Your One-Time Password (OTP) for account verification is:

{otp}

This OTP is valid for 10 minutes.

Please do not share this OTP with anyone for security reasons.

If you did not request this verification, please ignore this email.

Regards,
Food Delivery Team
"""

    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f6f8; padding: 20px;">
            <div style="
                max-width: 520px;
                margin: auto;
                background-color: #ffffff;
                border-radius: 10px;
                padding: 30px;
                border: 1px solid #dddddd;
            ">
                <h2 style="color: #222222; margin-bottom: 20px;">
                    Account Verification
                </h2>

                <p style="font-size: 15px; color: #555555;">
                    Hello,
                </p>

                <p style="font-size: 15px; color: #555555;">
                    Thank you for registering with our platform.
                </p>

                <p style="font-size: 15px; color: #555555;">
                    Your One-Time Password (OTP) for account verification is:
                </p>

                <div style="
                    margin: 25px 0;
                    text-align: center;
                ">
                    <span style="
                        display: inline-block;
                        background-color: #2563eb;
                        color: #ffffff;
                        padding: 14px 28px;
                        font-size: 30px;
                        font-weight: bold;
                        letter-spacing: 6px;
                        border-radius: 8px;
                    ">
                        {otp}
                    </span>
                </div>

                <p style="font-size: 15px; color: #555555;">
                    This OTP is valid for <strong>10 minutes</strong>.
                </p>

                <p style="font-size: 15px; color: #555555;">
                    Please do not share this OTP with anyone for security reasons.
                </p>

                <p style="font-size: 15px; color: #555555;">
                    If you did not request this verification, please ignore this email.
                </p>

                <hr style="border: none; border-top: 1px solid #eeeeee; margin: 25px 0;" />

                <p style="font-size: 14px; color: #888888;">
                    Regards,<br />
                    Food Delivery Team
                </p>
            </div>
        </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.FROM_EMAIL
    msg["To"] = to_email

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(settings.FROM_EMAIL, [to_email], msg.as_string())


def send_restaurant_approval_email(to_email: str, restaurant_name: str) -> None:
    subject = "Restaurant Approved Successfully"
    body = f"""
Hello {restaurant_name},

Congratulations!

Your restaurant has been approved successfully by Super Admin.

Now you can login and start managing your restaurant on the platform.

Thank you,
Food Delivery Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.FROM_EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.FROM_EMAIL, [to_email], msg.as_string())
    except Exception as e:
        logger.exception("Failed to send restaurant approval email: %s", e)

def send_restaurant_rejected_email(to_email: str, restaurant_name: str) -> None:
    subject = "Restaurant Registration Rejected"
    body = f"""
Hello {restaurant_name},

We are sorry to inform you that your restaurant registration has been rejected by Super Admin.

Please contact support or update the required details and try again.

Thank you,
Food Delivery Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.FROM_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(settings.FROM_EMAIL, [to_email], msg.as_string())


def send_delivery_approved_email(to_email: str, full_name: str) -> None:
    subject = "Delivery Agent Approved Successfully"
    body = f"""
Hello {full_name},

Congratulations!

Your delivery agent account has been approved successfully by Super Admin.

You can now login and start accepting delivery tasks.

Thank you,
Food Delivery Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.FROM_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(settings.FROM_EMAIL, [to_email], msg.as_string())


def send_delivery_rejected_email(to_email: str, full_name: str) -> None:
    subject = "Delivery Agent Registration Rejected"
    body = f"""
Hello {full_name},

We are sorry to inform you that your delivery agent registration has been rejected by Super Admin.

Please contact support or update the required details and try again.

Thank you,
Food Delivery Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.FROM_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(settings.FROM_EMAIL, [to_email], msg.as_string())