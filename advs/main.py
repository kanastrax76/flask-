import atexit

from flask import jsonify, request
from flask_login import LoginManager, logout_user, login_user, current_user

from adv import get_app
from validate import check_password, validate, CreateUserSchema
from crud import get_item
from user_login import UserLogin
from errors import ApiError, error_handler
from views import AdvertisementView, Session, UserView
from models import User, close_db, init_db
import config

adv = get_app()
adv.secret_key = config.SECRET_KEY

login_manager = LoginManager(adv)

init_db()
atexit.register(close_db)


@adv.route('/login', methods=['GET', 'POST'])
def login():
    login_data = validate(request.json, CreateUserSchema)
    with Session() as session:
        user = session.query(User).filter(User.email == login_data["email"]).first()
        if user and check_password(user.password, login_data['password']):
            user_login = UserLogin().create(user)
            login_user(user_login, remember=True)
            return jsonify({'status': 'Auth is successfully'})
        raise ApiError(401, {'status': 'Not authenticated'})


@login_manager.user_loader
def load_user(user_id: int):
    with Session() as session:
        user = get_item(session, User, user_id)
    return UserLogin().create(user)


@adv.route('/logout', methods=['POST'])
# @login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({'status': 'logout'})
    raise ApiError(401, {'status': 'Not authenticated'})


adv.add_url_rule('/adv/<int:adv_id>',
                 view_func=AdvertisementView.as_view('adv_get'),
                 methods=['GET']
                 )
adv.add_url_rule('/adv/<int:adv_id>',
                 view_func=AdvertisementView.as_view('adv'),
                 methods=['PATCH', 'DELETE']
                 )
adv.add_url_rule('/adv',
                 view_func=AdvertisementView.as_view('adv_post'),
                 methods=['POST']
                 )

adv.add_url_rule('/users/<int:user_id>',
                 view_func=UserView.as_view('users'),
                 methods=['GET']
                 )
adv.add_url_rule('/users/',
                 view_func=UserView.as_view('users_post'),
                 methods=['POST']
                 )

adv.errorhandler(ApiError)(error_handler)


if __name__ == '__main__':
    adv.run(debug=1, port=5001)
