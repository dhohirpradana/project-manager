from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.core.security import verify_password, create_access_token
from app.schemas.user import LoginRequest


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def authenticate(self, username: str, password: str):
        user = self.users.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def login(self, data: LoginRequest) -> dict | None:
        user = self.authenticate(data.username, data.password)
        if not user:
            return None
        token = create_access_token({"sub": str(user.id), "username": user.username})
        return {"access_token": token, "token_type": "bearer", "user_id": user.id}