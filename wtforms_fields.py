from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, IntegerField, validators, SubmitField, BooleanField
from wtforms.validators import InputRequired, NumberRange, DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    """ Registration form """

    largo = DecimalField('largo_label', validators = [InputRequired(message = "Largo required"), NumberRange(min=0.0, max=12.0, message='Error')])
    diametro = DecimalField('diametro_label', validators = [InputRequired(message = "Diametro required"), NumberRange(min=0.0, max=None, message='Error')])
    cantidad = DecimalField('cantidad_label', validators = [InputRequired(message = "Cantidad required"), NumberRange(min=0.0, max=None, message='Error')])
    proyecto = StringField('cantidad_label', validators = [InputRequired(message = "Proyecto required")])
    etiqueta = StringField('cantidad_label', validators = [InputRequired(message = "Etiqueta required")])
    fecha = StringField('cantidad_label', validators = [InputRequired(message = "Fecha required")])
    submit = SubmitField('Submit')

class RegistrationUser(FlaskForm):
    """ Registration User Form """
    username = StringField('Username', 
                            validators = [DataRequired(), Length(min = 2, max = 20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                        validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    """ Login User Form """
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
