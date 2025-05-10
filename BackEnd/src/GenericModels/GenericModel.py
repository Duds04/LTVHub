from src.workflows.task import Task
import pandas as pd
from abc import abstractmethod
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error

# usados pelo Machine Learning (tem o Y independente)


class GenericModelTask(Task):
    def __init__(
        self,
        name: str,
        target: str,
        isMonetary: bool,
        isTunning: bool = False,
        isRating: bool = False,
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
        self.isRating = isRating

    @abstractmethod
    def on_run(self, dfRFM: pd.DataFrame) -> pd.DataFrame:
        """
            Dado um dataset com os valores de RFM, retorna a predição do número de transações esperadas
        """
        self.data_predict = self.task_in["data_predict"].output
        self.data_training = self.task_in["data_training"].output

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

        # Cálculo da Mediana do Erro Absoluto
        from sklearn.metrics import median_absolute_error
        medae = median_absolute_error(yTrue, expected)
        print("Mediana do Erro Absoluto (MedAE):", medae)

        if (yTrue != 0).any(): 
            valid_indices = yTrue != 0  
            mape = (abs(yTrue[valid_indices] - expected[valid_indices]
                        ) / yTrue[valid_indices]).mean() * 100
            print("Mean Absolute Percentage Error (MAPE):", mape, "%")
            mean_relative_error = (abs(yTrue[valid_indices] - expected[valid_indices]) / abs(yTrue[valid_indices])).mean()
            print("Erro Relativo Médio:", mean_relative_error)
        else:
            # Define como infinito se todos os valores de yTrue forem zero
            mean_relative_error = float('inf')
            print("Mean Absolute Percentage Error (MAPE): Não pode ser calculado (todos os valores de monetary_value são zero).")
            print("Erro Relativo Médio: inf (todos os valores de monetary_value são zero)")

        return mse
