from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class UserDBModel(BaseModel):
    """
    MongoDB schema representation for the 'users' collection (Phase 6/7).
    
    Fields:
    - _id / id
    - name
    - email
    - password_hash (never store plaintext passwords)
    - created_at
    """
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = Field(None, alias="_id")
    name: str = Field(..., description="Full name of user")
    email: str = Field(..., description="Unique email address")
    password_hash: str = Field(..., description="Argon2/Bcrypt hashed password")
    is_active: bool = Field(True, description="Account active status")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
