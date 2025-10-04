import jwt
from apis.config import config
from apis.exceptions import UnauthorizedException


def decode_jwt(token: str):
    """
    Decode a JWT token and return the payload.
    Raises UnauthorizedException if invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            config.jwt_secret,
            algorithms=["HS256"],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token has expired")
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Invalid token")
