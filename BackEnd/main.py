from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_cors import CORS
import os

import pandas as pd
from pipelines import calculate_LTV_and_Plot, readCSV
from src.TrasactionModels.TransactionModelRunner import TransactionModelRunner
from src.MonetaryModels.MonetaryModelRunner import MonetaryModelRunner

# Inicializa a aplicação Flask
app = Flask(__name__, static_folder="../FrontEnd/public",
            template_folder="../FrontEnd/public")

# Permite requisições de diferentes origens (CORS)
CORS(app)

# Define a pasta onde os arquivos enviados serão armazenados
UPLOAD_FOLDER = './data'
IMAGE_FOLDER = './images'  # Adicione esta linha para definir a pasta de imagens

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Cria a pasta se ela não existir

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)  # Cria a pasta de imagens se ela não existir

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER  # Adicione esta linha para configurar a pasta de imagens

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
        if csv_file_path is not None:
            with open(csv_file_path, 'r') as file:
                first_line = file.readline().strip()
                columns = [col for col in first_line.split(',') if col.strip()]
            return jsonify({"columns": columns}), 200
        else:
            return jsonify({"error": "Nenhum arquivo foi processado ainda.<br />Por favor, volte à tela inicial e envie um arquivo."}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao processar o arquivo: {e}"}), 500

# Rota para receber os dados do formulário
@app.route('/submit_form', methods=['POST'])
def submit_form():
    global dfLTV
    global dfOriginal

    try:
        data = request.json
        data['weeksAhead'] = float(data['weeksAhead'])
        
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

        dfLTV = calculate_LTV_and_Plot(transactionModel, monetaryModel, csv_file_path,
                      data['idColumn'], data['dateColumn'], data['amountColumn'])
        
        print(dfLTV)
        
        dfOriginal = readCSV(csv_file_path, data['idColumn'], data['dateColumn'], data['amountColumn'])
        
        return jsonify({"message": "Dados recebidos com sucesso."}), 200

    except Exception as e:
        print(f"Erro ao processar o formulário: {e}")
        return jsonify({"error": f"Erro ao processar o formulário: {e}"}), 500

# Rota para retornar os clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    global dfLTV
    if dfLTV is not None:
        clientes = dfLTV.reset_index().to_dict(orient='records')
        return jsonify(clientes), 200
    else:
        return jsonify({"error": "O cálculo do LTV ainda não foi realizado.<br />Por favor, volte à tela 'Modelo' e envie as informações para continuar."}), 400

# Rota para retornar os dados de um cliente específico
@app.route('/cliente/<int:id>', methods=['GET'])
def get_cliente(id):
    global dfLTV
    global dfOriginal
    
    if dfLTV is not None and dfOriginal is not None:
        cliente = dfLTV[dfLTV.index == id].to_dict(orient='records')
        
        if cliente:
            compras_cliente = dfOriginal[dfOriginal['id'] == id]
            compras_cliente = compras_cliente.reset_index(drop=True)
            compras_cliente['id_transaction'] = compras_cliente.index
            compras_cliente['date'] = compras_cliente['date'].apply(lambda x: x.strftime('%d/%m/%Y') if isinstance(x, pd.Timestamp) else x)
            transactions = compras_cliente[['id_transaction', 'monetary', 'date']].to_dict(orient='records')
            cliente[0]['transactions'] = transactions
            return jsonify(cliente[0]), 200
        else:
            return jsonify({"error": "Cliente não encontrado."}), 404
    else:
        return jsonify({"error": "O cálculo do LTV ainda não foi realizado.<br />Por favor, volte à tela 'Modelo' e envie as informações para continuar."}), 400

# Rota para servir imagens da pasta de imagens
@app.route('/images/<path:filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)

# Inicia a aplicação Flask
if __name__ == "__main__":
    app.run(debug=True)