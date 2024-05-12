import string
import random

alphabet = string.ascii_lowercase + string.digits

def gen_id():
    return ''.join(random.choices(alphabet, k=12))