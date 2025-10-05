import inspect
from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def serializer(body=None, query=None):
    """
    Decorator to validate request data using DRF serializers.
    - If controller defines param `body`, pass body_serializer.validated_data
    - If controller defines param `query`, pass query_serializer.validated_data
    """
    def decorator(func):
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            inject_args = {}

            # Handle body serializer
            if body and "body" in sig.parameters:
                body_serializer = body(data=request.data)
                if not body_serializer.is_valid():
                    return Response(body_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                inject_args["body"] = body_serializer.validated_data

            # Handle query serializer
            if query and "query" in sig.parameters:
                query_serializer = query(data=request.query_params)
                if not query_serializer.is_valid():
                    return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                inject_args["query"] = query_serializer.validated_data

            # Only pass request if it's in the function signature
            if "request" in sig.parameters:
                return func(self, request, *args, **kwargs, **inject_args)
            else:
                return func(self, *args, **kwargs, **inject_args)

        return wrapper
    return decorator
