from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class RegistrationForm(FlaskForm):
    """
    Formulario de registro de usuarios:
    
        name (StringField): Nombre del usuario. minimo 3 caracteres.
        email (StringField): Correo electronico del usuario. formato de email valido.
        password (PasswordField): Contraseña del usuario. minimo 6 caracteres.
        submit (SubmitField): Boton para enviar el formulario.
    """
    name = StringField('Nombre',
        validators=[DataRequired(message="El nombre es obligatorio."),
            Length(min=3, message="El nombre debe tener al menos 3 caracteres.")])
    
    email = StringField('Correo Electronico',
        validators=[DataRequired(message="El correo electronico es obligatorio."),
            Email(message="Por favor, introduce una dirección de correo válida.")])
    
    password = PasswordField('Contraseña',
        validators=[DataRequired(message="La contraseña es obligatoria."),
            Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")])
    
    submit = SubmitField('Registrarse')