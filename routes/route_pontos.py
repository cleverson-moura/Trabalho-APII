from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os

from models.pontos_turisticos_model import PontoTuristicoModel

ponto_bp = Blueprint('ponto', __name__, template_folder='../templates')

# A função 'listar_pontos' pode continuar a mesma por enquanto,
# mas lembre-se que ela agora recebe 'imagem_capa' do banco de dados.

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


@ponto_bp.route('/adicionar_ponto', methods=['POST'])
def adicionar_ponto():
    # Coleta os dados do formulário
    nome = request.form['nome']
    descricao = request.form['descricao']
    cidade = request.form['cidade']
    bairro = request.form['bairro']
    rua = request.form['rua']

    # 1. Insere os dados de texto e obtém o ID do novo ponto
    ponto_model = PontoTuristicoModel(nome=nome, descricao=descricao, cidade=cidade, bairro=bairro, rua=rua)
    id_novo_ponto = ponto_model.inserir()

    # 2. Processa e salva os arquivos de imagem
    imagens_para_salvar = {}
    
    # Lista com os nomes dos inputs de imagem no HTML
    nomes_dos_inputs = ['imagem_capa', 'imagem_extra_1', 'imagem_extra_2', 'imagem_extra_3', 'imagem_extra_4']

    for nome_input in nomes_dos_inputs:
        imagem_file = request.files.get(nome_input)
        
        if imagem_file and imagem_file.filename != '':
            # Garante que o nome do arquivo é seguro
            nome_arquivo = secure_filename(imagem_file.filename)
            # Define o caminho para salvar o arquivo
            caminho_salvar = os.path.join('static/uploads', nome_arquivo)
            # Salva o arquivo no disco
            imagem_file.save(caminho_salvar)
            # Guarda o caminho relativo para salvar no banco
            imagens_para_salvar[nome_input] = f'uploads/{nome_arquivo}'

    # 3. Se alguma imagem foi enviada, insere os caminhos no banco
    if imagens_para_salvar:
        ponto_model.inserir_imagens(id_novo_ponto, imagens_para_salvar)

    flash('Ponto turístico adicionado com sucesso!', 'success')
    return redirect(url_for('ponto.listar_pontos'))


@ponto_bp.route('/pontos/<int:id_ponto>')
def detalhes_ponto(id_ponto):
    model = PontoTuristicoModel()
    ponto = model.buscar_por_id(id_ponto)

    if not ponto:
        flash("Ponto turístico não encontrado!", "danger")
        return redirect(url_for("ponto.listar_pontos"))

    # Lógica para pegar ícone e endereço do perfil
    if 'usuario' in session:
        icone = "/static/{}".format(session['usuario']['imagem'])
        endereco = "/perfil_usuario"
    elif 'hotel' in session:
        icone = "/static/{}".format(session['hotel']['foto'])
        endereco = "/perfil_hotel"
    else:
        icone = "/static/imagens/user.png"
        endereco = "/login"

    return render_template(
        "detalhes_ponto.html",
        ponto=ponto,
        icone=icone,
        endereco=endereco
    )
