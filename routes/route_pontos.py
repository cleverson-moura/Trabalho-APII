from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os

from models.pontos_turisticos_model import PontoTuristicoModel

ponto_bp = Blueprint('ponto', __name__, template_folder='../templates')

@ponto_bp.route('/pontos')
def listar_pontos():
    model = PontoTuristicoModel()
    pontos = model.buscar_todos()

    if 'usuario' in session:
        icone = "/static/{}".format(session['usuario']['imagem'])
        endereco = "/perfil_usuario"
    elif 'hotel' in session:
        icone = "/static/{}".format(session['hotel']['foto'])
        endereco = "/perfil_hotel"
    else:
        icone = "/static/imagens/user.png"
        endereco = "/login"

    return render_template('pontos.html', pontos=pontos, icone=icone, endereco=endereco)

@ponto_bp.route('/adicionar_ponto', methods=['GET', 'POST'])
def adicionar_ponto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        cidade = request.form['cidade']
        imagem = request.files['imagem']

        if imagem and imagem.filename != '':
            nome_arquivo = secure_filename(imagem.filename)
            caminho = os.path.join('static/uploads', nome_arquivo)
            imagem.save(caminho)
            imagem_path = f'uploads/{nome_arquivo}'
        else:
            imagem_path = 'imagens/default.png'

        ponto = PontoTuristicoModel(nome=nome, descricao=descricao, cidade=cidade, imagem=imagem_path)
        ponto.inserir()

        flash('Ponto turístico adicionado com sucesso!', 'success')
        return redirect(url_for('ponto.listar_pontos'))

    return render_template('ponto_turistico/adicionar.html')