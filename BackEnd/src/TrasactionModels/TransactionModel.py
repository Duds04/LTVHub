from src.workflows.task import Task
import pandas as pd
from abc import abstractmethod
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, median_absolute_error


class TransactionModelTask(Task):
    def __init__(
        self,
        name: str,
        isTraining: bool = False,
        penalizer: float = 0.1,
        numPeriods: int = 1,
        isRating: bool = False,
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

    @abstractmethod
    def rating(self, expected: pd.Series, yTrue: pd.Series) -> float:
        """
        Retorna a classificação do cliente e calcula métricas de erro.

        Args:
            expected (pd.Series): Valores previstos (ExpectedFrequency).
            yTrue (pd.Series): Valores reais (frequency).

        Returns:
            float: Mean Squared Error (MSE) calculado.
        """
        # Imprime o intervalo dos valores reais (yTrue)
        print("Intervalo de frequency (valores reais):")
        print("Mínimo:", yTrue.min())
        print("Máximo:", yTrue.max())
        print()

        # Imprime o intervalo das previsões (expected)
        print("Intervalo de ExpectedFrequency (valores previstos):")
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

        # Cálculo do R²
        from sklearn.metrics import r2_score
        r2 = r2_score(yTrue, expected)
        print("R² (Coeficiente de Determinação):", r2)

        # Cálculo do RMSE
        import numpy as np
        rmse = np.sqrt(mse)
        print("RMSE (Root Mean Squared Error):", rmse)

        # Cálculo do MAPE (tratando valores zero em yTrue)
        non_zero_indices = yTrue != 0  # Filtra índices onde yTrue não é zero
        if non_zero_indices.any():  # Verifica se há valores válidos
            mape = (abs(yTrue[non_zero_indices] - expected[non_zero_indices]) / yTrue[non_zero_indices]).mean() * 100
            print("MAPE (Mean Absolute Percentage Error):", mape, "%")
        else:
            print("MAPE (Mean Absolute Percentage Error): Não pode ser calculado (todos os valores de frequency são zero).")

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