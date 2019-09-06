import os
import random

ID_ALPHABET = ('0123456789aAbBcC'
               'dDeEfFgGhHiIjJkK'
               'lLmMnNoOpPqQrRsS'
               'tTuUvVwWxXyYzZ_-')


def generate_id(k: int) -> str:
    random.seed(os.urandom(300))
    return ''.join(random.choices(ID_ALPHABET, k=k))
