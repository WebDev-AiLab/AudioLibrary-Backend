import secrets


def generate_random_string(length=64):
    return secrets.token_hex(length)


def seconds_to_minutes_and_seconds(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f'{m:02d}:{s:02d}'
