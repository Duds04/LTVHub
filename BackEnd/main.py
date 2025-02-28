from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_cors import CORS
import os

import pandas as pd
from pipelines import calculate_LTV, readCSV
from src.TrasactionModels.TransactionModelRunner import TransactionModelRunner
from src.MonetaryModels.MonetaryModelRunner import MonetaryModelRunner

# Inicializa a aplicação Flask
app = Flask(__name__, static_folder="../FrontEnd/public",
            template_folder="../FrontEnd/public")

# Permite requisições de diferentes origens (CORS)
CORS(app)

# Define a pasta onde os arquivos enviados serão armazenados
UPLOAD_FOLDER = './data'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Cria a pasta se ela não existir

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Variáveis globais
csv_file_path = None
dfLTV = None 
dfOriginal = None

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
    # Declara a variável csv_file_path como global para poder acessá-la fora da função
    global csv_file_path
    if 'file' not in request.files:
        # Retorna erro se nenhum arquivo foi enviado
        return jsonify({"error": "Nenhum arquivo foi enviado."}), 400

    file = request.files['file']
    if file.filename == '':
        # Retorna erro se nenhum arquivo foi selecionado
        return jsonify({"error": "Nenhum arquivo foi selecionado."}), 400

    # Salva o arquivo na pasta configurada
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    # Armazena o caminho do arquivo CSV na variável global
    csv_file_path = filename

    # Retorna sucesso se o arquivo foi salvo
    return jsonify({"message": "Arquivo enviado com sucesso."}), 200

# Rota para retornar as colunas do arquivo CSV
@app.route('/columns', methods=['GET'])
def columns():
    global csv_file_path  # Declara a variável csv_file_path como global para acessá-la
    try:
        if csv_file_path is not None:
            with open(csv_file_path, 'r') as file:
                # Lê a primeira linha do arquivo CSV
                first_line = file.readline().strip()
                # Divide a linha pelos delimitadores de coluna (assumindo que é uma vírgula)
                columns = [col for col in first_line.split(',') if col.strip()]
            # Retorna as colunas da tabela
            return jsonify({"columns": columns}), 200
        else:
            # Retorna erro se csv_file_path não estiver definido
            return jsonify({"error": "Nenhum arquivo foi processado ainda.<br />Por favor, volte à tela inicial e envie um arquivo."}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao processar o arquivo: {e}"}), 500

# Nova rota para receber os dados do formulário
@app.route('/submit_form', methods=['POST'])
def submit_form():
    """ Para adicionar um novo modelo é necessário:
        Criar uma Task para aquele modelo (herdando da Task generica de seu tipo)
        Adicionar os novos atributos necessários para se usar esse modelo no seu respectivo ModelRunner (TransactionModelRunner ou Monetary Model Runner)
        Adicionar um novo if no método run de seu ModelRunner para associar o modelo a sua Task
        Adicionar um novo if no método submit_form para associar a chamada do modelo aos seus parâmetros
    """
    global dfLTV  # Declara a variável dfLTV como global para acessá-la
    global dfOriginal
    

    try:
        data = request.json
        data['weeksAhead'] = float(data['weeksAhead'])
        print(data)
        
        if data['frequencyModel'] == "MachineLearning":
            transactionModel = TransactionModelRunner("transaction_model", model = data['frequencyModel'], target="frequency", X_Columns=[
                                                      'frequency', 'recency', 'T', 'monetary_value'])
        else:
            transactionModel = TransactionModelRunner(
                "transaction_model", data['frequencyModel'], isRating=True, numPeriods=data['weeksAhead'])

        if data['monetaryModel'] == "MachineLearning":
            monetaryModel = MonetaryModelRunner(name="monetary_model", model=data['monetaryModel'], target="monetary_value", X_Columns=[
                                                'frequency', 'recency', 'T', 'monetary_value'])
        else:
            monetaryModel = MonetaryModelRunner(
                name="monetary_model", model = data['monetaryModel'], isRating=True)

        print(transactionModel, monetaryModel)
        dfLTV = calculate_LTV(transactionModel, monetaryModel, csv_file_path,
                      data['idColumn'], data['dateColumn'], data['amountColumn'])
        
        
        dfOriginal = readCSV(csv_file_path, data['idColumn'], data['dateColumn'], data['amountColumn'])
        print(dfOriginal)
        
        return jsonify({"message": "Dados recebidos com sucesso."}), 200

    except Exception as e:
        print(f"Erro ao processar o formulário: {e}")
        return jsonify({"error": f"Erro ao processar o formulário: {e}"}), 500


# Nova rota para retornar os clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    global dfLTV  # Declara a variável dfLTV como global para acessá-la
    if dfLTV is not None:
        # Converte o DataFrame para uma lista de dicionários
        clientes = dfLTV.reset_index().to_dict(orient='records')
        
        # print(clientes)
        return jsonify(clientes), 200
        
    else:
        # Retorna erro se dfLTV não estiver definido
        return jsonify({"error": "O cálculo do LTV ainda não foi realizado.<br />Por favor, volte à tela 'Modelo' e envie as informações para continuar."}), 400
    
    # const searchString = `${client.id} ${client.type} ${client.frequency} ${client.LTV} ${client.monetary_value}`.toLowerCase();

# Nova rota para retornar os dados de um cliente específico
@app.route('/cliente/<int:id>', methods=['GET'])
def get_cliente(id):
    global dfLTV  # Declara a variável dfLTV como global para acessá-la
    global dfOriginal
    
    if dfLTV is not None and dfOriginal is not None:
        # Busca o cliente pelo ID
        cliente = dfLTV[dfLTV.index == id].to_dict(orient='records')
        if cliente:
            # Busca os dados de compra do cliente
            compras_cliente = dfOriginal[dfOriginal['id'] == id]
            compras_cliente = compras_cliente.reset_index(drop=True)
            compras_cliente['id_transaction'] = compras_cliente.index
            # Formata a data para o padrão brasileiro
            
            compras_cliente['date'] = compras_cliente['date'].apply(lambda x: x.strftime('%d/%m/%Y') if isinstance(x, pd.Timestamp) else x)
            
            transactions = compras_cliente[['id_transaction', 'monetary', 'date']].to_dict(orient='records')
            
            # Adiciona os dados de compra ao objeto do cliente
            cliente[0]['transactions'] = transactions
            
            return jsonify(cliente[0]), 200
        else:
            return jsonify({"error": "Cliente não encontrado."}), 404
    else:
        return jsonify({"error": "O cálculo do LTV ainda não foi realizado.<br />Por favor, volte à tela 'Modelo' e envie as informações para continuar."}), 400


# Inicia a aplicação Flask
if __name__ == "__main__":
    app.run(debug=True)
