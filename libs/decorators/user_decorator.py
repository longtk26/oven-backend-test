import inspect
from functools import wraps
from apis.exceptions import UnauthorizedException
from libs.jwt import decode_jwt


def user():
    """
    Decorator to extract user data from JWT token and inject it into the view method.
    - Extracts the Authorization header
    - Decodes the JWT token
    - Passes user_data to the method as an argument
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                raise UnauthorizedException("Authorization header missing or invalid")

            token = auth_header.split(" ")[1]

            try:
                user_data = decode_jwt(token)
            except Exception:
                raise UnauthorizedException("Invalid or expired token")

            # Inject user_data into the method if it accepts 'user'
            sig = inspect.signature(func)
            inject_args = {}
            if "user" in sig.parameters:
                inject_args["user"] = user_data

            # Call the original function
            if "request" in sig.parameters:
                return func(self, request, *args, **kwargs, **inject_args)
            else:
                return func(self, *args, **kwargs, **inject_args)

        return wrapper
    return decorator
