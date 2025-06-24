from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class AttachUserIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # In a real app, extract user_id from request headers or JWT
        request.state.user_id = "sample_user_id_123"
        response = await call_next(request)
        return response
