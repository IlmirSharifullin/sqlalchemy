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


@blueprint.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):
    if id.isdigit():
        db_sess = db_session.create_session()
        user: User = db_sess.query(User).get(int(id))
        if user:
            if user.id != 1:
                db_sess.delete(user)
                db_sess.commit()
                return jsonify(
                    {
                        'response': 200,
                        'text': 'OK'
                    }
                )
            return jsonify(
                {
                    'response': 404,
                    'text': 'captain can`t be deleted'
                }
            )
        return jsonify(
            {
                'response': 404,
                'text': 'NOT FOUND'
            }
        )
    return jsonify(
        {
            'response': 404,
            'text': 'Wrong type of id, expecting int type'
        }
    )


@blueprint.route('/api/users/', methods=['POST'])
def add_user():
    data = request.json
    if data:
        if all(key in data for key in
               ['surname', 'name', 'address', 'age', 'position', 'speciality', 'email', 'password']):
            db_sess = db_session.create_session()
            if not isinstance(data['age'], int):
                return jsonify({
                    'error': 'age must be int type'
                })
            if not isinstance(data['surname'], str):
                return jsonify({
                    'error': 'surname must be str type'
                })
            if not isinstance(data['name'], str):
                return jsonify({
                    'error': 'name must be str type'
                })
            if not isinstance(data['address'], str):
                return jsonify({
                    'error': 'address must be str type'
                })
            if not isinstance(data['speciality'], str):
                return jsonify({
                    'error': 'speciality must be str type'
                })
            if not isinstance(data['position'], str):
                return jsonify({
                    'error': 'position must be str type'
                })
            if not isinstance(data['email'], str):
                return jsonify({
                    'error': 'email must be str type'
                })
            if not isinstance(data['password'], str):
                return jsonify({
                    'error': 'password must be str type'
                })

            user = User()
            user.surname = data['surname']
            user.name = data['name']
            user.age = int(data['age'])
            user.address = data['address']
            user.position = data['position']
            user.speciality = data['speciality']
            user.email = data['email']
            user.set_password(data['password'])
            db_sess.add(user)
            db_sess.commit()
            return jsonify({
                'response': 200,
                'text': 'user added successfully'
            })
        return jsonify(
            {
                'error': 'Bad request'
            }
        )
    return jsonify(
        {
            'error': 'Empty request'
        }
    )


@blueprint.route('/api/users/<id>', methods=['PUT'])
def edit_user(id):
    if id.isdigit():
        db_sess = db_session.create_session()
        user: User = db_sess.query(User).get(int(id))
        if user:
            if request.json:
                errors = {}
                data = request.json
                keys = ['surname', 'name', 'address', 'age', 'position', 'speciality', 'email', 'password']
                if any(key in data for key in keys):
                    for key in keys:
                        if key in data:
                            value = data[key]
                            if key == 'age':
                                if isinstance(value, int):
                                    user.age = value
                                else:
                                    errors['age'] = 'Wrong type of age, expected int'
                            elif key == 'password':
                                if isinstance(value, str):
                                    user.set_password(value)
                                else:
                                    errors['password'] = 'Wrong type of password, expected str'
                            else:
                                if isinstance(value, str):
                                    if key == 'surname':
                                        user.surname = value
                                    if key == 'name':
                                        user.name = value
                                    if key == 'address':
                                        user.address = value
                                    if key == 'position':
                                        user.position = value
                                    if key == 'speciality':
                                        user.speciality = value
                                    if key == 'email':
                                        user.email = value
                                else:
                                    errors[key] = f'Wrong type of {key}, expected str'
                    db_sess.commit()
                    return jsonify({
                        'response': 200,
                        'errors': errors,
                        'text': 'OK'
                    })
                return jsonify({
                    'response': 404,
                    'text': 'Bad request'
                })
            return jsonify({
                'response': 404,
                'text': 'Empty request'
            })

        return jsonify(
            {
                'response': 404,
                'text': 'USER NOT FOUND'
            }
        )
    return jsonify(
        {
            'response': 404,
            'text': 'Wrong type of id, expecting int type'
        }
    )