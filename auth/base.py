from fastapi_users.authentication import (
    CookieTransport,
    JWTStrategy,
    AuthenticationBackend,
)

cookie_transport = CookieTransport(cookie_name="template", cookie_max_age=60 * 60)


SALT = "VERY_SECRET_AND_ENCRYPTED_LINE"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SALT, lifetime_seconds=60 * 60)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
