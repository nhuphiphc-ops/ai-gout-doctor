import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import httpx
from sqlalchemy.orm import Session
import database
import models

# JWT Security Configurations
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "SUPER_SECRET_KEY_FOR_MR_PHI_HEALTH_APP_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30  # 30 days for easy local use

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token", auto_error=False)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return payload
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) -> models.User:
    """
    Dependency to retrieve current authenticated user.
    If no token is provided or invalid, we will automatically fallback to the default user
    to make local PC & phone operations extremely convenient, while maintaining the structure.
    """
    default_email = "mrphi@health.local"
    
    # Auto-create default user if not exists
    default_user = db.query(models.User).filter(models.User.email == default_email).first()
    if not default_user:
        default_user = models.User(
            email=default_email,
            name="Mr. Phi",
            avatar_url="",
            age=47,
            height=1.70,
            target_weight=62.5
        )
        db.add(default_user)
        db.commit()
        db.refresh(default_user)

    if not token:
        # For ease of local deployment, return the default user if auth token is missing
        return default_user
        
    payload = verify_access_token(token)
    if not payload:
        return default_user

    email = payload.get("sub")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return default_user
        
    return user

async def verify_google_token(id_token: str) -> Optional[dict]:
    """
    Verifies a Google OAuth ID Token via Google's tokeninfo API.
    """
    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    "email": data.get("email"),
                    "name": data.get("name"),
                    "picture": data.get("picture")
                }
        except Exception as e:
            print(f"Error validating Google Token: {e}")
            
    return None

# --- GOOGLE FIT INTEGRATION ---

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/auth/google-fit/callback")

def get_google_fit_auth_url(user_email: str) -> str:
    """
    Generates the Google OAuth authorization URL for Google Fit read scopes.
    Falls back to mock redirect if Google credentials are not set up.
    """
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        # Mock mode callback url
        return f"{GOOGLE_REDIRECT_URI}?code=mock_auth_code_for_mr_phi&state={user_email}"
        
    scopes = "https://www.googleapis.com/auth/fitness.activity.read"
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        "response_type=code&"
        f"scope={scopes}&"
        "access_type=offline&"
        "prompt=consent&"
        f"state={user_email}"
    )
    return auth_url

async def exchange_google_fit_code(code: str) -> Optional[dict]:
    """
    Exchanges code for tokens.
    """
    if code == "mock_auth_code_for_mr_phi":
        return {
            "refresh_token": "mock_refresh_token_xyz123",
            "access_token": "mock_access_token_abc789"
        }
        
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": GOOGLE_REDIRECT_URI
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=data)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error exchanging Google Fit code: {e}")
    return None

async def get_google_fit_access_token(refresh_token: str) -> Optional[str]:
    """
    Refreshes access token using refresh token.
    """
    if refresh_token == "mock_refresh_token_xyz123":
        return "mock_access_token_abc789"
        
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=data)
            if response.status_code == 200:
                return response.json().get("access_token")
        except Exception as e:
            print(f"Error refreshing Google Fit token: {e}")
    return None

async def fetch_google_fit_steps(access_token: str) -> int:
    """
    Fetches step count for today (from 00:00:00 to current time local).
    """
    if access_token == "mock_access_token_abc789":
        # Generate mock steps count (e.g. realistic middle-aged walk: 6850 steps)
        import random
        # Seed by current hour to make it progressive during the day
        hour = datetime.now().hour
        base_steps = 1500 + hour * 300
        return base_steps + random.randint(-400, 400)
        
    # Query Google Fit Aggregated Steps for today
    today = date.today()
    start_dt = datetime(today.year, today.month, today.day, 0, 0, 0)
    end_dt = start_dt + timedelta(days=1)
    
    # Milliseconds since epoch
    start_ms = int(start_dt.timestamp() * 1000)
    # Get current time as end bound
    end_ms = int(datetime.now().timestamp() * 1000)
    
    if end_ms <= start_ms:
        end_ms = start_ms + 1000
        
    url = "https://www.googleapis.com/fitness/v1/users/me/dataset/aggregate"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "aggregateBy": [{
            "dataTypeName": "com.google.step_count.delta",
            "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
        }],
        "bucketByTime": { "durationMillis": 86400000 }, # 1 day buckets
        "startTimeMillis": start_ms,
        "endTimeMillis": end_ms
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=body, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                steps = 0
                for bucket in data.get("bucket", []):
                    for dataset in bucket.get("dataset", []):
                        for point in dataset.get("point", []):
                            for val in point.get("value", []):
                                # extract steps
                                steps += val.get("intVal", 0)
                return steps
        except Exception as e:
            print(f"Error fetching Google Fit steps: {e}")
            
    return 0

