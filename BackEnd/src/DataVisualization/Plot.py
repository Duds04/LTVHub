import os
import pandas as pd
from src.workflows.task import Task
from src.DataTransformation.RFM import dictClassificacao
import json


class PlotTask(Task):
    def __init__(self, name: str, plot_all: bool = False, isTraining: bool = False, plot_type: str = None) -> None:
        super().__init__(name)
        self.plot_all = plot_all
        self.plot_type = plot_type
        self.colRank = 'rankingClients'

        if isTraining:
            self.colMonetary = 'monetary_value_cal'
            self.colFreq = 'frequency_cal'
        else:
            self.colMonetary = 'monetary_value'
            self.colFreq = 'frequency'

        self.colors = ['#003436', '#005843', '#007252', '#008D60', '#00A86B', '#66BFA1', '#99D1BA', '#B2D1BD']
        self.color_map = {key: self.colors[i % len(self.colors)] for i, key in enumerate(dictClassificacao.keys())}

    def generatePieData(self, data):
        pie_data = {}
        total_value = data.sum()

        for rank, value in data.items():
            pie_data[rank] = {
                "Tipo": dictClassificacao.get(rank, ["Unknown"])[0],  # Get the type of the rank
                "Porcentagem": (value / total_value) * 100,
                "ValorAbsoluto": value
            }

        return pie_data

    def plotPorcentagemClientes(self, df: pd.DataFrame):
        data = df[self.colRank].value_counts()
        return self.generatePieData(data)

    def plotMonetaryClientes(self, df: pd.DataFrame):
        data = df.groupby([self.colRank]).sum()[self.colMonetary]
        return self.generatePieData(data)

    def plotFrequencyClientes(self, df: pd.DataFrame):
        dfNew = df.copy()
        dfNew['newFreq'] = df[self.colFreq] + 1
        data = dfNew.groupby([self.colRank]).sum()[self.colFreq]
        return self.generatePieData(data)

    def on_run(self, df: pd.DataFrame) -> pd.DataFrame:
        result = {}

        if self.plot_all:
            result["clients"] = self.plotPorcentagemClientes(df)
            result["monetary"] = self.plotMonetaryClientes(df)
            result["frequency"] = self.plotFrequencyClientes(df)
        elif self.plot_type == 'porcentagem':
            result["clients"] = self.plotPorcentagemClientes(df)
        elif self.plot_type == 'monetary':
            result["monetary"] = self.plotMonetaryClientes(df)
        elif self.plot_type == 'frequency':
            result["frequency"] = self.plotFrequencyClientes(df)
        else:
            raise ValueError(f"Plot type '{self.plot_type}' is not supported.")

        # Save the result as a JSON file for future use (to create a graph via frontend)
        json_path = "./output/plot_data.json"
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w') as json_file:
            json.dump(result, json_file, indent=4)

        return df
