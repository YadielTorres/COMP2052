import os
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '-llave_secreta'

# Configuracion de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Si un usuario no autenticado intenta acceder a una ruta protegida, lo redirigira a la vista 'login'
login_manager.login_view = 'login'
# Mensaje que se mostrara al redirigir al usuario.
login_manager.login_message = 'Inicia sesion para acceder a esta pagina.'
login_manager.login_message_category = 'info' # Categoria para el mensaje flash


users_db = {
    'usuario1': {
        'id': '1',
        'username': 'usuario1',
        # Contraseña hasheada para 'password123'
        'password_hash': generate_password_hash('password123', method='pbkdf2:sha256'),
        'role': 'user'
    },
    'admin': {
        'id': '2',
        'username': 'admin',
        # Contraseña hasheada para 'adminpass'
        'password_hash': generate_password_hash('adminpass', method='pbkdf2:sha256'),
        'role': 'admin'
    }
}

# La clase User DEBE heredar de UserMixin para funcionar con Flask Login
class User(UserMixin):
    def __init__(self, id, username, password_hash, role):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

    # Metodo para verificar la contraseña ingresada contra el hash almacenado
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# User Loader para Flask Login
@login_manager.user_loader
def load_user(user_id):
    # Buscamos el usuario por su ID
    for user_data in users_db.values():
        if user_data['id'] == user_id:
            return User(id=user_data['id'],
                        username=user_data['username'],
                        password_hash=user_data['password_hash'],
                        role=user_data['role'])
    return None # Si no se encuentra el usuario, return None

# Rutas de la Aplicacion
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario autentifica, entonces redirige a la pagina protegida
    if current_user.is_authenticated:
        return redirect(url_for('protected'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Buscar el usuario
        user_data = users_db.get(username)

        # Verificar si el usuario existe y la contraseña es correcta
        if user_data:
            user = User(id=user_data['id'], username=user_data['username'],
                        password_hash=user_data['password_hash'], role=user_data['role'])
            if user.check_password(password):
                # Contraseña correcta: iniciar sesion
                login_user(user) # Flask login maneja la sesion
                flash('Inicio de sesion exitoso', 'success')
                # Redirige a la pagina que intentaba acceder o a la protegida
                next_page = request.args.get('next')
                return redirect(next_page or url_for('protected'))
            else:
                # Contraseña incorrecta
                flash('Usuario o contraseña incorrectos.', 'danger')
        else:
            # Usuario no encontrado
            flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required # Solo usuarios logueados pueden desloguearse
def logout():
    logout_user()
    flash('Has cerrado sesion.', 'success')
    return redirect(url_for('home'))

@app.route('/protegido')
@login_required
def protected():
    # current_user es un proxy al objeto User de load_user
    return render_template('protected.html', username=current_user.username, role=current_user.role)

if __name__ == '__main__':
    app.run(debug=True)