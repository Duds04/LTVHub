from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_cors import CORS
import os

# Inicializa a aplicação Flask
app = Flask(__name__, static_folder="../FrontEnd/public", template_folder="../FrontEnd/public")

# Permite requisições de diferentes origens (CORS)
CORS(app)

# Define a pasta onde os arquivos enviados serão armazenados
UPLOAD_FOLDER = './src/DataBase'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Cria a pasta se ela não existir

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Variável global para armazenar o caminho do arquivo CSV
csv_file_path = None

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
    global csv_file_path  # Declara a variável csv_file_path como global para poder acessá-la fora da função
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo foi enviado."}), 400  # Retorna erro se nenhum arquivo foi enviado
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo foi selecionado."}), 400  # Retorna erro se nenhum arquivo foi selecionado
    
    # Salva o arquivo na pasta configurada
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    
    # Armazena o caminho do arquivo CSV na variável global
    csv_file_path = filename
    
    return jsonify({"message": "Arquivo enviado com sucesso."}), 200  # Retorna sucesso se o arquivo foi salvo

# Rota para retornar as colunas do arquivo CSV
@app.route('/columns', methods=['GET'])
def columns():
    global csv_file_path  # Declara a variável csv_file_path como global para acessá-la
    if csv_file_path is not None:
        with open(csv_file_path, 'r') as file:
            # Lê a primeira linha do arquivo CSV
            first_line = file.readline().strip()
            # Divide a linha pelos delimitadores de coluna (assumindo que é uma vírgula)
            columns = [col for col in first_line.split(',') if col.strip()]
        return jsonify({"columns": columns}), 200  # Retorna as colunas da tabela
    else:
        return jsonify({"error": "Nenhum arquivo foi processado ainda."}), 400  # Retorna erro se csv_file_path não estiver definido

# Nova rota para receber os dados do formulário
@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.json
    # Processar os dados recebidos
    print(data)
    return jsonify({"message": "Dados recebidos com sucesso."}), 200



# Inicia a aplicação Flask
if __name__ == "__main__":
    app.run(debug=True)