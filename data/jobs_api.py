import flask
from flask import jsonify, request

from data import db_session
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