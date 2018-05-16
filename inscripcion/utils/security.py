from werkzeug.security import generate_password_hash, check_password_hash

class PasswordManager:
    def __init__(self, plain_password):
        self.plain_password = plain_password

    def hash(self):
        return generate_password_hash(self.plain_password)

    def check_with(self, hashed_password):
        return check_password_hash(hashed_password, self.plain_password)

