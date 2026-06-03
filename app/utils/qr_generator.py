import base64
from io import BytesIO

try:
    import qrcode
    _qrcode_available = True
except ImportError:
    _qrcode_available = False


def generate_qr(data: str) -> str:
    """Generate a base64-encoded QR code PNG.
    Requires the 'qrcode[pil]' package: pip install qrcode[pil]
    Returns an empty string if qrcode is not installed.
    """
    if not _qrcode_available:
        return ""

    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()