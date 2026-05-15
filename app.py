from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Criar banco
def criar_banco():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT,
        nome TEXT,
        estoque INTEGER
    )
    """)

    conn.commit()
    conn.close()

criar_banco()

@app.route("/")
def home():
    return "Servidor funcionando"

app.run(debug=True)
@app.route("/produto", methods=["POST"])
def produto():

    dados = request.json

    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO produtos (sku, nome, estoque)
    VALUES (?, ?, ?)
    """, (
        dados["sku"],
        dados["nome"],
        dados["estoque"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"ok": True})

@app.route("/baixar", methods=["POST"])
def baixar():

    dados = request.json

    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE produtos
    SET estoque = estoque - 1
    WHERE sku = ?
    """, (dados["sku"],))

    conn.commit()
    conn.close()

    return jsonify({"ok": True})

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 login TEXT,
 senha TEXT
)
""")
@app.route("/login", methods=["POST"])
def login():

    dados = request.json

    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM usuarios
    WHERE login = ? AND senha = ?
    """, (
        dados["login"],
        dados["senha"]
    ))

    usuario = cursor.fetchone()

    conn.close()

    if usuario:
        return jsonify({"ok": True})

    return jsonify({"ok": False})
