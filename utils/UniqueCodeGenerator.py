from django.utils import timezone
import hashlib


def generate_key(text: str, size: int = 10):
    return hashlib.md5(str(text + str(timezone.now())).encode()).hexdigest()[:size]
