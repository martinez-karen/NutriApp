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
            flash(f"Registro exitoso!, {Nombre}!", 'success')
            return redirect(url_for('perfil.html'))
    
    return render_template('registro.html') 


@app.route('/iniciodesesion', methods=['GET'])
def iniciodesesion():
    if session.get('iniciodesesion'):
        return redirect(url_for("perfil"))
    return render_template("iniciodesesion.html")

@app.route('/cerrarsesion')
def cerrarsesion():
    session.clear()
    flash('Haz cerrado sesion', 'success')
    return redirect(url_for('iniciodesesion'))


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
                return redirect(url_for('perfil'))
            else:
                flash('Contraseña incorrecta','error')
        else:
            flash('Usuario no encontrado','error')


    return render_template("iniciodesesion.html")


@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == 'POST':
        edad = request.form.get('edad')
        sexo = request.form.get('sexo')
        peso = request.form.get('peso')
        altura = request.form.get('altura')
        actividad = request.form.get('actividad')
        objetivo = request.form.get('objetivo')
        alergias = request.form.get('alergias')
        intolerancias = request.form.get('intolerancias')
        dieta = request.form.get('dieta')
        alimentos_no = request.form.get('alimentos_no')
        experiencia = request.form.get('experiencia')
        text= request.form.get('text')
        busqueda = request.form.getlist('busqueda')

        if not edad or not sexo or not peso or not altura or not text or not busqueda:
            flash('¡Completa todos los campos antes de guardar!', 'danger')
            return redirect(url_for('perfil'))
        
        flash('Perfil guardado correctamente.', 'success')
        return redirect(url_for('articulos'))

    return render_template('perfil.html')

@app.route('/articulos')
def articulos():
    return render_template("articulos.html")

if __name__ == "__main__":
    app.run(debug=True)
