import pandas as pd
from src.workflows.pipeline import Pipeline

from src.DataBase.CsvRead import CsvReadTask
from src.DataTransformation.RFM import RFMTask
from src.TrasactionModels.ParetoModel import ParetoModelTask
from src.TrasactionModels.BGFModel import BGFModelTask
from src.MonetaryModels.GammaGammaModel import GammaGammaModelTask
from src.GenericModels.MachineLearning import MachineLearningModel
from src.LTV.LtvModel import LTVTask

from src.TrasactionModels.TransactionModelRunner import TransactionModelRunner
from src.MonetaryModels.MonetaryModelRunner import MonetaryModelRunner

#  @classmethod --> não precisa passar a instancia não usa o self


def __pipeline_readCSV():
    read_dt = CsvReadTask("read_dt", "data/transactions.csv",
                          "customer_id", "date", "amount")
    df = read_dt.run()
    return df


def __pipeline_RFM():
    read_dt = CsvReadTask(
        "read_dt", "data/transactions.csv", "customer_id", "date", "amount"
    )
    rfm_data = RFMTask("split_data", isTraining=True)
    read_dt >> rfm_data


def __pipeline_RFM_Enriquecido():
    read_dt = CsvReadTask(
        "read_dt", "data/transactions.csv", "customer_id", "date", "amount"
    )
    rfm_data_enriquecido = RFMTask(
        "split_data_enriquecido", predictInterval=4,  isTraining=True)
    read_dt >> rfm_data_enriquecido


def __pipeline_pareto():
    read_dt = CsvReadTask(
        "read_dt", "data/transactions.csv", "customer_id", "date", "amount"
    )
    rfm_data = RFMTask("split_data", isTraining=True)
    pareto_model = ParetoModelTask(
        "pareto_model", isRating=True, isTraining=True)

    read_dt >> rfm_data >> pareto_model


def __pipeline_bgf():
    read_dt = CsvReadTask(
        "read_dt", "data/transactions.csv", "customer_id", "date", "amount"
    )
    rfm_data = RFMTask("split_data")
    bgf_model = BGFModelTask("bgf_model", isRating=True)

    read_dt >> rfm_data >> bgf_model


def __pipeline_gammmaGamma():
    read_dt = CsvReadTask(
        "read_dt", "data/transactions.csv", "customer_id", "date", "amount"
    )
    rfm_data = RFMTask("split_data", isTraining=True)
    gammaGamma_model = GammaGammaModelTask(
        "gammaGamma_model", isRating=True, isTraining=True)

    read_dt >> rfm_data >> gammaGamma_model


def __pipeline_MLTrasaction():
    read_dt = CsvReadTask(
        "read_dt", "data/transactions.csv", "customer_id", "date", "amount"
    )
    rfm_data = RFMTask("split_data", isTraining=True)
    ml_model_transaction = MachineLearningModel("machine_learning_model_transaction", "frequency_holdout", isMonetary=False, X_Columns=[
        'frequency_cal', 'recency_cal', 'T_cal', 'monetary_value_cal', 'duration_holdout'], isTraining=True)

    read_dt >> rfm_data >> ml_model_transaction


def __pipeline_MLMonetary():
    read_dt = CsvReadTask(
        "read_dt", "data/transactions.csv", "customer_id", "date", "amount"
    )
    rfm_data = RFMTask("split_data", isTraining=True)
    ml_model_monetary = MachineLearningModel("machine_learning_monetary", "monetary_value_holdout", X_Columns=[
                                             'frequency_cal', 'recency_cal', 'T_cal', 'monetary_value_cal', 'duration_holdout'], isTraining=True, isMonetary=True)

    read_dt >> rfm_data >> ml_model_monetary


def __pipeline_MLMonetary_Enriquecido():
    read_dt = CsvReadTask(
        "read_dt", "data/transactions.csv", "customer_id", "date", "amount"
    )
    rfm_data_enriquecido = RFMTask(
        "split_data_enriquecido", predictInterval=4, isTraining=True)
    ml_model_monetary = MachineLearningModel("machine_learning_monetary", "monetary_value_holdout", X_Columns=[
                                             'frequency_cal', 'recency_cal', 'T_cal', 'monetary_value_cal', 'duration_holdout'], isTraining=True, isMonetary=True)
    read_dt >> rfm_data_enriquecido >> ml_model_monetary


def __pipeline_MLMonetary_NOT_Training():
    read_dt = CsvReadTask(
        "read_dt", "data/transactions.csv", "customer_id", "date", "amount"
    )
    rfm_data = RFMTask("split_data")
    ml_model_monetary = MachineLearningModel("machine_learning_monetary", "monetary_value", X_Columns=[
                                             'frequency', 'recency', 'T', 'monetary_value'], isMonetary=True)

    read_dt >> rfm_data >> ml_model_monetary


def __pipeline_MLTrasaction_NOT_Training():
    read_dt = CsvReadTask(
        "read_dt", "data/transactions.csv", "customer_id", "date", "amount"
    )
    rfm_data = RFMTask("split_data")
    ml_model_transaction = MachineLearningModel("machine_learning_model_transaction", "frequency", X_Columns=[
                                                'frequency', 'recency', 'T', 'monetary_value'], isMonetary=False)

    read_dt >> rfm_data >> ml_model_transaction


def __pipeline_pareto_CLV():
    read_dt = CsvReadTask(
        "read_dt", "data/transactions.csv", "customer_id", "date", "amount"
    )
    rfm_data = RFMTask("split_data")

    pareto_model = ParetoModelTask("pareto_model", isRating=True)
    ltv = LTVTask("calculo_ltv", columnFrequency="ExpectedFrequency")

    read_dt >> rfm_data >> pareto_model >> ltv


def __pipeline_gammaGamma_TEST_CLV():
    read_dt = CsvReadTask(
        "read_dt", "data/transactions.csv", "customer_id", "date", "amount"
    )
    rfm_data = RFMTask("split_data", isTraining=True)

    gammaGamma_model = GammaGammaModelTask(
        "gammaGamma_model", isRating=True, isTraining=True)
    ltv = LTVTask(
        "calculo_ltv", columnFrequency="ExpectedFrequency", isTraining=True)

    read_dt >> rfm_data >> gammaGamma_model >> ltv


def __pipeline_transaction():
    typeModels = {
        "1": "ParetoModel",
        "2": "MachineLearning",
        "3": "BGFModel",
    }

    print("Escolha o modelo para executar:")
    for key, value in typeModels.items():
        print(f"{key}: {value.value}")

    typeModel = input("\nDigite o número do modelo:")

    if typeModel in typeModels:
        typeModel = typeModels[typeModel]
    else:
        print("\nEscolha inválida.")
        return

    read_dt = CsvReadTask(
        "read_dt", "data/transactions.csv", "customer_id", "date", "amount"
    )
    rfm_data = RFMTask("split_data", isTraining=True)
    if (typeModel == "MachineLearning"):
        transaction_use = TransactionModelRunner("model", typeModel, isTraining=True, isRating=True, target="frequency_holdout", X_Columns=[
            'frequency_cal', 'recency_cal', 'T_cal', 'monetary_value_cal', 'duration_holdout'])
    else:
        transaction_use = TransactionModelRunner(
            "model", typeModel, isTraining=True, isRating=True)
    model = transaction_use.run()

    read_dt >> rfm_data >> model


def __pipeline_monetary():
    typeModels = {
        "1": "GammaGammaModel",
        "2": "MachineLearning",
    }

    print("Escolha o modelo para executar:")
    for key, value in typeModels.items():
        print(f"{key}: {value.value}")

    typeModel = input("\nDigite o número do modelo:")

    if typeModel in typeModels:
        typeModel = typeModels[typeModel]
    else:
        print("\nEscolha inválida.")
        return

    read_dt = CsvReadTask(
        "read_dt", "data/transactions.csv", "customer_id", "date", "amount"
    )
    rfm_data = RFMTask("split_data", isTraining=True)
    if (typeModel == "MachineLearning"):
        monetary_use = MonetaryModelRunner("model", typeModel, isTraining=True, isRating=True, target="frequency_holdout", X_Columns=[
                                           'frequency_cal', 'recency_cal', 'T_cal', 'monetary_value_cal', 'duration_holdout'])
    else:
        monetary_use = MonetaryModelRunner(
            "model", typeModel, isTraining=True, isRating=True)

    model = monetary_use.run()

    read_dt >> rfm_data >> model


def calculate_LTV(transactionModel, monetaryModel, file_path="data/transactions.csv", columnID="customer_id", columnDate="date", columnMonetary="amount"):
    with Pipeline() as pipeline:

        read_dt = CsvReadTask(
            "read_dt", file_path, columnID, columnDate, columnMonetary
        )
        rfm_data = RFMTask("split_data")

        transaction_model = transactionModel.run()
        monetary_model = monetaryModel.run()

        ltv = LTVTask("calculo_ltv", columnFrequency="ExpectedFrequency",
                      columnMonetary="ExpectedMonetary")

        # Lembrando (>> só associa, executa apenas apos rodar pipeline.run())
        read_dt >> rfm_data >> transaction_model >> monetary_model >> ltv

    df = pipeline.run()
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
    print(csv_file_path, data['idColumn'], data['dateColumn'], data['amountColumn'],
          data['weeksAhead'], data['frequencyModel'], data['monetaryModel'])

    if data['frequencyModel'] == "MachineLearning":
        transactionModel = TransactionModelRunner("transaction_model", model=data['frequencyModel'], target="frequency", X_Columns=[
                                                  'frequency', 'recency', 'T', 'monetary_value'])
    else:
        transactionModel = TransactionModelRunner(
            "transaction_model", data['frequencyModel'], isRating=True, numPeriods=data['weeksAhead'])

    if data['monetaryModel'] == "MachineLearning":
        monetaryModel = MonetaryModelRunner(name="monetary_model", model=data['monetaryModel'], target="monetary_value", X_Columns=[
                                            'frequency', 'recency', 'T', 'monetary_value'])
    else:
        monetaryModel = MonetaryModelRunner(
            name="monetary_model", model=data['monetaryModel'], isRating=True)

    print(transactionModel, monetaryModel)
    calculate_LTV(transactionModel, monetaryModel, csv_file_path,
                  data['idColumn'], data['dateColumn'], data['amountColumn'])


def calculate_Rating(file_path="data/transactions.csv", columnID="customer_id", columnDate="date", columnMonetary="amount"):
    with Pipeline() as pipeline:

        read_dt = CsvReadTask(
            "read_dt", file_path, columnID, columnDate, columnMonetary
        )
        rfm_data = RFMTask("split_data", isRating=True)

        # Lembrando (>> só associa, executa apenas apos rodar pipeline.run())
        read_dt >> rfm_data

    rfm = pipeline.run()['split_data']
    
    return rfm


def __test_rating():
    data = {
        'idColumn': 'customer_id',
        'dateColumn': 'date',
        'amountColumn': 'amount',
        'frequencyModel': 'MachineLearning',
        'monetaryModel': 'GammaGammaModel',
        'weeksAhead': 180
    }
    csv_file_path = "data/transactions.csv"
    print(csv_file_path, data['idColumn'], data['dateColumn'], data['amountColumn'],
          data['weeksAhead'], data['frequencyModel'], data['monetaryModel'])

    df = calculate_Rating(
        csv_file_path, data['idColumn'], data['dateColumn'], data['amountColumn'])

    return df
    
""" Para adicionar um novo modelo é necessário:
        Criar uma Task para aquele modelo (herdando da Task generica de seu tipo)
        Adicionar os novos atributos necessários para se usar esse modelo no seu respectivo ModelRunner (TransactionModelRunner ou Monetary Model Runner)
        Adicionar um novo if no método run de seu ModelRunner para associar o modelo a sua Task
        Adicionar um novo if no método __use_calculate para associar a chamada do modelo aos seus parâmetros   
"""


def menu():
    while True:
        pipelines = {
            "1": __use_calculate,
            "2": __pipeline_RFM,
            "3": __pipeline_RFM_Enriquecido,
            "4": __pipeline_pareto,
            "5": __pipeline_bgf,
            "6": __pipeline_gammmaGamma,
            "7": __pipeline_MLTrasaction,
            "8": __pipeline_MLMonetary,
            "9": __pipeline_MLMonetary_Enriquecido,
            "10": __pipeline_pareto_CLV,
            "11": __pipeline_transaction,
            "12": __pipeline_monetary,
            "13": __pipeline_gammaGamma_TEST_CLV,
            "14": __pipeline_MLMonetary_NOT_Training,
            "15": __pipeline_MLTrasaction_NOT_Training,
            "16": __pipeline_readCSV
        }

        print("Escolha um pipeline para executar:")
        for key, value in pipelines.items():
            print(f"{key}: {value.__name__}")

        opcao = input("\nDigite o número do pipeline:")
        print("\nExecutando pipeline...\n")

        if (opcao == "1") or (opcao == "16"):
            pipelines[opcao]()
        elif opcao in pipelines:
            with Pipeline() as pipeline:
                pipelines[opcao]()
            print("\n", pipeline.run())
        else:
            print("\nEscolha inválida.")

        print("\nDeseja executar outro pipeline? (s/n)")
        continuar = input()
        if continuar.lower() != "s":
            break


dictClassificacao = {
    # Tipo, Descrição, Como lidar

    7: ("Important value customer",
        "Recently, this customer group has purchased, with high purchase frequency and high consumption, and they are the main consumers.",
        "Upgrade to the very important person (VIP) customers, provide personalized services, and tilt more resources."),
    3: ("Important development customer",
        "Recently, this customer group has purchased, with low purchase frequency and high customer unit price. They may be a new wholesaler or enterprise purchaser.", "Provide member points service and provide a certain degree of discount to improve the retention rate of customers.",),
    5: ("Important protection customer",
        "Recently, this customer group has not bought, but the purchase frequency is high and the consumption is high.",
        "Introduce the latest products/functions/upgraded services through SMS and email to promote customer consumption."),
    1: ("Important retention customer",
        "Recently, this customer group has not bought, and the purchase frequency is low, but the customer unit price is high.",
        "Introduce the latest products/functions/upgrade services, promotional discounts, etc., through SMS, email, phone, etc., to avoid the loss of customers."
        ),
    6: ("General value customer",
        "Recently, this customer group has purchased, with high purchase frequency, but low consumption.",
        "Introduce the latest products/functions/upgraded services to promote customers’ consumption."
        ),
    4: ("General development customer ",
        "Recently, this customer group has purchased, with low purchase frequency and low consumption. They may be new customers.",
        "Provide community services, introduce new products/functions, and promote customers’ consumption."),
    2: ("General retention customer",
        "Recently, this customer group has not bought, with high purchase frequency and low consumption.",
        "Introduce new products/functions to arouse this part of customers."),
    0: ("Lost customer",
        " Recently, this customer group has not bought, with low purchase frequency and low consumption, which has been lost.",
        "This part of customers can be aroused by promotion and discount. When the resource allocation is insufficient, this part of users can be temporarily abandoned."
        )
}

import seaborn as sns
import matplotlib.pyplot as plt
import os

def plotPorcentagemClientes(df, col='rankingClients'):
    plt.subplots(figsize=(15, 15))
    colors = sns.color_palette('pastel')
    data = df[col].value_counts()
    legenda = [dictClassificacao[i][0] for i in data.index]

    # create pie chart
    patches, texts, junk = plt.pie(
        data.values, colors=colors, autopct='%.0f%%')
    plt.legend(patches, legenda, loc='best')
    plt.title("Porcentagem das classificações de clientes")
    plot_path = "./static/assets/plots/clientsPie.png"
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path, bbox_inches="tight")
    plt.close()

def plotMonetaryClientes(df, colRank='rankingClients', colMonetary='monetary_value'):
    plt.subplots(figsize=(15, 15))
    colors = sns.color_palette('pastel')
    data = df.groupby([colRank]).sum()[colMonetary]
    legenda = [dictClassificacao[i][0] for i in data.index]

    # create pie chart
    patches, texts, junk = plt.pie(
        data.values, colors=colors, autopct='%.0f%%')
    plt.legend(patches, legenda, loc='best')
    plt.title("Porcentagem do valor monetário das classificações de clientes")
    plot_path = "./static/assets/plots/monetaryPie.png"
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path, bbox_inches="tight")
    plt.close()

def plotFrequencyClientes(df, colRank='rankingClients', colFreq='frequency'):
    df['newFreq'] = df[colFreq] + 1
    plt.subplots(figsize=(15, 15))
    colors = sns.color_palette('pastel')
    data = df.groupby([colRank]).sum()[colFreq]
    legenda = [dictClassificacao[i][0] for i in data.index]

    # create pie chart
    patches, texts, junk = plt.pie(
        data.values, colors=colors, autopct='%.0f%%')
    plt.legend(patches, legenda, loc='best')
    plt.title("Porcentagem das compras das classificações de clientes")
    plot_path = "./static/assets/plots/frequencyPie.png"
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path, bbox_inches="tight")
    plt.close()


def main():
    # menu()
    rfm = __test_rating()
    
    print(rfm)
    
    # plotPorcentagemClientes(rfm)
    # plotMonetaryClientes(rfm)
    # plotFrequencyClientes(rfm)


if __name__ == "__main__":
    main()
