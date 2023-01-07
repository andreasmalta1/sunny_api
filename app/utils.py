from passlib.context import CryptContext

try:
    import app.models as models
    from app.config import settings
except ImportError:
    import models
    from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)
