from flask import Flask, render_template, request, redirect, url_for, flash, session 

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"


@app.route('/')
def index():
    return render_template("index.html")


#USUARIOS DEFINIDOS (simulando base de datos) 
USUARIOS_REGISTRADOS = {
    'admin@gmail.com' : {
        'password' : 'Admin123',
        'nombre' : 'Administrador',
        'fecha_nacimiento' : '1985-11-28'
    },
    'usuario@correo.com' : {
        'password' : 'usuario123',
        'nombre' : 'Karime Cruz',
        'fecha_nacimiento' : '2009-12-17'
    } 
}

app.config['SECRET_KEY'] = 'Mimecita123'


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        error = None
        Nombre = request.form.get("nombre")
        Apellido = request.form.get("apellido")
        fecha = request.form.get("fecha")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")
        genero = request.form.get("genero")

        if password != confirmPassword:
            error = "Las contraseñas no coinciden" 

        if error is not None:
            flash(error)
            return render_template('registro.html')
        else:
            flash(f"Registro exitoso!: {Nombre}")
            return render_template('index.html')
    
    return render_template('registro.html') 


@app.route('/iniciodesesion', methods=['GET'])
def iniciodesesion():
    if session.get('iniciodesesion'):
        return redirect(url_for("index.html"))
    return render_template("iniciodesesion.html")

@app.route('/cerrarsesion')
def cerrarsesion():
    session.clear()
    flash('Haz cerrado sesion', 'success')
    return redirect(url_for('iniciodesesion.html'))


@app.route('/validainiciodesesion', methods=['POST'])
def validainiciodesesion():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # VALIDAR CREDENCIALES
        if not email or not password:
            flash('Por favor ingresa email y contraseña','error')
        elif email in USUARIOS_REGISTRADOS:
            usuario = USUARIOS_REGISTRADOS[email]
            if usuario['password'] == password:
                # CREDENCIALES CORRECTAS
                session['usuario_email'] = email
                session['usuario'] = usuario['nombre']
                session['iniciodesesion'] = True
                return redirect(url_for('index.html'))
            else:
                flash('Contraseña incorrecta','error')
        else:
            flash('Usuario no encontrado','error')


    return render_template("iniciodesesion.html")

if __name__ == "__main__":
    app.run(debug=True)
