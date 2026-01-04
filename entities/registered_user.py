
class RegisteredUser:

    def __init__(self, email: str, fullName: str, password: str, passwordRepeat: str, roles: list):
        self.email = email
        self.fullName = fullName
        self.password = password
        self.passwordRepeat = passwordRepeat
        self.roles = roles

    @property
    def creds(self):
        return self.email, self.fullName, self.password, self.passwordRepeat, self.roles