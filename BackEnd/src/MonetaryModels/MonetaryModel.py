from src.workflows.task import Task
import pandas as pd
from abc import abstractmethod
from sklearn.metrics import mean_squared_error

class MonetaryModelTask(Task):
    def __init__(
        self,
        name: str,
        isTunning: bool = False,
    ) -> None:
        """
        Args:
        """
        super().__init__(name)
        self.model = None
        self.isTunning = isTunning

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
    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """
            Dado um período, retorna o número de transações esperadas até ele
        """
        pass

    @abstractmethod
    def fit(self, df: pd.DataFrame) -> pd.DataFrame:
        """
            Treina o modelo com os dados passados
        """
        pass

