import string
import random
import api.models


def generate_unique_code() -> str:
    chars = string.ascii_letters + string.digits
    code = ''.join(random.choice(chars) for _ in range(6))
    if api.models.Referral.objects.filter(code=code).exists():
        return generate_unique_code()
    return code
