from urllib.parse import urlencode
from flask import Flask, request, render_template, redirect
import mysql.connector
#Conexao com o banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1324",
    database="comp"
)
# Verifica se o e-mail já está cadastrado
def verificar_email_cadastrado(email):
    cursor = mydb.cursor()
    sql = "SELECT * FROM usuarios WHERE email = %s"
    val = (email,)
    cursor.execute(sql, val)
    usuario = cursor.fetchone()
    cursor.close()
    return usuario is not None

def verificar_login(email, senha):
    cursor = mydb.cursor()
    sql = "SELECT * FROM usuarios WHERE email = %s AND senha = MD5(%s)"
    val = (email, senha)
    cursor.execute(sql, val)
    usuario = cursor.fetchone()  # Recupera a primeira linha do resultado da consulta
    cursor.close()
    return usuario is not None  # Se usuário existir, retorna True

#config padrao 
app = Flask(__name__)
app.config["SECRET_KEY"] = "IGORKEVEN"


#route padrao 
@app.route("/")
def home():
    return render_template('Inicio.html')

@app.route('/login')
def login():
    

    return render_template('login.html')

@app.route('/Cadastro')
def cadastro():
    return render_template('Cadastro.html')

@app.route('/Tela')
def tela():
    return render_template('Tela.html')


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
            return render_template("CriarConta.html")
        
        # Verifica se o e-mail já está cadastrado
        if verificar_email_cadastrado(email):
            return render_template("CriarConta.html")
        
        # Inserção dos dados na tabela de usuários
        cursor = mydb.cursor()
        sql = "INSERT INTO usuarios (username, email, senha) VALUES (%s, %s, MD5(%s))"
        val = (nome, email, senha)
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()
        
        #TODO redirecionar para a uma tela principal /home
        return render_template("Tela.html")
    else:
        return render_template("CriarConta.html")


@app.route("/logando", methods=["POST"])
def logando():
    email = request.form.get("email")
    senha = request.form.get("senha")
    if verificar_login(email, senha):
        # Usuário autenticado
        return render_template("Tela.html") # Redirecionar para a página de tela
    else:
        # Credenciais inválidas
        return render_template("login.html")
   

    
@app.route("/tela", methods=["GET", "POST"])
def tela2():
    cursor = mydb.cursor(dictionary=True)

    if request.method == "GET":
        pesquisa = request.args.get("pesquisa", "")
        marca = request.args.get("marca", "")
        site = request.args.get("site", "")
        preco_min = request.args.get("preco_min", "")
        preco_max = request.args.get("preco_max", "")

        sql = "SELECT * FROM produto WHERE 1=1"
        val = ()

        if pesquisa:
            sql += " AND (Nome LIKE %s OR Marca LIKE %s)"
            val += ("%" + pesquisa + "%", "%" + pesquisa + "%")

        if marca:
            sql += " AND Marca = %s"
            val += (marca,)

        if site:
            sql += " AND Site = %s"
            val += (site,)

        if preco_min:
            sql += " AND Preco >= %s"
            val += (preco_min,)

        if preco_max:
            sql += " AND Preco <= %s"
            val += (preco_max,)

        cursor.execute(sql, val)
        produtos = cursor.fetchall()

    cursor.close()
    return render_template("Tela.html", produtos=produtos)


@app.route("/produto")
def produto():
    nome_produto = request.args.get("nome")
    imagem_produto = request.args.get("imagem")
    return render_template("Produto.html", nome_produto=nome_produto, imagem_produto=imagem_produto)


if __name__ == "__main__":
    app.run(debug=True)
