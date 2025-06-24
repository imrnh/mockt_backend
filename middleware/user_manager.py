from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from firebase_admin import auth

# Set your protected paths here (can be extended)
PROTECTED_PATHS = {
    "/create_interview_session",
    "/secure/data",
    "/admin",
}

class FirebaseAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Use default or custom protected path set
        self.protected_paths = PROTECTED_PATHS

    async def dispatch(self, request: Request, call_next):
        request.state.user_id = None  # Set default to avoid AttributeError

        # Only require auth if path is protected
        if any(request.url.path.startswith(p) for p in self.protected_paths):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

            token = auth_header.split("Bearer ")[-1]
            try:
                decoded_token = auth.verify_id_token(token)
                request.state.user_id = decoded_token["uid"]
            except Exception:
                raise HTTPException(status_code=401, detail="Invalid or expired token")
        else:
            # Token is optional for unprotected routes
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split("Bearer ")[-1]
                try:
                    decoded_token = auth.verify_id_token(token)
                    request.state.user_id = decoded_token["uid"]
                except Exception:
                    pass  # Ignore errors silently for public routes

        return await call_next(request)
