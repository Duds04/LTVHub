import React from 'react';
import stylesEstatisticas from '../style/Estatisticas.module.css'; 
import isConfigurateModel from "../components/isConfigurateModel"; // Importando o HOC

const Estatisticas = () => {
  return (
    <div className={stylesEstatisticas.container}>
      <h1>ESTATÍSTICAS</h1>

      <div className={stylesEstatisticas.graphRow}>
        {/* Gráfico 1 */}
        <div className={stylesEstatisticas.graphContainer}>
          <h3>Porcentagem de Compras - Base de Dados</h3>
          <img 
            src="/static/react/assets/grafico_1.svg"
            alt="Gráfico de Compras"
            className={stylesEstatisticas.graphImage}
          />
          <img 
            src="/static/react/assets/legenda_grafico_1.svg"
            alt="Legenda Gráfico de Compras"
            className={stylesEstatisticas.graphLegenda}
          />
        </div>

        {/* Gráfico 2 */}
        <div className={stylesEstatisticas.graphContainer}>
          <h3>Porcentagem Compras das Classificações</h3>
          <img 
            src="/static/react/assets/grafico2.png"
            alt="Gráfico de Vendas"
            className={stylesEstatisticas.graphImage}
          />
          <img 
            src="/static/react/assets/legenda_grafico_2.svg"
            alt="Legenda Gráfico de Compras"
            className={stylesEstatisticas.graphLegenda}
          />
        </div>
      </div>

      <div className={stylesEstatisticas.graphRow}>
        {/* Gráfico 3 */}
        <div className={stylesEstatisticas.graphContainer}>
          <h3>Porcentagem Classificação de Clientes</h3>
          <img 
            src="/static/react/assets/grafico3.png"
            alt="Gráfico de Taxa de Conversão"
            className={stylesEstatisticas.graphImage}
          />
          <img 
            src="/static/react/assets/legenda_grafico_3.svg"
            alt="Legenda Gráfico de Taxa de Conversão"
            className={stylesEstatisticas.graphLegenda}
          />
        </div>

        {/* Gráfico 4 */}
        <div className={stylesEstatisticas.graphContainer}>
          <h3>Porcentagem Valor Monetário de Clientes</h3>
          <img 
            src="/static/react/assets/grafico4.png"
            alt="Gráfico de Retenção"
            className={stylesEstatisticas.graphImage}
          />
          <img 
            src="/static/react/assets/legenda_grafico_4.svg"
            alt="Legenda Gráfico de Retenção"
            className={stylesEstatisticas.graphLegenda}
          />
        </div>
      </div>
    </div>
  );
};

export default isConfigurateModel(Estatisticas);
