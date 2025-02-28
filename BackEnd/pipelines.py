import pandas as pd
from src.workflows.pipeline import Pipeline

from src.DataBase.CsvRead import CsvReadTask
from src.DataTransformation.RFM import RFMTask
from src.LTV.LtvModel import LTVTask

from src.TrasactionModels.TransactionModelRunner import TransactionModelRunner
from src.MonetaryModels.MonetaryModelRunner import MonetaryModelRunner
from src.DataVisualization.Plot import PlotTask

from datetime import datetime

def readCSV(file_path="data/transactions.csv", columnID="customer_id", columnDate="date", columnMonetary="amount"):
    read_dt = CsvReadTask("read_dt", file_path, columnID, columnDate, columnMonetary)
    df = read_dt.run()

    return df

def calculate_LTV_and_Plot(transactionModel, monetaryModel, file_path="data/transactions.csv", columnID="customer_id", columnDate="date", columnMonetary="amount"):
    with Pipeline() as pipeline:
    
    
        read_dt = CsvReadTask(
            "read_dt", file_path, columnID, columnDate, columnMonetary
        )
        rfm_data = RFMTask("split_data", isRating=True)

        transaction_model = transactionModel.run()
        monetary_model = monetaryModel.run()

        ltv = LTVTask("calculo_ltv", columnFrequency="ExpectedFrequency",
                    columnMonetary="ExpectedMonetary")
        
        plot_data = PlotTask("plot", plot_all=True)


        # Lembrando (>> só associa, executa apenas apos rodar pipeline.run())
        read_dt >> rfm_data >> transaction_model >> monetary_model >> ltv >> plot_data
    
    # Retorna um Dicionario com o nome da Task e o DataFrame
    df = pipeline.run()['plot']
    
    return df


    # TODO: Verificar o fluxo do pipeline (era pra dar merge no df ao invés de passar um para o outro)
    # read_dt >> rfm_data
    # rfm_data >> transaction_model
    # rfm_data >> monetary_model
    # # transaction_model >> ltv
    # monetary_model >> ltv


def __use_calculate():
    data = {
        'idColumn': 'customer_id',
        'dateColumn': 'date',
        'amountColumn': 'amount',
        'frequencyModel': 'MachineLearning',
        'monetaryModel': 'GammaGammaModel',
        'weeksAhead': 180
    }
    csv_file_path = "data/transactions.csv"

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

    calculate_LTV_and_Plot(transactionModel, monetaryModel, csv_file_path,
                  data['idColumn'], data['dateColumn'], data['amountColumn'])
    


""" Para adicionar um novo modelo é necessário:
        Criar uma Task para aquele modelo (herdando da Task generica de seu tipo)
        Adicionar os novos atributos necessários para se usar esse modelo no seu respectivo ModelRunner (TransactionModelRunner ou Monetary Model Runner)
        Adicionar um novo if no método run de seu ModelRunner para associar o modelo a sua Task
        Adicionar um novo if no método __use_calculate para associar a chamada do modelo aos seus parâmetros   
"""
def main():
    while True:
        pipelines = {
            "1": __use_calculate,
            "2": readCSV
        }

        print("Escolha um pipeline para executar:")
        for key, value in pipelines.items():
            print(f"{key}: {value.__name__}")

        opcao = input("\nDigite o número do pipeline:")
        print("\nExecutando pipeline...\n")

        if opcao in pipelines:
            pipelines[opcao]()
        else:
            print("\nEscolha inválida.")

        print("\nDeseja executar outro pipeline? (s/n)")
        continuar = input()
        if continuar.lower() != "s":
            break


if __name__ == "__main__":
    main()
