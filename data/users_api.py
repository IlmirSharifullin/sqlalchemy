import flask
from flask import jsonify, request

from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    jobs = db_sess.query(User).all()
    return jsonify(
        {
            'response': 200,
            'users':
                [item.to_dict() for item in jobs]
        }
    )


@blueprint.route('/api/users/<id>', methods=['GET'])
def get_user(id):
    if not id.isdigit():
        return jsonify(
            {
                'response': 404,
                'text': 'Wrong type of id, expecting int type'
            }
        )
    db_sess = db_session.create_session()
    user: User = db_sess.query(User).get(id)
    if user:
        return jsonify(
            {
                'response': 200,
                'user':
                    user.to_dict()
            }
        )
    else:
        return jsonify(
            {
                'response': 404,
                'text': 'NOT FOUND'
            }
        )
