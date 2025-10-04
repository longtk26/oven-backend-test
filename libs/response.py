from rest_framework.response import Response
from rest_framework import status

def make_response(serializer_class, data, status_code=status.HTTP_200_OK):
    """
    Validates response data with the given serializer class,
    then returns a DRF Response object.
    
    Args:
        serializer_class: A DRF serializer class (not instance)
        data: The response data (dict or object)
        status_code: HTTP status (default 200)
    """
    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status_code)
