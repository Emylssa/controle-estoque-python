from app.models.database import initialize_database
from app.models.user_model import UserModel
from app.ui.login_window import LoginWindow


if __name__ == '__main__':
    initialize_database()
    UserModel.create_default_admin()
    LoginWindow().run()
