import hashlib
import time


def generate_primary_key():
    """Генерация уникального первичного ключа"""
    timestamp = str(int(time.time()))
    unique_string = f"task-{timestamp}"
    return hashlib.sha256(unique_string.encode('utf-8')).hexdigest()[:16]
