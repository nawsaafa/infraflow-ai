"""
InfraFlow AI - Authentication Middleware
JWT-based authentication and authorization
"""

from typing import Optional
import os
import logging
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from passlib.context import CryptContext

from models import User

logger = logging.getLogger(__name__)

# Security configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer for JWT tokens
security = HTTPBearer()


class AuthenticationError(Exception):
    """Authentication error"""
    pass


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token

    Args:
        data: Data to encode in token (user_id, email, etc.)
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify and decode JWT token

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        AuthenticationError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    except jwt.JWTError as e:
        raise AuthenticationError(f"Invalid token: {str(e)}")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password to verify against

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Get current authenticated user from JWT token

    This is a FastAPI dependency that can be used to protect endpoints.
    It extracts the JWT token from the Authorization header, verifies it,
    and returns the user information.

    Args:
        credentials: HTTP Bearer credentials containing JWT token

    Returns:
        User object with authenticated user information

    Raises:
        HTTPException: If authentication fails

    Example:
        @app.get("/protected")
        async def protected_route(user: User = Depends(get_current_user)):
            return {"user_id": user.id, "email": user.email}
    """
    try:
        # Extract token from credentials
        token = credentials.credentials

        # Verify and decode token
        payload = verify_token(token)

        # Extract user information from payload
        user_id = payload.get("sub")
        email = payload.get("email")

        if not user_id or not email:
            raise AuthenticationError("Invalid token payload")

        # Create User object
        user = User(
            id=user_id,
            email=email,
            name=payload.get("name"),
            organization=payload.get("organization"),
            role=payload.get("role", "user"),
            is_admin=payload.get("is_admin", False)
        )

        logger.info(f"Authenticated user: {user.email}")
        return user

    except AuthenticationError as e:
        logger.warning(f"Authentication failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Unexpected authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current user and verify they have admin privileges

    This dependency can be used to protect admin-only endpoints.

    Args:
        current_user: Current authenticated user

    Returns:
        User object if user is admin

    Raises:
        HTTPException: If user is not admin

    Example:
        @app.delete("/admin/projects/{project_id}")
        async def delete_any_project(
            project_id: str,
            admin: User = Depends(get_current_admin_user)
        ):
            # Only admins can access this
            pass
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

    return current_user


def create_user_token(user_id: str, email: str, **kwargs) -> str:
    """
    Create JWT token for a user

    Args:
        user_id: User ID
        email: User email
        **kwargs: Additional claims (name, organization, role, is_admin)

    Returns:
        JWT token string
    """
    token_data = {
        "sub": user_id,
        "email": email,
        "name": kwargs.get("name"),
        "organization": kwargs.get("organization"),
        "role": kwargs.get("role", "user"),
        "is_admin": kwargs.get("is_admin", False)
    }

    return create_access_token(token_data)


# Optional: API Key authentication (alternative to JWT)
class APIKeyAuth:
    """
    API Key authentication for service-to-service communication

    This can be used as an alternative to JWT for automated processes,
    integrations, or external services.
    """

    def __init__(self):
        """Initialize API key authentication"""
        # In production, API keys would be stored in database
        self.valid_api_keys = self._load_api_keys()

    def _load_api_keys(self) -> dict:
        """
        Load valid API keys from environment or database

        Returns:
            Dictionary mapping API keys to service information
        """
        # Load from environment for now
        api_keys = {}

        # Example: INFRAFLOW_API_KEY_SERVICE1=key123:service1:read,write
        for key, value in os.environ.items():
            if key.startswith("INFRAFLOW_API_KEY_"):
                parts = value.split(":")
                if len(parts) >= 2:
                    api_key = parts[0]
                    service_name = parts[1]
                    permissions = parts[2].split(",") if len(parts) > 2 else []

                    api_keys[api_key] = {
                        "service": service_name,
                        "permissions": permissions
                    }

        return api_keys

    def verify_api_key(self, api_key: str) -> Optional[dict]:
        """
        Verify API key and return service information

        Args:
            api_key: API key to verify

        Returns:
            Service information if valid, None otherwise
        """
        return self.valid_api_keys.get(api_key)


# Global API key authenticator
api_key_auth = APIKeyAuth()


async def get_api_key_service(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Authenticate using API key

    This dependency can be used for service-to-service authentication.

    Args:
        credentials: HTTP Bearer credentials containing API key

    Returns:
        Service information dictionary

    Raises:
        HTTPException: If API key is invalid

    Example:
        @app.post("/api/webhook")
        async def webhook_handler(
            data: dict,
            service: dict = Depends(get_api_key_service)
        ):
            # Authenticated service access
            logger.info(f"Request from service: {service['service']}")
            return {"status": "received"}
    """
    try:
        api_key = credentials.credentials

        service_info = api_key_auth.verify_api_key(api_key)

        if not service_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"API key authenticated: {service_info['service']}")
        return service_info

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API key authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate API key",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Rate limiting helper
class RateLimiter:
    """
    Simple in-memory rate limiter

    In production, use Redis-based rate limiting for distributed systems.
    """

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        """
        Initialize rate limiter

        Args:
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}  # user_id -> [(timestamp, count)]

    def is_allowed(self, user_id: str) -> bool:
        """
        Check if request is allowed for user

        Args:
            user_id: User identifier

        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_seconds)

        # Clean old entries
        if user_id in self.requests:
            self.requests[user_id] = [
                (ts, count) for ts, count in self.requests[user_id]
                if ts > window_start
            ]
        else:
            self.requests[user_id] = []

        # Count requests in window
        total_requests = sum(count for _, count in self.requests[user_id])

        if total_requests >= self.max_requests:
            return False

        # Add current request
        self.requests[user_id].append((now, 1))
        return True


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=100, window_seconds=60)


async def check_rate_limit(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Check rate limit for authenticated user

    This dependency can be added to endpoints to enforce rate limiting.

    Args:
        current_user: Current authenticated user

    Returns:
        User object if rate limit not exceeded

    Raises:
        HTTPException: If rate limit exceeded

    Example:
        @app.get("/api/expensive-operation")
        async def expensive_operation(
            user: User = Depends(check_rate_limit)
        ):
            # Rate-limited endpoint
            pass
    """
    if not rate_limiter.is_allowed(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )

    return current_user
