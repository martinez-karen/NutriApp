from flask import Flask, render_template, request, redirect, url_for, flash, session 

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
