import flask
from flask import jsonify, request

from data import db_session
from data.hazard_categories import HazardCategory
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    print(jobs)
    return jsonify(
        {
            'response': 200,
            'jobs':
                [item.to_dict() for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<id>', methods=['GET'])
def get_job(id):
    if not id.isdigit():
        return jsonify(
            {
                'response': 404,
                'text': 'Wrong type of id, expecting int type'
            }
        )
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(id)
    if job:
        return jsonify(
            {
                'response': 200,
                'job':
                    {'job': job.job,
                     'team_leader': job.team_leader,
                     'work_size': job.work_size,
                     'collaborators': job.collaborators,
                     'is_finished': job.is_finished,
                     'start_date': job.start_date,
                     'end_date': job.end_date,
                     'user': f'{job.user.surname} {job.user.name}'}
            }
        )
    else:
        return jsonify(
            {
                'response': 404,
                'text': 'NOT FOUND'
            }
        )


@blueprint.route('/api/jobs', methods=['POST'])
def add_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished', 'hazard_type']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    if db_sess.query(Jobs).get(int(request.json['id'])):
        return jsonify({'error': 'Id already exists'})

    job = Jobs()
    job.id = request.json['id']
    job.team_leader = request.json['team_leader']
    job.hazard_type = request.json['hazard_type']
    job.job = request.json['job']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.is_finished = request.json['is_finished']

    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<id>', methods=['DELETE'])
def delete_job(id):
    if not id.isdigit():
        return jsonify({'error': 'Wrong type of id, expecting int type'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(int(id))
    if not job:
        return jsonify({'error': 'NOT FOUND'})

    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<id>', methods=['PUT'])
def edit_job(id):
    if not id.isdigit():
        return jsonify({'error': 'Wrong type of id, expecting int type'})
    elif not any(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished', 'hazard_type']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job: Jobs = db_sess.query(Jobs).get(int(id))
    if not job:
        return jsonify({'error': 'NOT FOUND'})
    data = request.json
    errors = []
    if 'job' in data:
        job.job = data['job']
    if 'work_size' in data:
        if isinstance(data['work_size'], str) and data['work_size'].isdigit() or isinstance(data['work_size'], int):
            job.work_size = data['work_size']
        else:
            errors.append({'work_size': 'Wrong type, expected int'})
    if 'collaborators' in data:
        try:
            [int(i) for i in data['collaborators'].split(', ')]
        except Exception:
            errors.append({'collaborators': 'Expected ints splitted by ", "'})
        else:
            job.collaborators = data['collaborators']
    if 'is_finished' in data:
        is_fin = data['is_finished']
        if isinstance(is_fin, str) and is_fin.isdigit() or isinstance(is_fin, int):
            if int(data['is_finished']) not in [0, 1]:
                errors.append({'is_finished': 'Expected 1 if True, else 0'})
            else:
                job.is_finished = data['is_finished']
        else:
            errors.append({'is_finished': 'Wrong type, expected int'})

    if 'hazard_type' in data:
        if data['hazard_type'].isdigit():

            haz_typ = db_sess.query(HazardCategory).get(int(data['hazard_type']))
            if not haz_typ:
                errors.append({'hazard_type': 'Not found'})
            else:
                job.hazard_type = data['hazard_type']
        else:
            errors.append({'hazard_type': 'Wrong type, expected int'})
        job.hazard_type = data['hazard_type']
    db_sess.commit()
    return jsonify({
        'errors': errors if errors else 'no errors',
        'response': 'OK'
    })
