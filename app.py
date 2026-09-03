from flask import Flask, render_template, request
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "dbname": os.environ.get("DB_NAME", "practica04_bd")
}

def conectar():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/saludar", methods=["POST"])
def f_saludar():
    nombre = request.form["nombre"]
    pasatiempos = request.form.getlist("pasatiempos")
    me_gusta = request.form["me_gusta"]

    pasatiempos_texto = ", ".join(pasatiempos)

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO alumnos (nombre, pasatiempos, me_gusta)
        VALUES (%s, %s, %s)
    """, (nombre, pasatiempos_texto, me_gusta))
    conexion.commit()
    cursor.close()
    conexion.close()

    return render_template(
        "saludar.html",
        nombre=nombre,
        pasatiempos=pasatiempos,
        me_gusta=me_gusta
    )

@app.route("/alumnos")
def listar_alumnos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM alumnos ORDER BY id")
    alumnos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template(
        "listar_alumnos.html",
        alumnos=alumnos
    )

@app.route("/debug")
def debug():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT current_database(), current_user, current_schema();")
    resultado = cursor.fetchone()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tablas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return f"Base de datos: {resultado[0]}, Usuario: {resultado[1]}, Esquema: {resultado[2]}, Tablas: {tablas}"

if __name__ == "__main__":
    app.run(debug=True)