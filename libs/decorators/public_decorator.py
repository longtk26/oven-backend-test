from functools import wraps

def public(view_func):
    """
    Mark a Django view as public (no authentication required).
    This sets an attribute on the view that middleware can later check.
    """
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    
    wrapped_view._is_public = True
    return wrapped_view
