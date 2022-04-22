from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class AddDepartmentForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    members = StringField('ID сотрудников (через ", ")', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField('Добавить')
