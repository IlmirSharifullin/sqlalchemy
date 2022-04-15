import flask
from flask import jsonify

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'response': 200,
            'jobs':
                [item.to_dict() for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<id>')
def get_job(id):
    if not id.isdigit():
        return jsonify(
            {
                'response': 404,
                'text': 'Wrong type of id, int expected'
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
