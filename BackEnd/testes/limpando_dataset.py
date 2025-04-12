import pandas as pd
from sklearn.preprocessing import StandardScaler

# Caminhos dos arquivos
ltv_file_path = "../output/data/id.csv"
transaction_file_path = "../output/data/transactions.csv"
filtered_transaction_file_path = "../output/data/filtered_transaction.csv"

# Carregar o dataset LTV
data = pd.read_csv(ltv_file_path)
print("Dataset LTV carregado com sucesso!")

# Verificar valores ausentes
if data.isnull().sum().any():
    print("Valores ausentes encontrados no dataset LTV. Preenchendo com a média...")
    data.fillna(data.mean(), inplace=True)

# Normalizar os dados do dataset LTV
if {'monetary_value', 'frequency'}.issubset(data.columns):
    scaler = StandardScaler()
    data[['monetary_value', 'frequency']] = scaler.fit_transform(data[['monetary_value', 'frequency']])
    print("Dados normalizados com sucesso!")
else:
    print("As colunas necessárias para normalização não estão presentes no dataset.")

# Critérios para identificar outliers
MONETARY_THRESHOLD = 1200  # Valores maiores que 100 são considerados outliers
FREQUENCY_THRESHOLD = 5   # Valores maiores que 8 são considerados outliers

# Identificar outliers na coluna 'monetary_value'
outlier_ids = set()
if 'monetary_value' in data.columns:
    monetary_outliers = data[data['monetary_value'] > MONETARY_THRESHOLD]
    print("Outliers na coluna 'monetary_value':")
    print(monetary_outliers[['id', 'monetary_value']])
    outlier_ids.update(monetary_outliers['id'].tolist())
else:
    print("A coluna 'monetary_value' não está presente no dataset.")

# Identificar outliers na coluna 'frequency'
if 'frequency' in data.columns:
    frequency_outliers = data[data['frequency'] > FREQUENCY_THRESHOLD]
    print("Outliers na coluna 'frequency':")
    print(frequency_outliers[['id', 'frequency']])
    outlier_ids.update(frequency_outliers['id'].tolist())
else:
    print("A coluna 'frequency' não está presente no dataset.")

# Carregar o arquivo de transações
transactions = pd.read_csv(transaction_file_path)
print("Dataset de transações carregado com sucesso!")

# Verificar valores ausentes no dataset de transações
if transactions.isnull().sum().any():
    print("Valores ausentes encontrados no dataset de transações. Preenchendo com a média...")
    transactions.fillna(transactions.mean(), inplace=True)

# Filtrar transações removendo os IDs dos outliers
filtered_transactions = transactions[~transactions['customer_id'].isin(outlier_ids)]
print(f"Número de transações antes do filtro: {len(transactions)}")
print(f"Número de transações após o filtro: {len(filtered_transactions)}")

# Salvar o arquivo filtrado
filtered_transactions.to_csv(filtered_transaction_file_path, index=False)
print(f"Arquivo filtrado salvo em: {filtered_transaction_file_path}")