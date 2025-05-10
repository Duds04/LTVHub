import os
import json
import pandas as pd
from src.workflows.pipeline import Pipeline

from src.DataBase.CsvRead import CsvReadTask
from src.DataTransformation.RFM import RFMTask
from src.LTV.LtvModel import LTVTask

from src.DataVisualization.Plot import PlotTask


def readCSV(file_path="output/data/transactions.csv", columnID="customer_id", columnDate="date", columnMonetary="amount"):
    read_dt = CsvReadTask("read_dt", file_path, columnID,
                          columnDate, columnMonetary)
    df = read_dt.run()

    return df


def calculate_LTV_and_Plot(data, file_path="output/data/transactions.csv", columnID="customer_id", columnDate="date", columnMonetary="amount", numPeriods=3):
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
    daysAhead = data["weeksAhead"]
    # Criando modelos dinâmicos e passando numPeriods apenas quando necessário
    transactionModel = load_model(
        "frequencyModels",
        data["frequencyModel"],
        # Se o modelo aceitar essa prop, ela será usada
        {"numPeriods": daysAhead},
    )

    monetaryModel = load_model(
        "monetaryModels",
        data["monetaryModel"],
        # Se o modelo aceitar essa prop, ela será usada
        {"numPeriods": daysAhead},
    )
    
    with Pipeline() as pipeline:
        read_dt = CsvReadTask("read_dt", file_path,
                              columnID, columnDate, columnMonetary)
        rfm_training = RFMTask("data_training", predictInterval=numPeriods, isTraining=True, isRating=False)
        rfm_predict = RFMTask("data_predict", isRating=True, isTraining=False)
        ltv = LTVTask("calculo_ltv", columnFrequency="ExpectedFrequency",
                      columnMonetary="ExpectedMonetary")

        plot_data = PlotTask("plot", plot_all=True, save_outliers_plots=False)

        # Lembrando (>> só associa, executa apenas apos rodar pipeline.run())
        read_dt >> rfm_training
        read_dt >> rfm_predict
        rfm_training >> transactionModel
        rfm_predict >> transactionModel
        rfm_training >> monetaryModel
        rfm_predict >> monetaryModel
        transactionModel >> monetaryModel >> ltv >> plot_data

    # Retorna um Dicionario com o nome da Task e o DataFrame
    df = pipeline.run()['plot']

    return df


def load_model(model_type, model_id, custom_props=None, data_predict=None):
    """Carrega e inicializa um modelo baseado no JSON e adiciona parâmetros personalizados apenas se necessário
        Se o parâmetro adicionado não for definido no modelo, ele será ignorado. """

    json_path = os.path.join(os.path.dirname(__file__), "jsons", "Models.json")

    with open(json_path, "r") as file:
        models_data = json.load(file)

    # Encontrar a lista correta (frequencyModels ou monetaryModels)
    model_list = models_data.get(model_type, [])

    # Buscar o modelo específico pelo ID
    model_config = next((m for m in model_list if m["id"] == model_id), None)

    if not model_config:
        raise ValueError(f"Modelo '{model_id}' não encontrado no JSON!")

    # Executa o import dinâmico do chamador
    exec(model_config["importer"], globals())

    # Atualiza os props com valores customizados, se existirem
    model_props = model_config["props"]

    # Pega os custom_props e adiciona apenas os que são usados no modelo
    if custom_props:
        for key, value in custom_props.items():
            # Adiciona o parâmetro somente se a chave existir nos props do modelo
            if key in model_props:
                model_props[key] = value

    # Inicializa o modelo dinamicamente
    model_class = globals()[model_config["model_task_name"]]
    
    model_instance = model_class(**model_props)

    return model_instance

def __use_calculate():
    data = {
        'idColumn': 'customer_id',
        'dateColumn': 'date',
        'amountColumn': 'amount',
        'frequencyModel': 'ParetoModel',
        'monetaryModel': 'MachineLearningModel',
        'weeksAhead': 1,
    }

    csv_file_path = "output/data/transactions.csv"
    

    df = calculate_LTV_and_Plot(data, csv_file_path,
                                data['idColumn'], data['dateColumn'], data['amountColumn'], data['weeksAhead'])

    # Salvar esse df em um arquivo 
    output_file_path = "output/ltv_results.csv"
    df.to_csv(output_file_path, index=True)
    print(f"Resultados salvos em: {output_file_path}")
    return df


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
    # main()
    __use_calculate()
