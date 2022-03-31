from flask_restful import abort
from sqlalchemy.sql.elements import or_
from werkzeug.utils import redirect

from data import db_session
from flask import Flask, render_template, request, make_response

from data.departments import Department
from data.users import User
from data.jobs import Jobs
from forms.add_department import AddDepartmentForm
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
        job = db_sess.query(Jobs).get(id)
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


@app.route('/departments')
def departments():
    db_sess = db_session.create_session()
    deps = db_sess.query(Department).all()
    return render_template('departments.html', deps=deps, db_sess=db_sess, User=User)


@app.route('/delete_department/<int:id>')
@login_required
def delete_dep(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).get(id)
    if current_user.id == dep.chief or current_user.id == 1:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = AddDepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        mems = form.members.data
        try:
            [int(i) for i in mems.split(', ')]
        except Exception as e:
            return render_template('add_department.html', message='Неправильно написаны ID сотрудников', form=form,
                                   title='Добавление департамента')
        dep = Department()
        dep.chief = current_user.id
        dep.title = form.title.data
        dep.members = form.members.data
        dep.email = form.email.data
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/departments')
    return render_template('add_department.html', form=form, title='Добавление департамента')


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = AddDepartmentForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).get(id)
        if dep:
            if dep.chief == current_user.id or current_user.id == 1:
                form.title.data = dep.title
                form.members.data = dep.members
                form.email.data = dep.email
        else:
            abort(404)
            return render_template('notfound.html')
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).get(id)
        if dep and (dep.chief == current_user.id or current_user.id == 1):
            mems = form.members.data
            try:
                [int(i) for i in mems.split(', ')]
            except Exception as e:
                return render_template('add_department.html', message='Неправильно написаны ID сотрудников', form=form,
                                   title='Изменение департамента')
            dep.title = form.title.data
            dep.members = form.members.data
            dep.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
            return render_template('notfound.html')
    return render_template('add_department.html', title='Изменение департамента', form=form)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run()


if __name__ == '__main__':
    main()
