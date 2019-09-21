from cryptography.exceptions import InvalidSignature as BadSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .errors import InvalidSignature


def check_signature(pub_key, signature, content):
    public_key = Ed25519PublicKey.from_public_bytes(pub_key)
    try:
        public_key.verify(signature, content)
    except BadSignature:
        return InvalidSignature(pub_key)
