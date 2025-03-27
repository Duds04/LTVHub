from src.workflows.task import Task
import pandas as pd
from abc import abstractmethod

# usados pelo Machine Learning (tem o Y independente)
class GenericModelTask(Task):
    def __init__(
        self,
        name: str,
        target: str,
        isMonetary: bool,
        isTunning: bool = False,
    ) -> None:
        """
        Args:
            target: str, # Nome da coluna onde está o valor alvo (Y)
            isTunning = None # Fazer o Tunning de hyperparâmetros se for True
        """
        super().__init__(name)
        self.target = target
        self.isTunning = isTunning
        self.isMonetary = isMonetary

    @abstractmethod
    def on_run(self, dfRFM: pd.DataFrame) -> pd.DataFrame:
        """
            Dado um dataset com os valores de RFM, retorna a predição do número de transações esperadas
        """
        self.data_predict = self.task_in["data_predict"].output.copy()
        self.data_training = self.task_in["data_training"].output.copy()

    @abstractmethod
    def predict(self):
        """
            Dado um período, retorna o número de transações esperadas até ele
        """
        pass

    @abstractmethod
    def fit(self):
        """
            Treina o modelo com os dados passados
        """
        pass

    @abstractmethod
    def rating(self):
        """
            Retorna a classificação do modelo
        """
        pass

