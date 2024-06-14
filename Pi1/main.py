
from flask import Flask, request, render_template, redirect
import mysql.connector
#Conexao com o banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="comp"
)

#config padrao 
app = Flask(__name__)
app.config["SECRET_KEY"] = "IGORKEVEN"

def verificar_login(email, senha):
    cursor = mydb.cursor()
    sql = "SELECT * FROM usuarios WHERE email = %s AND senha = MD5(%s)"
    val = (email, senha)
    cursor.execute(sql, val)
    usuario = cursor.fetchone()  # Recupera a primeira linha do resultado da consulta
    cursor.close()
    return usuario is not None  # Se usuário existir, retorna True

# Verifica se o e-mail já está cadastrado
def verificar_email_cadastrado(email):
    cursor = mydb.cursor()
    sql = "SELECT * FROM usuarios WHERE email = %s"
    val = (email,)
    cursor.execute(sql, val)
    usuario = cursor.fetchone()
    cursor.close()
    return usuario is not None

#route padrao 
@app.route("/")
def home():
    return render_template('login.html')

#route da tela de login 
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    senha = request.form.get("senha")
    if verificar_login(email, senha):
        # Usuário autenticado
        return "Usuário autenticado. Faça o que desejar."
    else:
        # Credenciais inválidas
        return "Credenciais inválidas. Por favor, tente novamente."

#route da tela de Criar Conta
@app.route("/CriarConta", methods=["GET","POST"])
def CriarConta():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha1")
        Csenha = request.form.get("senha2")

        #Verifica se as senhas sao iguais
        #TODO fazer uma mensagem na tela 
        if senha != Csenha:
            return "As senhas não coincidem. Tente novamente."
        
        # Verifica se o e-mail já está cadastrado
        if verificar_email_cadastrado(email):
            return "Este e-mail já está cadastrado. Por favor, use um e-mail novo."
        
        # Inserção dos dados na tabela de usuários
        cursor = mydb.cursor()
        sql = "INSERT INTO usuarios (username, email, senha) VALUES (%s, %s, MD5(%s))"
        val = (nome, email, senha)
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()
        
        #TODO redirecionar para a uma tela principal /home
        return redirect("/")
    else:
        return render_template("CriarConta.html")

if __name__ == "__main__":
    app.run(debug=True)
