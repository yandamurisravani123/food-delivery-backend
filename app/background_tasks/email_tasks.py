from app.core.logger import logger


async def send_otp_email(to_email: str, otp: str) -> None:
    """Send OTP verification email."""
    logger.info(f"[EMAIL] Sending OTP to {to_email}")
    # TODO: integrate SMTP via app.utils.email_utils


async def send_registration_confirmation(to_email: str, name: str) -> None:
    """Send welcome email after successful registration."""
    logger.info(f"[EMAIL] Sending registration confirmation to {to_email}")
    # TODO: integrate SMTP via app.utils.email_utils


async def send_password_reset_email(to_email: str, reset_token: str) -> None:
    """Send password reset link."""
    logger.info(f"[EMAIL] Sending password reset to {to_email}")
    # TODO: integrate SMTP via app.utils.email_utils


async def send_order_confirmation_email(to_email: str, order_id: int) -> None:
    """Send order confirmation email to customer."""
    logger.info(f"[EMAIL] Sending order confirmation for order {order_id} to {to_email}")
    # TODO: integrate SMTP via app.utils.email_utils