from flask import Flask, render_template, flash, redirect, url_for, request
from forms import RegistrationForm
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24) # Genera clave segura al iniciar


@app.route('/', methods=['GET', 'POST'])
def index_register():

    form = RegistrationForm()
    if form.validate_on_submit():
        user_name = form.name.data
        # Simular registro exitoso
        flash(f'Cuenta creada exitosamente para {user_name}', 'success')
        return redirect(url_for('index_register')) # Redirige de vuelta a la misma pagina
    return render_template('register.html', title='Registro de Usuario', form=form)


if __name__ == '__main__':
    app.run()