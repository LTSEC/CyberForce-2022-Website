class User():
    def __init__(self, user):
        self.user = user

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    # Flask-Login is technically able to support these.
    # We don't swing that way.
    def is_anonymous(self):
        return False

    @staticmethod
    def get(user):
        return User(user)

    def get_id(self):
        return self.user

    def __repr__(self):
        return '<User %r>' % self.user

    def get_auth_token(self):
        data = [self.user.id, self.user]
        return login_serializer.dumps(data)
