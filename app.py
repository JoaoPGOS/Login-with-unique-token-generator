from flask import Flask, render_template, request, redirect, jsonify, session
import json
import os

app = Flask(__name__,template_folder='template')
app.secret_key = '0000'

@app.route('/', methods=['POST','GET'])
def home():
    return render_template('index.html')
@app.route('/home')
def ok():
    if session['usuario_autenticado'] == 1:
        return '<h1>Acesso Liberado</h1>'
    else:
        return '<h1>Sem acesso</h1>'

@app.route('/secondverification', methods=['POST'])
def verify():
    data = request.json
    if 'token' in data:
    # Obter dados do corpo da requisição
        data = request.json

        # Obter token e user do corpo da requisição
        token = data.get('token')
        user = data.get('user')

        if token and user:
            # Caminho para o arquivo JSON (caminho relativo ao script Flask)
            caminho_arquivo_json = os.path.join(os.path.dirname(__file__), 'template', 'token.json')

            # Abrir e carregar o conteúdo do arquivo JSON
            with open(caminho_arquivo_json, 'r') as arquivo_json:
                dados_json = json.load(arquivo_json)

            # Verificar se a chave 'user' existe no JSON e se seu valor é uma string vazia
            if user in dados_json and dados_json[user] == "":
                # Substituir o valor vazio pelo token
                dados_json[user] = token

                # Salvar as alterações de volta no arquivo JSON
                with open(caminho_arquivo_json, 'w') as arquivo_json:
                    json.dump(dados_json, arquivo_json, indent=2)
                return jsonify({'token': f'{token}','user':f'{user}'})
            else:
                if user in dados_json:
                    return jsonify({'status': 'Access Denied'})
                else:
                    return jsonify({'status': 'User is not in the allowed users list'})
            


    else:
        return jsonify({'error': 'Erro'})
    
@app.route('/verification', methods=['POST'])
def verification():
    token_user = request.json
    token = token_user.get('token')
    user = token_user.get('user')

    # Caminho para o arquivo JSON (caminho relativo ao script Flask)
    caminho_arquivo_json = os.path.join(os.path.dirname(__file__), 'template', 'token.json')

    # Abrir e carregar o conteúdo do arquivo JSON
    with open(caminho_arquivo_json, 'r') as arquivo_json:
        dados_json = json.load(arquivo_json)

    # Verificar se os valores de 'user' e 'token' existem no JSON
    if user in dados_json and token == dados_json[user]:
        # Se existirem, criar uma sessão
        session['usuario_autenticado'] = 1
        print('ok')
        return jsonify({'status': 'verified'})
    else:
        print('erro')
        return jsonify({'error': 'Usuário ou token inválidos'}), 401



if __name__ == '__main__':
    app.run(debug=True)