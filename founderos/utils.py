import time
from django.core.cache import cache
from django.http import HttpResponseForbidden
from functools import wraps

def ratelimit(key='user', rate='10/h', block=True):
    """
    A simple rate limiter using Django's cache.
    rate format: '10/h', '5/m', '100/d'
    """
    try:
        limit_str, period_str = rate.split('/')
        limit = int(limit_str)
    except ValueError:
        limit = 10
        period_str = 'h'

    if period_str == 's':
        period = 1
    elif period_str == 'm':
        period = 60
    elif period_str == 'h':
        period = 3600
    elif period_str == 'd':
        period = 86400
    else:
        period = 3600
        
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if key == 'user' and request.user.is_authenticated:
                ident = str(request.user.pk)
            else:
                ident = request.META.get('REMOTE_ADDR', 'ip')
                
            cache_key = f"rl_{view_func.__name__}_{ident}"
            
            # Simple fixed window counter
            current = cache.get(cache_key, 0)
            if current >= limit:
                if block:
                    return HttpResponseForbidden("Rate limit exceeded. Please try again later.")
            else:
                if current == 0:
                    cache.set(cache_key, 1, period)
                else:
                    try:
                        cache.incr(cache_key)
                    except ValueError:
                        cache.set(cache_key, 1, period)
                        
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
