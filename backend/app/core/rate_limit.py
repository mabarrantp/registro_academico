from time import time

LOGIN_ATTEMPTS = {}
MAX_ATTEMPTS = 5
WINDOW_SECONDS = 60


def check_login_rate_limit(ip: str):
    now = time()
    attempts = LOGIN_ATTEMPTS.get(ip, [])

    attempts = [t for t in attempts if now - t < WINDOW_SECONDS]

    if len(attempts) >= MAX_ATTEMPTS:
        raise Exception("Too many login attempts. Try again later.")

    attempts.append(now)
    LOGIN_ATTEMPTS[ip] = attempts

