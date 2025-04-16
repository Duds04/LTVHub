from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import json
import time

import pandas as pd
from pipelines import calculate_LTV_and_Plot, readCSV, load_model
from src.DataTransformation.RFM import RFMTask

# Caminho para o arquivo de resultados persistentes
RESULTS_FILE = './output/results.json'

# Função para salvar os resultados no arquivo JSON
def save_results(csv_file_path, dfLTV_path, dfOriginal_path, weeksAhead, columns=None):
    results = {
        "csv_file_path": csv_file_path,
        "dfLTV_path": dfLTV_path,
        "dfOriginal_path": dfOriginal_path,
        "weeksAhead": weeksAhead
    }
    if columns:
        results["columns"] = columns  # Salva as colunas no arquivo JSON
    with open(RESULTS_FILE, 'w') as file:
        json.dump(results, file, indent=4)

# Função para carregar os resultados do arquivo JSON
def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as file:
            return json.load(file)
    return None

# Inicializa a aplicação Flask
app = Flask(__name__, static_folder="../FrontEnd/public",
            template_folder="../FrontEnd/public")

# Permite requisições de diferentes origens (CORS)
CORS(app)

# Define a pasta onde os arquivos enviados serão armazenados
UPLOAD_FOLDER = './output/data'
IMAGE_FOLDER = './images'  # Adicione esta linha para definir a pasta de imagens

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Cria a pasta se ela não existir

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)  # Cria a pasta de imagens se ela não existir

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Adicione esta linha para configurar a pasta de imagens
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

# Variáveis globais
csv_file_path = None
weeksAhead = None
dfLTV = None
dfOriginal = None

# Variável global para mensagens de progresso
app.config['PROGRESS_MESSAGES'] = []
app.config['LAST_UPDATE'] = time.time()  # Timestamp da última atualização

# Rota para a página inicial


@app.route("/")
def index():
    return render_template("index.html")

# Rota para servir arquivos estáticos


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

# Rota para upload de arquivos


@app.route('/upload', methods=['POST'])
def upload_file():
    global csv_file_path
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo foi enviado."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo foi selecionado."}), 400

    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    csv_file_path = filename

    return jsonify({"message": "Arquivo enviado com sucesso."}), 200

# Rota para retornar as colunas do arquivo CSV
@app.route('/columns', methods=['GET'])
def columns():
    global csv_file_path
    try:
        # Verificar se o arquivo CSV foi enviado
        if csv_file_path is not None:
            with open(csv_file_path, 'r') as file:
                first_line = file.readline().strip()
                columns = [col for col in first_line.split(',') if col.strip()]
            
            # Salvar as colunas no arquivo results.json
            results = load_results() or {}
            save_results(
                results.get("csv_file_path", csv_file_path),
                results.get("dfLTV_path", ""),
                results.get("dfOriginal_path", ""),
                results.get("weeksAhead", None),
                columns=columns
            )
            
            return jsonify({"columns": columns}), 200
        else:
            # Caso o arquivo CSV não esteja disponível, pegar as colunas do results.json
            results = load_results()
            if results and "columns" in results:
                return jsonify({"columns": results["columns"]}), 200
            else:
                return jsonify({"error": "Nenhum arquivo foi processado ainda e as colunas não estão disponíveis.<br />Por favor, volte à tela inicial e envie um arquivo."}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao processar o arquivo: {e}"}), 500

# Rota para receber os dados do formulário    
@app.route('/submit_form', methods=['POST'])
def submit_form():
    """ Para adicionar um novo modelo, siga os seguintes passos:
            1. Criar a Classe do Modelo:
            - A classe deve ser criada no arquivo correspondente:
                - Para modelos de frequência: `src/TransactionModels/`
                - Para modelos monetários: `src/MonetaryModels/`
            - A classe deve herdar de `FrequencyModel`, `MonetaryModel` ou `Task`.

            2. Adicionar ao arquivo `Models.json`:
            - Adicione a entrada do modelo no respectivo grupo (`frequencyModels` ou `monetaryModels`):
            - O modelo deve conter as seguintes propriedades:
                - `id`: ID único do modelo
                - `model_task_name`: Nome da classe do modelo
                - `importer`: Import dinâmico da classe do modelo
                - `props`: Propriedades padrão do modelo (colocar todas as propriedades necessárias para o modelo executar)

            3. Carregar o Modelo Usando `load_model`:
                - Para carregar o modelo e usar no pipeline:
                - Exemplo:
                    model = load_model("frequencyModels",
                                        "NovoModeloID", {"param": 20})
     """
    global weeksAhead
    global csv_file_path
    global dfLTV
    global dfOriginal
    

    try:
        results = load_results()
        if csv_file_path is None:
            csv_file_path = results['csv_file_path'] if results else None
            print(f"results: {csv_file_path}")
        data = request.json
        data['weeksAhead'] = int(data['weeksAhead'])

        # Calcular os DataFrames
        dfLTV = calculate_LTV_and_Plot(
            data, csv_file_path, data['idColumn'], data['dateColumn'], data['amountColumn'], data["weeksAhead"]
        )
        dfOriginal = readCSV(
            csv_file_path, data['idColumn'], data['dateColumn'], data['amountColumn']
        )

        dfLTV_path = './output/dfLTV.csv'
        dfOriginal_path = './output/dfOriginal.csv'
        dfLTV.to_csv(dfLTV_path, index=True)
        dfOriginal.to_csv(dfOriginal_path, index=True)

        # Salvar os caminhos e weeksAhead no arquivo results.json
        save_results(csv_file_path, dfLTV_path, dfOriginal_path, data['weeksAhead'])

        return jsonify({"message": "Dados processados e salvos com sucesso."}), 200

    except Exception as e:
        print(f"Erro ao processar o formulário: {e}")
        return jsonify({"error": f"Erro ao processar o formulário: {e}"}), 500

# Rota para retornar os clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    global dfLTV
    
    if dfLTV is None:
        results = load_results()
        if results and os.path.exists(results['dfLTV_path']):
            dfLTV = pd.read_csv(results['dfLTV_path'])
        else:
            return jsonify({"error": "O cálculo do LTV ainda não foi realizado.<br />Por favor, volte à tela 'Modelo' e envie as informações para continuar."}), 400
    
    clientes = dfLTV.to_dict(orient='records')
    return jsonify(clientes), 200
   
# Rota para retornar os dados de um cliente específico
@app.route('/cliente/<int:id>', methods=['GET'])
def get_cliente(id):
    global dfLTV
    global dfOriginal
    
    if dfLTV is None or dfOriginal is None:
        results = load_results()
        if results and os.path.exists(results['dfLTV_path']) and os.path.exists(results['dfOriginal_path']):
            dfLTV = pd.read_csv(results['dfLTV_path'])
            dfOriginal = pd.read_csv(results['dfOriginal_path'])
        else:
            return jsonify({"error": "O cálculo do LTV ainda não foi realizado.<br />Por favor, volte à tela 'Modelo' e envie as informações para continuar."}), 400
    

    cliente = dfLTV[dfLTV['id'] == id].to_dict(orient='records')
    if cliente:
        compras_cliente = dfOriginal[dfOriginal['id'] == id]
        compras_cliente = compras_cliente.reset_index(drop=True)
        compras_cliente['id_transaction'] = compras_cliente.index
        compras_cliente['date'] = pd.to_datetime(compras_cliente['date'], errors='coerce').dt.strftime('%d/%m/%Y')
        transactions = compras_cliente[[
            'id_transaction', 'monetary', 'date']].to_dict(orient='records')
        cliente[0]['transactions'] = transactions
        return jsonify(cliente[0]), 200
    else:
        return jsonify({"error": "Cliente não encontrado."}), 404

@app.route('/weeksahead', methods=['GET'])
def get_weeks_ahead():
    global weeksAhead
    try:
        if weeksAhead is not None:
            return jsonify({"weeksAhead": weeksAhead}), 200
        else:
            results = load_results()
            if results and "weeksAhead" in results:
                weeksAhead = results["weeksAhead"]
                return jsonify({"weeksAhead": weeksAhead}), 200
            else:
                return jsonify({"error": "Nenhum valor de weeksAhead encontrado."}), 400
    except Exception as e:    
        return jsonify({"error": "O cálculo do LTV ainda não foi realizado.<br />Por favor, volte à tela 'Modelo' e envie as informações para continuar."}), 400


# Rota para servir imagens da pasta de imagens
@app.route('/images/<path:filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)

# Rota para retornar os modelos de frequência e monetário
@app.route('/models', methods=['GET'])
def get_models():
    try:
        with open('./jsons/Models.json', 'r') as file:
            models = json.load(file)
        return jsonify(models), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao carregar os modelos: {e}"}), 500

# Rota para retornar os dados de plotagem
@app.route('/plot_data', methods=['GET'])
def get_plot_data():
    try:
        with open('./output/plot_data.json', 'r') as file:
            plot_data = json.load(file)
        return jsonify(plot_data), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao carregar os dados de plotagem: {e}"}), 500

@app.route('/progress', methods=['GET'])
def get_progress():
    # Obter o timestamp da última atualização enviado pelo frontend
    last_request_time = float(request.args.get('last_update', 0))

    # Verificar se há novas mensagens
    if app.config['LAST_UPDATE'] > last_request_time:
        return jsonify({
            "messages": app.config['PROGRESS_MESSAGES'],
            "last_update": app.config['LAST_UPDATE']
        }), 200
    else:
        # Nenhuma atualização
        return jsonify({"messages": [], "last_update": app.config['LAST_UPDATE']}), 204

# Exemplo de função que atualiza as mensagens de progresso
def add_progress_message(message):
    app.config['PROGRESS_MESSAGES'].append(message)
    app.config['LAST_UPDATE'] = time.time()  # Atualizar o timestamp

# Inicia a aplicação Flask
if __name__ == "__main__":
    app.run(debug=True)
