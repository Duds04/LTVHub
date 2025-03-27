from src.workflows.task import Task
import pandas as pd
from abc import abstractmethod
from sklearn.metrics import mean_squared_error


class TransactionModelTask(Task):
    def __init__(
        self,
        name: str,
        isTraining: bool = False,
        penalizer: float = 0.1,
        numPeriods: int = 1,
    ) -> None:
        """
        Args:
            model #Modelo BG/NBD ou de Pareto esperado para realizar a predição
            rfm #Dataset já processado pelo RFM
            isTraining = True #Caso seja para efetuar a predição em um dataset com ou sem o período de observação
        """
        super().__init__(name)
        self.model = None
        self.isTraining = isTraining
        self.penalizer = penalizer
        self.numPeriods = numPeriods

    @abstractmethod
    def on_run(self, dfRFM: pd.DataFrame) -> pd.DataFrame:
        """
            Dado um dataset com os valores de RFM, retorna a predição do número de transações esperadas
        """
        self.data_predict = self.task_in["data_predict"].output.copy()
        self.data_training = self.task_in["data_training"].output.copy()

    @abstractmethod
    def createModel(self, df: pd.DataFrame):
        pass

    @abstractmethod
    def predict(self, df: pd.DataFrame, isTraining: bool = False) -> pd.DataFrame:
        """
            Dado um período, retorna o número de transações esperadas até ele
        """
        if isTraining:
            # No período de Treino e no periodo de Validação
            return self.model.conditional_expected_number_of_purchases_up_to_time(
                self.numPeriods,
                df["frequency_cal"].values,
                df["recency_cal"].values,
                df["T_cal"].values,
            )
        # Prever dados futuros, com todo o dataset
        return self.model.conditional_expected_number_of_purchases_up_to_time(
            self.numPeriods,
            df["frequency"].values,
            df["recency"].values,
            df["T"].values
        )

    @abstractmethod
    def fit(self, df: pd.DataFrame) -> pd.DataFrame:
        """
            Treina o modelo com os dados passados
        """
        pass

   