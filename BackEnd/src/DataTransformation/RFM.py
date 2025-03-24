from src.workflows.task import Task
import pandas as pd
from lifetimes.utils import (  # noqa: E402
    calibration_and_holdout_data,
    summary_data_from_transaction_data,
)
import numpy as np


""" Dicionario antes da tradução

dictClassificacao = {
    7: ("Important value customer", "Recently, this customer group has purchased, with high purchase frequency and high consumption, and they are the main consumers.", "Upgrade to the very important person (VIP) customers, provide personalized services, and tilt more resources."),
    3: ("Important development customer", "Recently, this customer group has purchased, with low purchase frequency and high customer unit price. They may be a new wholesaler or enterprise purchaser.", "Provide member points service and provide a certain degree of discount to improve the retention rate of customers."),
    5: ("Important protection customer", "Recently, this customer group has not bought, but the purchase frequency is high and the consumption is high.", "Introduce the latest products/functions/upgraded services through SMS and email to promote customer consumption."),
    1: ("Important retention customer", "Recently, this customer group has not bought, and the purchase frequency is low, but the customer unit price is high.", "Introduce the latest products/functions/upgrade services, promotional discounts, etc., through SMS, email, phone, etc., to avoid the loss of customers."),
    6: ("General value customer", "Recently, this customer group has purchased, with high purchase frequency, but low consumption.", "Introduce the latest products/functions/upgraded services to promote customers’ consumption."),
    4: ("General development customer", "Recently, this customer group has purchased, with low purchase frequency and low consumption. They may be new customers.", "Provide community services, introduce new products/functions, and promote customers’ consumption."),
    2: ("General retention customer", "Recently, this customer group has not bought, with high purchase frequency and low consumption.", "Introduce new products/functions to arouse this part of customers."),
    0: ("Lost customer", "Recently, this customer group has not bought, with low purchase frequency and low consumption, which has been lost.", "This part of customers can be aroused by promotion and discount. When the resource allocation is insufficient, this part of users can be temporarily abandoned.")
}"""

dictClassificacao = {
    7: ("Cliente de alto valor", 
    "Este grupo de clientes tem comprado recentemente com alta frequência e alto volume de consumo, sendo os principais consumidores.", 
    "Eleve esses clientes ao status de VIP, oferecendo serviços personalizados e alocando mais recursos para atendê-los."),
    3: ("Cliente de desenvolvimento estratégico", 
    "Este grupo de clientes tem feito compras com baixa frequência, mas com alto valor unitário por compra. Podem ser novos atacadistas ou compradores corporativos.", 
    "Ofereça serviços de pontos para membros e ofereça descontos para aumentar a fidelização e retenção desses clientes."),
    5: ("Cliente em fase de proteção", 
    "Este grupo de clientes não tem feito compras recentemente, mas apresenta alta frequência de compras passadas e elevado volume de consumo.", 
    "Envie atualizações sobre novos produtos, serviços e funcionalidades por meio de SMS e e-mails para incentivar o retorno e aumentar o consumo."),
    1: ("Cliente de retenção crítica", 
    "Este grupo de clientes não tem comprado recentemente, apresenta baixa frequência de compras, mas tem um alto valor médio por compra.", 
    "Envie ofertas personalizadas, atualizações de produtos ou serviços, e promoções via SMS, e-mail ou telefone para evitar a perda desses clientes valiosos."),
    6: ("Cliente de valor geral", 
    "Este grupo de clientes tem comprado com alta frequência, mas seu consumo tem sido baixo.", 
    "Introduza novos produtos, serviços e funcionalidades para incentivar um aumento no volume de compras e engajamento desses clientes."),
    4: ("Cliente em desenvolvimento", 
    "Este grupo de clientes tem comprado com baixa frequência e baixo volume de consumo. Podem ser clientes novos ou pouco engajados.", 
    "Ofereça serviços adicionais, apresente novos produtos ou funcionalidades e incentive o aumento no consumo para estreitar o relacionamento com esses clientes."),
    2: ("Cliente de retenção geral", 
    "Este grupo de clientes não tem feito compras recentemente, mas apresenta alta frequência de compras passadas com baixo volume de consumo.", 
    "Apresente novos produtos ou funcionalidades para despertar o interesse e estimular o consumo desses clientes."),
    0: ("Cliente perdido", 
    "Este grupo de clientes não tem feito compras, apresenta baixa frequência de compras e baixo volume de consumo, sendo considerado perdido.", 
    "Utilize promoções e descontos para tentar reconquistar esses clientes. Quando os recursos são limitados, pode ser necessário priorizar outros segmentos e deixar esses clientes de lado por enquanto.")
}


class RFMTask(Task):
    def __init__(
        self,
        name: str,
        minTrainin: int = -1,
        maxTraining: int = -1,
        predictInterval: int = -1,
        columnID: str = "id",
        columnDate: str = "date",
        columnMonetary: str = "monetary",
        frequency: str = "W",
        calibrationEnd=None,
        observationEnd=None,
        split: float = 0.8,
        isTraining: bool = False,
        isRating: bool = False,
    ) -> None:
        """
        Args:
                columnID #Nome da coluna onde encontra-se os identificadores
                columnDate  #Nome da coluna onde encontra-se as datas
                columnMonetary  #Nome da coluna onde encontra-se os valores monetários
                frequency = 'W' #Frequência em que será observado, Ex: "W" - Weeks
                calibrationEnd = None #Caso queira passar a data do fim do período de calibração
                observationEnd = None #Caso queira passar a data do fim do período de Obsersvação
                split = 0.8 # Porcentagem da divisão dos dados para separar em Obsersvação e calibração
                minTrainin: int, # Qual é o periodo mínimo que será usado para treino
                maxTraining: int, # Qual será o último período que será usado para o treino
                predictInterval: int = 4, # Define quantos períodos serão os intervalos de predição (Quantos periodos queremos prever)
                apply_calibration_split # Fazer a divisão do dataFrame em calibration e holdout (se for Test isso ficara como true)
        """
        super().__init__(name)
        self.columnID = columnID
        self.columnDate = columnDate
        self.columnMonetary = columnMonetary
        self.frequency = frequency
        self.calibrationEnd = calibrationEnd
        self.observationEnd = observationEnd
        self.split = split
        self.isTraining = isTraining
        if(isTraining): self.apply_calibration_split = True
        else: self.apply_calibration_split = False
        self.minTrainin = minTrainin
        self.maxTraining = maxTraining
        self.predictInterval = predictInterval
        self.isRating = isRating
        
        

    def __getPeriodosList(self, df: pd.DataFrame):
        def __to_period(df: pd.DataFrame):
            return df.to_period(self.frequency)

        df["period"] = df[self.columnDate].map(__to_period)
        df = df.sort_values(by='period')
        return df.period.unique()

    def __getPeriodos(
        self, df: pd.DataFrame
    ):
        """
        Args:
            df, #Dataframe do Pandas
        """
        assert self.columnDate in df.columns

        firstData = df[self.columnDate].sort_values().values[0]
        lastData = df[self.columnDate].sort_values().values[-1]
        rangeDatas = pd.date_range(
            start=firstData, end=lastData, freq=self.frequency)
        indexCut = round(len(rangeDatas) * self.split)
        return rangeDatas[indexCut], lastData

    def __rfm_data_filler(self, df: pd.DataFrame) -> pd.DataFrame:
            """
            Args:
                df, #Dataframe do Pandas
            """
            if self.calibrationEnd is None:
                self.calibrationEnd, self.observationEnd = self.__getPeriodos(
                    df
                )
            
            if self.apply_calibration_split is False:
                return summary_data_from_transaction_data(
                    transactions=df,
                    customer_id_col=self.columnID,
                    datetime_col=self.columnDate,
                    monetary_value_col=self.columnMonetary,
                    freq=self.frequency,
                )
            else:
                rfm_cal_holdout = calibration_and_holdout_data(
                    transactions=df,
                    customer_id_col=self.columnID,
                    datetime_col=self.columnDate,
                    monetary_value_col=self.columnMonetary,
                    freq=self.frequency,
                    calibration_period_end=self.calibrationEnd,
                    observation_period_end=self.observationEnd,
                )
            return rfm_cal_holdout
        
    def __split_by_percentage(self, df: pd.DataFrame, column: str, percent=0.75):
        limiar = df[column].sort_values().iloc[int(df.shape[0] * percent)]
        return np.where(df[column] > limiar, 1, 0)
    
    def rating(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.isTraining:
            df['groupFrequency'] = self.__split_by_percentage(df, 'frequency_cal')
            df['groupRecency'] = self.__split_by_percentage(df, 'recency_cal')
            df['groupMonetary'] = self.__split_by_percentage(df, 'monetary_value_cal')
        else:
            df['groupFrequency'] = self.__split_by_percentage(df, 'frequency')
            df['groupRecency'] = self.__split_by_percentage(df, 'recency')
            df['groupMonetary'] = self.__split_by_percentage(df, 'monetary_value')

        cols = ['groupFrequency', 'groupRecency', 'groupMonetary']
        df['rankingClients'] = df[cols].apply(lambda row: int(''.join(row.values.astype(str)), 2), axis=1)
        
        df['type'] = df['rankingClients'].map(lambda x: dictClassificacao.get(x, ("Unknown", "", ""))[0])
        df['description'] = df['rankingClients'].map(lambda x: dictClassificacao.get(x, ("Unknown", "", ""))[1])
        df['howToManage'] = df['rankingClients'].map(lambda x: dictClassificacao.get(x, ("Unknown", "", ""))[2])
        
        return df


    def on_run(self, df: pd.DataFrame) -> pd.DataFrame:
        assert self.columnID in df.columns, f"ID column '{self.columnID}' not found in DataFrame columns: {df.columns}"
        assert self.columnMonetary in df.columns, f"Monetary column '{self.columnMonetary}' not found in DataFrame columns: {df.columns}"
        assert self.columnDate in df.columns, f"Date column '{self.columnDate}' not found in DataFrame columns: {df.columns}"
        
        dfReturn = pd.DataFrame()
        if self.apply_calibration_split:
            dfReturn = self.__rfm_data_filler(df)
        else:
            periods = self.__getPeriodosList(df)
            
            if self.maxTraining == -1:
                self.maxTraining = len(periods) - (self.predictInterval + 1)
            if self.minTrainin == -1:
                self.minTrainin = self.predictInterval * 2
            
            for period in range(self.minTrainin, self.maxTraining, self.predictInterval):
                self.calibrationEnd = periods[period].to_timestamp()
                self.observationEnd = periods[period + self.predictInterval].to_timestamp()
                dfReturn = pd.concat([dfReturn, self.__rfm_data_filler(df)])
                
        if self.isRating:
            dfReturn = self.rating(dfReturn)
                
        return dfReturn