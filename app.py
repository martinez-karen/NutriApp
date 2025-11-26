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
            return redirect(url_for('perfil'))
    
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

        # VALIDAR CREDENCIALESS
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
            return redirect(url_for('perfil.html'))
        
        flash('Perfil guardado correctamente.', 'success')
        return redirect(url_for('articulos'))

    return render_template('perfil.html')

@app.route('/articulos')
def articulos():
    return render_template("articulos.html")

@app.route('/calculadoraimc', methods=['GET', 'POST'])
def calculadoraimc():
    resultado = None
    if request.method ==  'POST':
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        imc = peso / (altura ** 2)
        resultado = round(peso/ (altura **2),2)
    return render_template("calculadoraimc.html", resultado=resultado)

@app.route('/calculadoratmb', methods=['GET', 'POST'])
def calculadoratmb():
    resultado = None  

    if request.method == 'POST':
        altura = float(request.form.get("altura"))
        peso = float(request.form.get("peso"))
        edad = int(request.form.get("edad"))
        sexo = request.form.get("sexo")

        if sexo == "hombre":
            resultado = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
        else:
            resultado = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)

        resultado = round(resultado, 2)

    return render_template("calculadoratmb.html", resultado=resultado)

@app.route('/calculadoragct', methods=['GET', 'POST'])
def calculadoragct():
    resultado = None

    if request.method == 'POST':
        tmb = float(request.form.get("tmb"))
        actividad = float(request.form.get("actividad"))

        resultado = round(tmb * actividad, 2)

    return render_template("calculadoragct.html", resultado=resultado)

@app.route('/macronutrientes', methods=['GET', 'POST'])
def macronutrientes():
    resultado = None  

    if request.method == 'POST':
        gct = float(request.form.get("calorias"))

        proteina = round((gct * 0.2) / 4, 2)
        grasa = round((gct * 0.25) / 9, 2)
        carbo = round((gct * 0.55) / 4, 2)

        resultado = {
            'proteina': proteina,
            'grasas': grasa,
            'carbs': carbo
        }

    return render_template("macronutrientes.html", resultado=resultado)

@app.route('/calculadorapesoideal', methods=['GET', 'POST'])
def calculadorapesoideal():
    resultado = None

    if request.method == 'POST':
        altura = float(request.form.get("altura"))
        sexo = request.form.get("sexo")

        if sexo == "hombre":
            resultado = altura - 100 - ((altura - 150) / 4)
        else:
            resultado = altura - 100 - ((altura - 150) / 2.5)

        resultado = round(resultado, 2)

    return render_template("calculadorapesoideal.html", resultado=resultado)


@app.route('/recetas', methods=['GET', 'POST'])
def recetas():
    biblioteca = [
        {"nombre": "Tostadas de Aguacate con Huevo", "tiempo": "desayuno", "dificultad": "fácil", "tipo": "saludable"},
        {"nombre": "Pollo con Verduras Salteadas", "tiempo": "comida", "dificultad": "media", "tipo": "saludable"},
        {"nombre": "Avena Frutal Rápida", "tiempo": "desayuno", "dificultad": "fácil", "tipo": "rápida"},
        {"nombre": "Wrap de Atún Ligero", "tiempo": "cena", "dificultad": "fácil", "tipo": "rápida"},
    ]

    recetas_filtradas = []

    if request.method == 'POST':
        tiempo = request.form.get("tiempo")
        dificultad = request.form.get("dificultad")
        tipo = request.form.get("tipo")

        for receta in biblioteca:
            if receta["tiempo"] == tiempo and receta["dificultad"] == dificultad and receta["tipo"] == tipo:
                recetas_filtradas.append(receta)

        return render_template(
            "recetas.html",
            resultado=True,
            recetas=recetas_filtradas,
            tiempo=tiempo,
            dificultad=dificultad,
            tipo=tipo
        )

    return render_template("recetas.html", resultado=False)


@app.route('/recetas/<nombre>')
def ver_receta(nombre):

    recetas = {
        "tostada_huevo": {
            "titulo": "Tostadas de Aguacate con Huevo",
            "tiempo": "10 minutos",
            "categoria": "Desayuno",
            "dificultad": "Fácil",
            "tipo": "Saludable",
            "ingredientes": [
                "1 huevo",
                "1 tostada horneada",
                "1/2 aguacate",
                "Sal y pimienta",
                "Limón al gusto"
            ],
            "preparacion": [
                "Cocina el huevo.",
                "Machaca el aguacate con sal y limón.",
                "Úntalo sobre la tostada.",
                "Agrega el huevo, sal y pimienta."
            ]
        },

        "pollo_verduras": {
            "titulo": "Pollo con Verduras Salteadas",
            "tiempo": "15 minutos",
            "categoria": "Comida",
            "dificultad": "Media",
            "tipo": "Saludable",
            "ingredientes": [
                "100 g de pechuga de pollo",
                "Verduras mixtas",
                "1 cda de aceite",
                "Sal y ajo en polvo"
            ],
            "preparacion": [
                "Cocina el pollo en trozos.",
                "Agrega las verduras.",
                "Sazona con sal y ajo.",
                "Saltea por 5-7 minutos."
            ]
        },

        "avena_frutal": {
            "titulo": "Avena Frutal Rápida",
            "tiempo": "10 minutos",
            "categoria": "Desayuno",
            "dificultad": "Fácil",
            "tipo": "Rápida",
            "ingredientes": [
                "1/2 taza de avena",
                "1 taza de agua",
                "1/2 plátano o fresas",
                "1 cdita de miel"
            ],
            "preparacion": [
                "Cocina la avena.",
                "Agrega la fruta.",
                "Endulza con miel.",
                "Mezcla y sirve."
            ]
        },

        "wrap_atun": {
            "titulo": "Wrap de Atún Ligero",
            "tiempo": "12 minutos",
            "categoria": "Cena",
            "dificultad": "Fácil",
            "tipo": "Rápida",
            "ingredientes": [
                "1 tortilla integral",
                "1 lata pequeña de atún",
                "Lechuga",
                "1 cda de mayonesa ligera",
                "Sal y limón"
            ],
            "preparacion": [
                "Mezcla el atún con mayonesa, sal y limón.",
                "Colócalo sobre la tortilla.",
                "Agrega lechuga.",
                "Enrolla y corta."
            ]
        }
    }

    receta = recetas.get(nombre)
    return render_template("combinacionesreceta.html", receta=receta)



recetas = {
    "ensalada de pollo": {"calorias": 350, "proteina": 30, "carbs": 20, "grasas": 15},
    "arroz con pollo": {"calorias": 500, "proteina": 25, "carbs": 60, "grasas": 18},
    "huevos revueltos": {"calorias": 200, "proteina": 12, "carbs": 2, "grasas": 15},
    "tacos de carne": {"calorias": 400, "proteina": 20, "carbs": 35, "grasas": 18},
    "sopa de verduras": {"calorias": 150, "proteina": 5, "carbs": 25, "grasas": 3}
}


@app.route('/analizador', methods=['GET', 'POST'])
def analizador():
    resultado = None
    mensaje_error = None

    if request.method == 'POST':
        receta = request.form.get("receta").lower()
        if receta in recetas:
            resultado = recetas[receta]
        else:
            mensaje_error = "Receta no encontrada. Intenta con otra."

    return render_template("analizador.html", resultado=resultado, mensaje_error=mensaje_error)

if __name__ == "__main__": 
    app.run(debug=True) 