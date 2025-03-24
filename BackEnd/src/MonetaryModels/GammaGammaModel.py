from src.workflows.task import Task
import pandas as pd
from lifetimes import GammaGammaFitter
from src.MonetaryModels.MonetaryModel import MonetaryModelTask

class GammaGammaModelTask(MonetaryModelTask):
    def __init__(
        self,
        name: str,
        isTunning: bool = False,
        penalizer: float = 0.1,
    ) -> None:
        """
        Args:
            isTraining = True #Caso seja para efetuar a predição em um dataset com ou sem o período de observação
            isTunning = None # Fazer o Tunning de hyperparâmetros se for True
            penalizer = 0.1 # Coeficiente de penalização usado pelo modelo
        """
        super().__init__(name, isTunning)
        self.penalizer = penalizer
        self.model = self.createModel()

    def on_run(self, dfRFM: pd.DataFrame) -> pd.DataFrame:
        super().on_run(dfRFM)
        monetary = "monetary_value"
        frequency = "frequency"

        self.data_predict = self.data_predict[self.data_predict[monetary] > 0]

        self.fit(self.data_predict, monetary, frequency)

        self.data_predict['ExpectedMonetary'] = self.predict(self.data_predict, monetary, frequency)

        return self.data_predict

    def createModel(self) -> pd.DataFrame:
        gamma = GammaGammaFitter(penalizer_coef=self.penalizer)
        return gamma

    def fit(self, df: pd.DataFrame, monetary: str, frequency: str) -> pd.DataFrame:
        """
            Treina o modelo com os dados passados
        """
        self.model.fit(df[frequency], df[monetary])
        return self.model

    def predict(self, df: pd.DataFrame, monetary: str, frequency: str) -> pd.DataFrame:
        """
            Dado um período, retorna o número de transações esperadas até ele
        """
        return self.model.conditional_expected_average_profit(df[frequency], df[monetary])
