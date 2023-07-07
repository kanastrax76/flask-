from flask_login import UserMixin

from errors import ApiError


class UserLogin(UserMixin):
    def __init__(self):
        self.__user = None

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        try:
            return self.__user.id
        except AttributeError:
            raise ApiError(404, 'Not found user_id')
