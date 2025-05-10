Aqui está uma explicação detalhada sobre cada uma das métricas de erro implementadas no método `rating`:

---

### 1. **MSE (Mean Squared Error - Erro Quadrático Médio)**
   - **O que é:** Mede o erro médio ao quadrado entre os valores reais (`Y_test`) e os valores previstos (`predict`).
   - **Fórmula:**  
     \[
     \text{MSE} = \frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2
     \]
   - **Interpretação:**  
     - Penaliza mais os erros maiores devido ao uso do quadrado.
     - Quanto menor o MSE, melhor o modelo.
   - **Uso:** É útil para identificar grandes discrepâncias entre os valores reais e previstos.

---

### 2. **MAE (Mean Absolute Error - Erro Absoluto Médio)**
   - **O que é:** Mede o erro médio absoluto entre os valores reais e previstos.
   - **Fórmula:**  
     \[
     \text{MAE} = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i|
     \]
   - **Interpretação:**  
     - É menos sensível a outliers do que o MSE, pois não eleva os erros ao quadrado.
     - Quanto menor o MAE, melhor o modelo.
   - **Uso:** Ideal para cenários onde outliers não devem ter um impacto significativo.

---

### 3. **R² (Coeficiente de Determinação)**
   - **O que é:** Mede a proporção da variância dos dados que é explicada pelo modelo.
   - **Fórmula:**  
     \[
     R^2 = 1 - \frac{\text{SSE}}{\text{SST}}
     \]
     Onde:
     - \( \text{SSE} = \sum_{i=1}^n (y_i - \hat{y}_i)^2 \) (Soma dos Erros ao Quadrado)
     - \( \text{SST} = \sum_{i=1}^n (y_i - \bar{y})^2 \) (Soma Total dos Quadrados)
   - **Interpretação:**  
     - \( R^2 = 1 \): O modelo explica 100% da variância dos dados.
     - \( R^2 = 0 \): O modelo não explica nada além da média dos dados.
     - \( R^2 < 0 \): O modelo é pior do que simplesmente usar a média como previsão.
   - **Uso:** Avalia a qualidade geral do ajuste do modelo.

---

### 4. **RMSE (Root Mean Squared Error - Raiz do Erro Quadrático Médio)**
   - **O que é:** É a raiz quadrada do MSE, trazendo o erro para a mesma escala dos valores reais.
   - **Fórmula:**  
     \[
     \text{RMSE} = \sqrt{\text{MSE}}
     \]
   - **Interpretação:**  
     - Quanto menor o RMSE, melhor o modelo.
     - É mais interpretável do que o MSE, pois está na mesma unidade dos valores reais.
   - **Uso:** Útil para entender o erro médio em termos absolutos na mesma escala dos dados.

---

### 5. **MAPE (Mean Absolute Percentage Error - Erro Percentual Absoluto Médio)**
   - **O que é:** Mede o erro médio absoluto em termos percentuais.
   - **Fórmula:**  
     \[
     \text{MAPE} = \frac{1}{n} \sum_{i=1}^n \left| \frac{y_i - \hat{y}_i}{y_i} \right| \times 100
     \]
   - **Interpretação:**  
     - Representa o erro médio como uma porcentagem dos valores reais.
     - Quanto menor o MAPE, melhor o modelo.
     - Pode ser problemático se os valores reais (\( y_i \)) forem muito próximos de zero.
   - **Uso:** Útil para interpretar o erro em termos percentuais, especialmente em problemas de negócios.

---

### 6. **MedAE (Median Absolute Error - Mediana do Erro Absoluto)**
   - **O que é:** Mede a mediana dos erros absolutos entre os valores reais e previstos.
   - **Fórmula:**  
     \[
     \text{MedAE} = \text{Mediana}(|y_i - \hat{y}_i|)
     \]
   - **Interpretação:**  
     - É robusta a outliers, pois usa a mediana em vez da média.
     - Quanto menor o MedAE, melhor o modelo.
   - **Uso:** Ideal para cenários onde os outliers podem distorcer outras métricas, como o MAE.

---

### Resumo das Métricas e Seus Usos

| **Métrica** | **Sensível a Outliers?** | **Escala** | **Uso Principal** |
|-------------|---------------------------|------------|--------------------|
| **MSE**     | Sim                       | Quadrática | Penalizar grandes erros. |
| **MAE**     | Não                       | Linear     | Avaliar erros médios absolutos. |
| **R²**      | Não                       | Sem unidade | Avaliar a qualidade geral do modelo. |
| **RMSE**    | Sim                       | Linear     | Interpretar o erro médio na escala dos dados. |
| **MAPE**    | Sim (próximo de zero)     | Percentual | Interpretar o erro em termos percentuais. |
| **MedAE**   | Não                       | Linear     | Avaliar erros absolutos ignorando outliers. |

---

### Conclusão
Cada métrica tem seu propósito e limitações. Para uma análise completa, é recomendável usar várias métricas em conjunto. Por exemplo, o MSE e o RMSE são úteis para identificar grandes erros, enquanto o MAE e o MedAE são mais robustos a outliers. O R² ajuda a entender a qualidade geral do modelo, e o MAPE é útil para interpretar o erro em termos percentuais.

Quando temos outliers nos dados, algumas métricas de avaliação tradicionais como MSE ou RMSE podem ser enganosas, porque elas penalizam fortemente erros grandes (quadráticos), fazendo parecer que o modelo é pior do que realmente é — mesmo que só esteja errando em poucos pontos extremos.

#### Melhores métricas para avaliar modelos com outliers:
🔹 1. MAE (Mean Absolute Error)

    Resistente a outliers.

    Como usa valores absolutos, trata todos os erros da mesma forma, sem elevar ao quadrado.

    Boa no geral, especialmente se você quer saber o erro médio real.

🔹 2. MedAE (Mediana do Erro Absoluto)

    Muito robusta contra outliers.

    Mostra o erro típico (mediano), ignorando completamente valores extremos.

    Excelente quando os dados têm muitos outliers ou distribuição assimétrica.