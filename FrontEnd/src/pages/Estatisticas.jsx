import React from "react";
import stylesEstatisticas from "../style/Estatisticas.module.css";
import isConfigurateModel from "../components/isConfigurateModel"; // Importando o HOC

const Estatisticas = () => {
  return (
    <div className={stylesEstatisticas.container}>
      <h1 className={stylesEstatisticas.title}>ESTATÍSTICAS</h1>

      <div className={stylesEstatisticas.graphRow}>
        {/* Gráfico 1 */}
        <div className={stylesEstatisticas.graphContainer}>
          <h3 className={stylesEstatisticas.graphTitle}>Distribuição Percentual pelos Tipos de Clientes</h3>
          <div className={stylesEstatisticas.graphContent}>

            <img
              src="http://localhost:5000/images/clientsPie_chart.svg"
              alt="Gráfico de Compras"
              className={stylesEstatisticas.graphImage}
            />
            <img
              src="http://localhost:5000/images/clientsPie_legend.svg"
              alt="Legenda Gráfico de Compras"
              className={stylesEstatisticas.graphLegend}
            />
            </div>
        </div>

        {/* Gráfico 2 */}
        <div className={stylesEstatisticas.graphContainer}>
          <h3 className={stylesEstatisticas.graphTitle}>
            Distribuição Percentual do Valor Monetário pelos Tipos de Clientes
          </h3>
          <div className={stylesEstatisticas.graphContent}>
            <img
              src="http://localhost:5000/images/frequencyPie_chart.svg"
              alt="Gráfico de Vendas"
              className={stylesEstatisticas.graphImage}
            />
            <img
              src="http://localhost:5000/images/frequencyPie_legend.svg"
              alt="Legenda Gráfico de Compras"
              className={stylesEstatisticas.graphLegend}
            />
          </div>
        </div>
      </div>

      <div className={stylesEstatisticas.graphRow}>
        {/* Gráfico 3 */}
        <div className={stylesEstatisticas.graphContainer}>
          <h3 className={stylesEstatisticas.graphTitle}>Distribuição Percentual das Compras pelos Tipos de Clientes</h3>
          <div className={stylesEstatisticas.graphContent}>

            <img
              src="http://localhost:5000/images/monetaryPie_chart.svg"
              alt="Gráfico de Taxa de Conversão"
              className={stylesEstatisticas.graphImage}
            />
            <img
              src="http://localhost:5000/images/monetaryPie_legend.svg"
              alt="Legenda Gráfico de Taxa de Conversão"
              className={stylesEstatisticas.graphLegend}
            />
          </div>

        </div>
      </div>
    </div>
  );
};

export default isConfigurateModel(Estatisticas);
