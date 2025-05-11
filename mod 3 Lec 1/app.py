from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'key_123!@#'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Route to redirect to if @login_required fails
login_manager.login_message = "Debe iniciar sesión para acceder a esta página" # Custom message
login_manager.login_message_category = "warning" # Bootstrap category for flash message

# In-memory User Storage
users_db = {}  # Stores User objects: (user_id: User_object)
next_user_id = 1 # Auto-incrementing ID for new users


class User(UserMixin):
    """
    User model for Flask-Login
    Includes id, username, hashed password, and role.
    """
    def __init__(self, id, username, password_hash, role="user"):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role  # e.g., "user", "admin"

    def __repr__(self):
        return f'<User id={self.id} username={self.username} role={self.role}>'

    # Helper methods for password management (optional but good practice)
    def set_password(self, password):
        """Hashes and sets the password for the user"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Checks if the provided password matches the hashed password"""
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return users_db.get(int(user_id))

# Find user by username
def find_user_by_username(username):
    for user_obj in users_db.values():
        if user_obj.username == username:
            return user_obj
    return None


@app.route('/')
def index():
    """Serves the homepage."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("Ya ha iniciado sesión", "info")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        global next_user_id
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'user') # Default role to 'user' if not provided

        # Basic validation
        if not username or not password or not confirm_password:
            flash('Todos los campos son obligatorios', 'danger')
            return redirect(url_for('register'))
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('register'))
        if find_user_by_username(username):
            flash('El nombre de usuario ya existe. Por favor, elija otro', 'warning')
            return redirect(url_for('register'))

        # Create new user
        new_user = User(id=next_user_id, username=username, password_hash="", role=role)
        new_user.set_password(password) # Hash password

        users_db[next_user_id] = new_user
        next_user_id += 1

        flash('Registro exitoso, por favor inicie sesión', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login"""
    if current_user.is_authenticated:
        flash("Ya ha iniciado sesión", "info")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Se requiere nombre de usuario y contraseña.', 'danger')
            return redirect(url_for('login'))

        user = find_user_by_username(username)

        if user and user.check_password(password):
            login_user(user)
            flash('Inicio de sesión exitosa', 'success')
            
            # Redirect back to the page or to  dashboard
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Nombre de usuario o contraseña inválidos. Inténtalo de nuevo.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required # Only logged-in users can access this route
def logout():
    """Handles user logout"""
    logout_user() # Clears user's session
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('index'))

# Restricted Routes
@app.route('/dashboard')
@login_required # Protects the route
def dashboard():
    """Dashboard page accessible only to logged in users"""
    return render_template('dashboard.html')

@app.route('/profile')
@login_required
def profile():
    """Simple profile page"""
    return render_template('profile.html', user=current_user)




if __name__ == '__main__':
    app.run(debug=True)