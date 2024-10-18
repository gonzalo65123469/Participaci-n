from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'clave_secreta_muy_segura'  # Necesaria para manejar las sesiones de manera segura

# Simulación de una base de datos de usuarios
users = {}

# Ruta para la página de inicio donde se encuentra el formulario de inicio de sesión
@app.route('/')
def index():
    return render_template('login.html')

# Ruta para manejar el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Verifica si el usuario existe en la "base de datos"
    if username in users and check_password_hash(users[username], password):
        session['username'] = username  # Guarda el usuario en la sesión
        flash('Inicio de sesión exitoso', 'success')
        return redirect(url_for('welcome'))
    else:
        flash('Nombre de usuario o contraseña incorrectos', 'error')
        return redirect(url_for('index'))

# Ruta para manejar el registro de nuevos usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verifica que el usuario no esté registrado ya
        if username in users:
            flash('El usuario ya está registrado', 'error')
            return redirect(url_for('register'))
        
        # Almacena el nuevo usuario con la contraseña encriptada
        users[username] = generate_password_hash(password)
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')

# Ruta para mostrar la página de bienvenida una vez autenticado
@app.route('/welcome')
def welcome():
    if 'username' in session:
        username = session['username']
        return render_template('welcome.html', username=username)
    else:
        flash('Por favor, inicia sesión primero', 'error')
        return redirect(url_for('index'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)  # Elimina el usuario de la sesión
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('index'))

# Ruta para ver la lista de usuarios registrados (solo si está autenticado)
@app.route('/users')
def users_list():
    if 'username' in session:
        return render_template('users.html', users=users)
    else:
        flash('Por favor, inicia sesión primero', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
