import os
import matplotlib.pyplot as plt
import pandas as pd
from src.workflows.task import Task

dictClassificacao = {
    7: ("Important value customer", "Recently, this customer group has purchased, with high purchase frequency and high consumption, and they are the main consumers.", "Upgrade to the very important person (VIP) customers, provide personalized services, and tilt more resources."),
    3: ("Important development customer", "Recently, this customer group has purchased, with low purchase frequency and high customer unit price. They may be a new wholesaler or enterprise purchaser.", "Provide member points service and provide a certain degree of discount to improve the retention rate of customers."),
    5: ("Important protection customer", "Recently, this customer group has not bought, but the purchase frequency is high and the consumption is high.", "Introduce the latest products/functions/upgraded services through SMS and email to promote customer consumption."),
    1: ("Important retention customer", "Recently, this customer group has not bought, and the purchase frequency is low, but the customer unit price is high.", "Introduce the latest products/functions/upgrade services, promotional discounts, etc., through SMS, email, phone, etc., to avoid the loss of customers."),
    6: ("General value customer", "Recently, this customer group has purchased, with high purchase frequency, but low consumption.", "Introduce the latest products/functions/upgraded services to promote customers’ consumption."),
    4: ("General development customer", "Recently, this customer group has purchased, with low purchase frequency and low consumption. They may be new customers.", "Provide community services, introduce new products/functions, and promote customers’ consumption."),
    2: ("General retention customer", "Recently, this customer group has not bought, with high purchase frequency and low consumption.", "Introduce new products/functions to arouse this part of customers."),
    0: ("Lost customer", "Recently, this customer group has not bought, with low purchase frequency and low consumption, which has been lost.", "This part of customers can be aroused by promotion and discount. When the resource allocation is insufficient, this part of users can be temporarily abandoned.")
}

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

    def plotPieChart(self, data, filename):
        fig, ax = plt.subplots(figsize=(10, 10))
        wedges, texts, autotexts = ax.pie(
            data.values,
            colors=self.colors,
            autopct='%1.1f%%',
            pctdistance=1.1,  # Move a porcentagem para fora
            startangle=90
        )

        for autotext in autotexts:
            autotext.set_fontsize(14)

        plot_path = f"./images/{filename}_chart.svg"
        os.makedirs(os.path.dirname(plot_path), exist_ok=True)
        plt.savefig(plot_path, format="svg", bbox_inches="tight")
        plt.close()

        # Criando legenda separada com menos espaço vertical
        fig_legend, ax_legend = plt.subplots(figsize=(5, 2))  # Reduzindo altura da figura
        legend_labels = [dictClassificacao[i][0] for i in data.index]
        ax_legend.legend(wedges, legend_labels, loc='center', fontsize=12)
        ax_legend.axis('off')
        legend_path = f"./images/{filename}_legend.svg"
        plt.savefig(legend_path, format="svg", bbox_inches="tight")
        plt.close()

    def plotPorcentagemClientes(self, df: pd.DataFrame):
        data = df[self.colRank].value_counts()
        self.plotPieChart(data, "clientsPie")

    def plotMonetaryClientes(self, df: pd.DataFrame):
        data = df.groupby([self.colRank]).sum()[self.colMonetary]
        self.plotPieChart(data, "monetaryPie")

    def plotFrequencyClientes(self, df: pd.DataFrame):
        dfNew = df.copy()
        dfNew['newFreq'] = df[self.colFreq] + 1
        data = dfNew.groupby([self.colRank]).sum()[self.colFreq]
        self.plotPieChart(data, "frequencyPie")

    def on_run(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.plot_all:
            self.plotPorcentagemClientes(df)
            self.plotMonetaryClientes(df)
            self.plotFrequencyClientes(df)
        elif self.plot_type == 'porcentagem':
            self.plotPorcentagemClientes(df)
        elif self.plot_type == 'monetary':
            self.plotMonetaryClientes(df)
        elif self.plot_type == 'frequency':
            self.plotFrequencyClientes(df)
        else:
            raise ValueError(f"Plot type '{self.plot_type}' is not supported.")

        return df
