import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.workflows.task import Task
from src.DataTransformation.RFM import dictClassificacao
import json


class PlotTask(Task):
    def __init__(self, name: str, plot_all: bool = False, isTraining: bool = False, plot_type: str = None, save_outliers_plots: bool = False) -> None:
        super().__init__(name)
        self.plot_all = plot_all
        self.plot_type = plot_type
        self.save_outliers_plots = save_outliers_plots
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

    def calculate_outliers(self, df, column):
        Q1 = df[column].quantile(0.25)  # Primeiro quartil
        Q3 = df[column].quantile(0.75)  # Terceiro quartil
        IQR = Q3 - Q1  # Intervalo interquartil
        upper_bound = Q3 + 1.5 * IQR  # Limite superior
        outliers = df[df[column] > upper_bound]  # Apenas outliers superiores
        if not outliers.empty:
            min_outlier = outliers[column].min()
            print(f"Menor valor de outlier em '{column}': {min_outlier}")
        else:
            print(f"Não há outliers em '{column}'.")
        return outliers

    def save_outliers_plot(self, df, column, color, output_dir, return_min_outlier=False):
        if return_min_outlier:
            print()
            min_outlier = self.calculate_outliers(df, column)
            print()
            
        plt.figure(figsize=(10, 5))
        sns.boxplot(x=df[column], color=color)
        plt.title(f'Outliers em {column}')
        plt.xlabel(column)
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, f"outliers_{column}.png"))
        plt.close()

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

        if self.save_outliers_plots:
            output_dir = "./plots"
            if 'ExpectedFrequency' in df.columns:
                self.save_outliers_plot(df, 'ExpectedFrequency', 'blue', output_dir)
            if 'ExpectedMonetary' in df.columns:
                self.save_outliers_plot(df, 'ExpectedMonetary', 'green', output_dir)
            if 'frequency' in df.columns:
                self.save_outliers_plot(df, 'frequency', 'orange', output_dir)
            if 'monetary_value' in df.columns:
                self.save_outliers_plot(df, 'monetary_value', 'purple', output_dir)

        # Salvar o resultado como um arquivo JSON
        json_path = "./output/plot_data.json"
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w') as json_file:
            json.dump(result, json_file, indent=4)

        return df