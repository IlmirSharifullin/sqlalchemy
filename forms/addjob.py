from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Работа', validators=[DataRequired()])
    work_size = StringField('Объем работы', validators=[DataRequired()])
    collaborators = StringField('Сотрудники (через ", ")', validators=[DataRequired()])
    is_finished = BooleanField('Закончено')
    submit = SubmitField('Добавить')
