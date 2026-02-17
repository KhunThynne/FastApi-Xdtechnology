import secrets
import string


def generate_product_key() -> str:
    # สร้าง Key รูปแบบ HP-XXXX-XXXX (เช่น HP-A1B2-C3D4)
    chars = string.ascii_uppercase + string.digits
    part1 = "".join(secrets.choice(chars) for _ in range(4))
    part2 = "".join(secrets.choice(chars) for _ in range(4))
    return f"HP-{part1}-{part2}"
