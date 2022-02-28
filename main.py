# from werkzeug.utils import redirect

from data import db_session
from flask import Flask, render_template
from data.users import User

# from data.jobs import Jobs
# from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")

    db_sess = db_session.create_session()
    # app.run()
    captain = User()
    captain.surname = 'Scott'
    captain.name = 'Ridley'
    captain.age = 21
    captain.position = 'captain'
    captain.speciality = 'research engineer'
    captain.address = 'module_1'
    captain.email = 'scott_chief@mars.org'
    db_sess.add(captain)

    Rinat = User()
    Rinat.surname = 'Galeev'
    Rinat.name = 'Rinat'
    Rinat.age = 16
    Rinat.position = 'engineer'
    Rinat.speciality = 'researcher'
    Rinat.address = 'module_3'
    Rinat.email = 'grinat@mars.org'
    db_sess.add(Rinat)

    Ilmir = User()
    Ilmir.surname = 'Sharifullin'
    Ilmir.name = 'Ilmir'
    Ilmir.age = 15
    Ilmir.position = 'main programmer'
    Ilmir.speciality = 'programmer'
    Ilmir.address = 'module_4'
    Ilmir.email = 'ilmirsh@mars.org'
    db_sess.add(Ilmir)

    Kirill = User()
    Kirill.surname = 'Nikitin'
    Kirill.name = 'Kirill'
    Kirill.age = 17
    Kirill.position = 'second programmer'
    Kirill.speciality = 'sysadmin'
    Kirill.address = 'module_5'
    Kirill.email = 'nkirill@mars.org'
    db_sess.add(Kirill)

    db_sess.commit()


if __name__ == '__main__':
    main()
