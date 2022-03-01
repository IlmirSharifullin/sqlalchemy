from werkzeug.utils import redirect

from data import db_session
from flask import Flask, render_template
from data.users import User

from data.jobs import Jobs
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")

    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    jobs_with_max_collabs = []
    M = 0
    for job in jobs:
        c = len(job.collaborators.split(', '))
        if M < c:
            jobs_with_max_collabs = [job]
            M = c
        elif M == c:
            jobs_with_max_collabs.append(job)
    for job in jobs_with_max_collabs:
        user = db_sess.query(User).filter(User.id == job.team_leader).first()
        print(user.surname, user.name)


if __name__ == '__main__':
    main()


