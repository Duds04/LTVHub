import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, median_absolute_error
from sklearn.preprocessing import StandardScaler

import numpy as np
import xgboost as xgb
import lightgbm as lgb
from sklearn.linear_model import ElasticNet, LassoCV
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor, RandomForestRegressor

from src.GenericModels.GenericModel import GenericModelTask


class MachineLearningModelTask(GenericModelTask):
    """
        Instância diversos modelos de Machine Learning para prever o target e pega o mais adequado
    """

    def __init__(
        self,
        name: str,
        target: str,
        isMonetary: bool,
        X_Columns: list = None,
        isTunning: bool = False,
        isRating: bool = False,
    ) -> None:
        """
        Args:
            name, # Nome da tarefa
            target, # Nome da coluna onde está o valor alvo (Y)
            isTunning, # Fazer o Tunning de hyperparâmetros se for True
        """
        super().__init__(name, target, isMonetary, isTunning, isRating)
        self.models = self.createModels()

        self.bestModel = None

        self.X_Columns = X_Columns

        self.X_train = None
        self.X_test = None
        self.Y_train = None
        self.Y_test = None

    def on_run(self, dfRFM: pd.DataFrame) -> pd.DataFrame:
        super().on_run(dfRFM)

        if self.target not in self.data_training.columns:
            raise ValueError(
                f"Target column '{self.target}' not found in DataFrame columns: {self.data_training.columns}")

        for x_colum in self.X_Columns:
            if x_colum not in self.data_training.columns:
                raise ValueError(
                    f"Feature column '{x_colum}' not found in DataFrame columns: {self.data_training.columns}")

        X = self.data_training[self.X_Columns]
        Y = self.data_training[self.target]
        Y = Y[Y.index.isin(X.index.values)]

        # Normalizar os dados
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(
            X, np.ravel(Y.values), random_state=42)

        self.bestModel = self.selectBestModel()

        if self.isMonetary:
            xExpected = "ExpectedMonetary"
        else:
            xExpected = "ExpectedFrequency"

        self.data_predict[xExpected] = self.bestModel.predict(
            self.data_predict[["frequency", "recency", "T", "monetary_value"]])

        return self.data_predict
    
    def ratingBestModel(self, predict: pd.DataFrame) -> pd.DataFrame:
        print("Metricas do ",type(self.bestModel).__name__)
        
        return super().rating(predict, self.Y_test)
        

    def selectBestModel(self):
        """
            Seleciona o melhor modelo de acordo com o dataset passado
        """
        bestScore = None
        for model in self.models:
            score = self.fitAndRating(model)
            if bestScore is None or bestScore > score[0]:
                bestScore, self.bestModel = score

        if self.isRating:
            predict = self.predict(self.bestModel)
            self.ratingBestModel(predict)

        if self.isTunning:
            return self.bestModel.best_estimator_
        else:
            return self.bestModel

    def createModels(self):
        if self.isTunning == False:
            lasso = LassoCV()
            Enet = ElasticNet()
            rf = RandomForestRegressor()
            GBoost = GradientBoostingRegressor()
            HGBoost = HistGradientBoostingRegressor()
            model_xgb = xgb.XGBRegressor()
            model_lgb = lgb.LGBMRegressor(objective='regression', verbose=-1)

        else:
            grid = {'n_alphas' : [100,200,500,100],'max_iter' : [1000,1500,2000], 'random_state' : [42]}
            lasso = GridSearchCV(estimator=LassoCV(max_iter=5000), param_grid=grid, n_jobs=-1, scoring="neg_mean_squared_error")

            #Enet = ElasticNet()
            grid = {"max_iter": [1000,1500,2000],"alpha": [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],"l1_ratio": np.arange(0.0, 1.0, 0.1), 'random_state' : [42]}
            Enet = GridSearchCV(estimator=ElasticNet(max_iter=5000), param_grid=grid, n_jobs=-1, scoring="neg_mean_squared_error")

            #rf = RandomForestRegressor()
            grid = {'bootstrap': [True, False],'min_samples_leaf': [1, 2, 4], 'min_samples_split': [2, 5, 10], 'n_estimators': [200, 800, 1000],'random_state' : [42]}    
            rf = GridSearchCV(estimator=RandomForestRegressor(), param_grid=grid, n_jobs=-1, scoring="neg_mean_squared_error")
            
            #GBoost = GradientBoostingRegressor()
            grid = {'n_estimators':[500,1000,2000],'learning_rate':[.001,0.01,.1],'max_depth':[1,2,4],'subsample':[.5,.75,1],'random_state':[42]}
            GBoost = GridSearchCV(estimator=GradientBoostingRegressor(), param_grid=grid, n_jobs=-1, scoring="neg_mean_squared_error")
            
            #HGBoost = HistGradientBoostingRegressor()
            grid = {'learning_rate':[.001,0.01,.1],'max_depth':[1,2,4,None],'max_leaf_nodes' : [31,None],'random_state':[42]}
            HGBoost = GridSearchCV(estimator=HistGradientBoostingRegressor(), param_grid=grid, n_jobs=-1, scoring="neg_mean_squared_error")

            #model_xgb = xgb.XGBRegressor()
            grid = { 'max_depth': [3,6,10],'learning_rate': [0.01, 0.05, 0.1],'n_estimators': [100, 500, 1000],'colsample_bytree': [0.3, 0.7],'random_state':[42]}
            model_xgb = GridSearchCV(estimator=xgb.XGBRegressor(), param_grid=grid, n_jobs=-1, scoring="neg_mean_squared_error")
           
            #model_lgb = lgb.LGBMRegressor(objective='regression')
            model_lgb =GridSearchCV(estimator=lgb.LGBMRegressor(), param_grid=grid, n_jobs=-1, scoring="neg_mean_squared_error")
        
        models = [lasso, Enet, rf, GBoost, HGBoost, model_xgb, model_lgb]
        return models

    def fitAndRating(
        self,
        # Modelo que será treinado (Tem de ter a função fit e predict implementadas)
        RegressorModel
    ):
        self.fit(RegressorModel)
        predict = self.predict(RegressorModel)
        metrica = self.rating(predict)
        return metrica, RegressorModel  # Retorna o MSE e o Regressor

    def fit(self,
            # Modelo que será treinado (Tem de ter a função fit e predict implementadas)
            RegressorModel,
            ):
        """
            Treina o modelo com os dados passados
        """
        return RegressorModel.fit(self.X_train,  self.Y_train)

    def rating(self, predict) -> pd.DataFrame:
        """
            Retorna a classificação do modelo
        """
        # Utilizando o MSE, caso queira outra métrica, trocar nesta parte!
        return mean_squared_error(self.Y_test, predict)

    def predict(self, RegressorModel):
        return RegressorModel.predict(self.X_test)
