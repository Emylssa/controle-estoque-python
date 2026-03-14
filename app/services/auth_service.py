from app.models.user_model import UserModel
from app.utils.security import verify_password


class AuthService:
    @staticmethod
    def login(username: str, password: str):
        user = UserModel.get_by_username(username)
        if user and verify_password(password, user['password_hash']):
            return user
        return None
