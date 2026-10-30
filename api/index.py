import os
import sys
from urllib.parse import urlparse

# Add root directory to Python path so app modules and assets can be imported properly
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app

class VercelPathMiddleware:
    """
    WSGI Middleware to fix Flask's PATH_INFO when deployed behind Vercel rewrites.
    Vercel sets HTTP_X_MATCHED_PATH with the user's requested path, while
    PATH_INFO defaults to '/api/index'.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # 1. Prefer HTTP_X_MATCHED_PATH header sent by Vercel proxy
        matched_path = environ.get('HTTP_X_MATCHED_PATH') or environ.get('HTTP_X_FORWARDED_URI')
        if matched_path:
            parsed = urlparse(matched_path)
            environ['PATH_INFO'] = parsed.path or '/'
        else:
            path_info = environ.get('PATH_INFO', '')
            if path_info in ['/api/index', '/api/index/', '/api', '']:
                environ['PATH_INFO'] = '/'
            elif path_info.startswith('/api/index/'):
                environ['PATH_INFO'] = path_info[len('/api/index'):]

        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)
