import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Caminho do arquivo
file_path = "./output/ltv_results.csv"

# Criar diretório para salvar os gráficos, se não existir
output_dir = "./output/plots/"
os.makedirs(output_dir, exist_ok=True)

# Carregar o dataset
data = pd.read_csv(file_path)
print("Dataset carregado com sucesso!")
print(data.head())  # Exibe as primeiras linhas do dataset
print(data.columns)  # Exibe as colunas do dataset

# Função para calcular outliers e retornar o menor valor de outlier
def calculate_outliers(df, column):
    Q1 = df[column].quantile(0.25)  # Primeiro quartil
    Q3 = df[column].quantile(0.75)  # Terceiro quartil
    IQR = Q3 - Q1  # Intervalo interquartil
    lower_bound = Q1 - 1.5 * IQR  # Limite inferior
    upper_bound = Q3 + 1.5 * IQR  # Limite superior
    outliers = df[df[column] > upper_bound]  # Apenas outliers superiores
    if not outliers.empty:
        min_outlier = outliers[column].min()
        print(f"\nMenor valor de outlier em '{column}': {min_outlier}\n")
    else:
        print(f"Não há outliers em '{column}'.")
    return outliers

# Verificar e plotar para 'ExpectedFrequency' e 'ExpectedMonetary'
if 'ExpectedFrequency' in data.columns and 'ExpectedMonetary' in data.columns:
    sns.set(style="whitegrid")

    outliers_expected_frequency = calculate_outliers(data, 'ExpectedFrequency')
    plt.figure(figsize=(10, 5))
    sns.boxplot(x=data['ExpectedFrequency'], color='blue')
    plt.title('Outliers em ExpectedFrequency')
    plt.xlabel('ExpectedFrequency')
    plt.savefig(os.path.join(output_dir, "outliers_expected_frequency.png"))
    plt.show()

    outliers_expected_monetary = calculate_outliers(data, 'ExpectedMonetary')
    plt.figure(figsize=(10, 5))
    sns.boxplot(x=data['ExpectedMonetary'], color='green')
    plt.title('Outliers em ExpectedMonetary')
    plt.xlabel('ExpectedMonetary')
    plt.savefig(os.path.join(output_dir, "outliers_expected_monetary.png"))
    plt.show()

# Verificar e plotar para 'frequency' e 'monetary_value'
if 'frequency' in data.columns and 'monetary_value' in data.columns:
    # Outliers para 'frequency'
    outliers_frequency = calculate_outliers(data, 'frequency')
    plt.figure(figsize=(10, 5))
    sns.boxplot(x=data['frequency'], color='orange')
    plt.title('Outliers em Frequency')
    plt.xlabel('Frequency')
    plt.savefig(os.path.join(output_dir, "outliers_frequency.png"))
    plt.show()

    # Outliers para 'monetary_value'
    outliers_monetary_value = calculate_outliers(data, 'monetary_value')
    plt.figure(figsize=(10, 5))
    sns.boxplot(x=data['monetary_value'], color='purple')
    plt.title('Outliers em Monetary Value')
    plt.xlabel('Monetary Value')
    plt.savefig(os.path.join(output_dir, "outliers_monetary_value.png"))
    plt.show()
else:
    print("As colunas 'frequency' e/ou 'monetary_value' não estão presentes no dataset.")
