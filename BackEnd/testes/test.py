import pandas as pd
from lifetimes import GammaGammaFitter
from src.DataBase.CsvRead import CsvReadTask
from src.DataTransformation.RFM import RFMTask
from src.workflows.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error

def test_gamma_gamma_penalizer():
    with Pipeline() as pipeline:
        file_path = "output/data/filtered_transaction.csv"
        columnID = "customer_id"
        columnDate = "date"
        columnMonetary = "amount"

        read_dt = CsvReadTask("read_dt", file_path, columnID, columnDate, columnMonetary)
        rfm_predict = RFMTask("data_predict", isRating=True, predictInterval=1, isTraining=False)

        # Associa as tarefas no pipeline
        read_dt >> rfm_predict

    df = pipeline.run()["data_predict"]

    # Garantir que os dados necessários estão presentes
    if "frequency" not in df.columns or "monetary_value" not in df.columns:
        raise ValueError("O arquivo CSV deve conter as colunas 'frequency' e 'monetary_value'.")

    # Filtrar valores inválidos
    df = df[(df["frequency"] > 0) & (df["monetary_value"] > 0)]

    # Testar diferentes valores de penalizer
    penalizer_values = [0.01, 0.1, 1, 10]
    best_penalizer = None
    best_mae = float("inf")

    print("Testando diferentes valores de penalizer para o modelo Gamma-Gamma...\n")
    for penalizer in penalizer_values:
        model = GammaGammaFitter(penalizer_coef=penalizer)
        model.fit(df["frequency"], df["monetary_value"])
        predictions = model.conditional_expected_average_profit(df["frequency"], df["monetary_value"])
        mae = mean_absolute_error(df["monetary_value"], predictions)

        print(f"Penalizer: {penalizer}, MAE: {mae}")

        # Atualizar o melhor penalizer
        if mae < best_mae:
            best_mae = mae
            best_penalizer = penalizer

    print("\nMelhor Penalizer:")
    print(f"Penalizer: {best_penalizer}, MAE: {best_mae}")

if __name__ == "__main__":
    test_gamma_gamma_penalizer()