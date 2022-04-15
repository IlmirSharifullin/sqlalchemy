from flask_restful import abort
from werkzeug.utils import redirect

from data import db_session, jobs_api
from flask import Flask, render_template, request, make_response

from data.departments import Department
from data.users import User
from data.jobs import Jobs
from forms.addjob import AddJobForm
from forms.login import LoginForm
from forms.user import RegisterForm
from flask_login import LoginManager, login_required, logout_user, login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        cols = form.collaborators.data
        try:
            [int(i) for i in cols.split(', ')]
        except Exception as e:
            print(e)
            return render_template('add_job.html', message='Wrong collaborators', form=form, user=current_user,
                                   title='Добавление работы')
        if not form.work_size.data.isdigit():
            return render_template('add_job.html', message='Объем работы выражается в количестве часов', form=form,
                                   user=current_user, title='Добавление работы')
        job = Jobs()
        job.team_leader = current_user.id
        job.job = form.job.data
        job.work_size = int(form.work_size.data)
        job.collaborators = cols
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')

    return render_template('add_job.html', form=form, user=current_user, title='Добавление работы')


@app.route('/delete_job/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if job and (job.team_leader == current_user.id or current_user.id == 1):
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = AddJobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job and (job.team_leader == current_user.id or current_user.id == 1):
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job and (job.team_leader == current_user.id or current_user.id == 1):
            job.job = form.job.data
            job.work_size = int(form.work_size.data)
            job.is_finished = form.is_finished.data
            job.collaborators = form.collaborators.data
            db_sess.commit()
            print('Принято')
            return redirect('/')
        else:
            abort(404)
    return render_template('add_job.html',
                           title='Редактирование работы',
                           form=form,
                           user=job.user
                           )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
def jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('index.html', jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.email = form.email.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.register_blueprint(jobs_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
