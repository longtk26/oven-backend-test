from rest_framework.views import exception_handler

def app_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and isinstance(response.data, dict):
        if hasattr(exc, "code"):
            response.data["code"] = exc.code

    return response
