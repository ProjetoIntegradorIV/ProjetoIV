from builtins import str

import numpy as np
from flask import Flask, request, render_template, make_response
import joblib
import sklearn.externals

app = Flask(__name__)
model = joblib.load('templates/arquivo.pkl')


@app.route('/')
def exibir_gui():
    return render_template('projeto.html', partial='time.html')


@app.route('/resultado', methods=['POST'])
def resultado():
    duracao = str(request.form['dur_emp'])
    status_emp = str(request.form['status_emp'])
    valor_emprestimo = str(request.form['money'])
    valor_sem_ponto = valor_emprestimo.replace(".", "").replace(",", "")

    poupanca = str(request.form['valor'])
    poupanca_sem_ponto = poupanca.replace(".", "").replace(",", "")
    tempo_empregado = str(request.form['tempo'])
    sexo = str(request.form['Sexo'])
    idade = str(request.form['idade'])
    moradia = request.form['moradia']
    situacao_trabalho = request.form['situacao_trabalho']
    if situacao_trabalho == "1 - Desempregado e não qualificado":
        valor = 1
    elif situacao_trabalho == "2 - Desempregado e qualificado":
        valor = 2
    elif situacao_trabalho == "3 - Empregado":
        valor = 3
    elif situacao_trabalho == "4 - Empregado e altamente qualificado":
        valor = 4
    else:
        valor = None

    dados_usuario = np.array([[duracao, status_emp, valor_sem_ponto, poupanca_sem_ponto,
                               tempo_empregado, sexo, idade, moradia, valor]])

    resultado = model.predict(dados_usuario)

    if resultado[0] == 0:
        classe = 'Aprovado'
    else:
        classe = 'Reprovado'

    # Renderize o template 'resultado.html' e passe a classe como argumento
    return render_template('resultado.html', classe=classe)


@app.route('/Projeto&Time')
def projetoeTime():
    return render_template('time.html')

@app.route('/Formulário')
def formulario():
    return render_template('projeto.html')


if __name__ == '__main__':
    app.run('localhost', 9090)



