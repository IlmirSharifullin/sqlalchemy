from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, StringField, EmailField
from wtforms.validators import DataRequired


class AddDepartmentForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    members = StringField('ID сотрудников (через ", ")', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField('Добавить')
