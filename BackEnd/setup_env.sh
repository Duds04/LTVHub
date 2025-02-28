#!/bin/bash

# Nome do ambiente virtual
ENV_DIR="ambiente_exec"

# Cria o ambiente virtual se não existir
if [ ! -d "$ENV_DIR" ]; then
  echo "Criando o ambiente virtual..."
  python3 -m venv ambiente_exec
fi

# Ativa o ambiente virtual
echo "Ativando o ambiente virtual..."
source ambiente_exec/bin/activate

# Instala as dependências
echo "Instalando dependências..."
pip install pandas numpy xgboost lightgbm scikit-learn lifetimes flask flask-cors seaborn

# Executa o script Python
#echo "Executando o script main.py..."
#python3 main.py

# Desativar o ambiente virtual
# echo "Desativando o ambiente virtual..."
# deactivate

echo "Processo concluído."

