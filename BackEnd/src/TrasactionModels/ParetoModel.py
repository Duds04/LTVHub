import pandas as pd
from lifetimes import ParetoNBDFitter
from sklearn.metrics import mean_squared_error
from src.TrasactionModels.TransactionModel import TransactionModelTask

class ParetoModelTask(TransactionModelTask):
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
            name, #Nome da tarefa
            isTraining = True #Caso seja para efetuar a predição em um dataset com ou sem o período de observação
            penalizer = 0.1# Coeficiente de penalização usado pelo modelo
        """
        super().__init__(name,  isTraining, penalizer, numPeriods, isRating)
        self.model = self.createModel()

    def on_run(self, dfRFM: pd.DataFrame) -> pd.DataFrame:
        super().on_run(dfRFM)
        
        self.fit(self.data_training)        
        
        self.data_predict['ExpectedFrequency'] = self.predict(self.data_predict)
        
        if self.isRating:
            self.rating()

        return self.data_predict

    def createModel(self) -> pd.DataFrame:
        pareto = ParetoNBDFitter(penalizer_coef=self.penalizer)
        return pareto

    def fit(self, df: pd.DataFrame, isTraining: bool = True):
        """
            Treina o modelo com os dados passados
        """
        # cal, holdout
        # cal --> X em momento de treino
        # holdout --> Y em momento de treino
        # sem nada é no momento de Teste, momento de previsão, final
        if isTraining:
            self.model.fit(frequency=df['frequency_cal'],
                           recency=df['recency_cal'],
                           T=df['T_cal'])
        else:
            self.model.fit(frequency=df['frequency'],
                           recency=df['recency'],
                           T=df['T'])

        return self.model

    def predict(self, df: pd.DataFrame, isTraining: bool = False) -> pd.DataFrame:
        return super().predict(df, isTraining=isTraining)

    def rating(self) -> pd.DataFrame:
        """
            Retorna a classificação do cliente
        """
        df = self.data_training.copy()
        df['ExpectedFrequency'] = self.predict(df, True)
        
        print("\n\nMetricas do modelo Pareto")
        return super().rating(df["ExpectedFrequency"], df["frequency_cal"])