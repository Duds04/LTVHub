from src.workflows.task import Task
import pandas as pd
from abc import abstractmethod
from sklearn.metrics import mean_squared_error

class MonetaryModelTask(Task):
    def __init__(
        self,
        name: str,
        isTunning: bool = False,
        isRating: bool = False,
    ) -> None:
        """
        Args:
        """
        super().__init__(name)
        self.model = None
        self.isTunning = isTunning
        self.isRating = isRating

    @abstractmethod
    def on_run(self, dfRFM: pd.DataFrame) -> pd.DataFrame:
        """
            Dado um dataset com os valores de RFM, retorna a predição do número de transações esperadas
        """
        self.data_predict = self.task_in["data_predict"].output
        self.data_training = self.task_in["data_training"].output

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

    @abstractmethod
    def rating(self, expected: pd.Series, yTrue: pd.Series) -> float:
        """
        Retorna a classificação do cliente e calcula métricas de erro.

        Args:
            expected (pd.Series): Valores previstos (ExpectedMonetary).
            yTrue (pd.Series): Valores reais (monetary_value).

        Returns:
            float: Mean Squared Error (MSE) calculado.
        """
        # Imprime o intervalo dos valores reais (yTrue)
        print("Intervalo de monetary_value (valores reais):")
        print("Mínimo:", yTrue.min())
        print("Máximo:", yTrue.max())
        print()

        # Imprime o intervalo das previsões (expected)
        print("Intervalo de ExpectedMonetary (valores previstos):")
        print("Mínimo:", expected.min())
        print("Máximo:", expected.max())
        print()

        # Cálculo do MSE
        mse = mean_squared_error(yTrue, expected)
        print("Model Mean Squared Error (MSE):", mse)

        # Cálculo do MAE
        from sklearn.metrics import mean_absolute_error
        mae = mean_absolute_error(yTrue, expected)
        print("Model Mean Absolute Error (MAE):", mae)

        # Cálculo do RMSE
        import numpy as np
        rmse = np.sqrt(mse)
        print("Root Mean Squared Error (RMSE):", rmse)

        # Cálculo do MAPE (tratando valores zero em yTrue)
        non_zero_indices = yTrue != 0  # Filtra índices onde yTrue não é zero
        if non_zero_indices.any():  # Verifica se há valores válidos
            mape = (abs(yTrue[non_zero_indices] - expected[non_zero_indices]) / yTrue[non_zero_indices]).mean() * 100
            print("Mean Absolute Percentage Error (MAPE):", mape, "%")
        else:
            print("Mean Absolute Percentage Error (MAPE): Não pode ser calculado (todos os valores de monetary_value são zero).")

        # Cálculo da Mediana do Erro Absoluto
        from sklearn.metrics import median_absolute_error
        medae = median_absolute_error(yTrue, expected)
        print("Mediana do Erro Absoluto (MedAE):", medae)

        if (yTrue != 0).all():  # Verifica se todos os valores de yTrue são diferentes de zero
            mean_relative_error = (abs(yTrue - expected) / abs(yTrue)).mean()
            print("Erro Relativo Médio:", mean_relative_error)
        else:
            mean_relative_error = float('inf')  # Define como infinito se houver divisão por zero
            print("Erro Relativo Médio: inf (divisão por zero detectada)")
            print()

        print()

        return mse