import React, { useEffect, useState } from "react";
import stylesEstatisticas from "../style/Estatisticas.module.css";
import isConfigurateModel from "../components/isConfigurateModel"; // Importando o HOC
import PieChart from "../components/PieChart"; // Componente para renderizar gráficos de pizza
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

const Estatisticas = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [hiddenCategories, setHiddenCategories] = useState([]);
  const [ltvData, setLtvData] = useState(null);

  const clientOrder = [
    "Cliente de alto valor",
    "Cliente de desenvolvimento estratégico",
    "Cliente em fase de proteção",
    "Cliente de retenção crítica",
    "Cliente de valor geral",
    "Cliente em desenvolvimento",
    "Cliente de retenção geral",
    "Cliente perdido",
  ];

  const colors = [
    "#003436",
    "#005843",
    "#007252",
    "#008D60",
    "#00A86B",
    "#66BFA1",
    "#99D1BA",
    "#B2D1BD",
  ];

  const toggleCategory = (category) => {
    setHiddenCategories((prev) =>
      prev.includes(category)
        ? prev.filter((item) => item !== category)
        : [...prev, category]
    );
  };

  const filteredLtvData = ltvData?.filter(
    (item) => !hiddenCategories.includes(item.TipoCliente)
  );

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5000/plot_data");
        const result = await response.json();
        if (response.ok) {
          setData(result);
          setLtvData(result.ltv_by_client_type);
        } else {
          setError(result.error || "Erro ao carregar os dados.");
        }
      } catch (err) {
        setError("Erro ao buscar os dados do backend.");
      }
    };

    fetchData();
  }, []);

  if (error) {
    return <div className={stylesEstatisticas.error}>{error}</div>;
  }

  if (!data) {
    return <div className={stylesEstatisticas.loading}>Carregando...</div>;
  }

  const filteredData = (chartData) => {
    return Object.fromEntries(
      Object.entries(chartData).filter(
        ([key, value]) => !hiddenCategories.includes(value.Tipo)
      )
    );
  };

  return (
    <div className={stylesEstatisticas.container}>
      <h1 className={stylesEstatisticas.title}>ESTATÍSTICAS</h1>

      <div className={stylesEstatisticas.graphRow}>
        {/* Gráfico 1 */}
        <div className={stylesEstatisticas.graphContainer}>
          <h3 className={stylesEstatisticas.graphTitle}>
            Distribuição Percentual pelos Tipos de Clientes
          </h3>
          <PieChart data={filteredData(data.clients)} />
        </div>

        {/* Gráfico 2 */}
        <div className={stylesEstatisticas.graphContainer}>
          <h3 className={stylesEstatisticas.graphTitle}>
            Distribuição Percentual do Valor Monetário pelos Tipos de Clientes
          </h3>
          <PieChart data={filteredData(data.monetary)} />
        </div>

        {/* Gráfico 3 */}
        <div className={stylesEstatisticas.graphContainer}>
          <h3 className={stylesEstatisticas.graphTitle}>
            Distribuição Percentual das Transações pelos Tipos de Clientes
          </h3>
          <PieChart
            data={filteredData(data.frequency)}
            className={stylesEstatisticas.graph}
          />
        </div>
      </div>

      {/* Gráfico de LTV */}
      <div className={stylesEstatisticas.graphContainerLTV}>
        <h3 className={stylesEstatisticas.graphTitle}>
          LTV Agregado por Tipo de Cliente (Ranking)
        </h3>
        <ResponsiveContainer width="100%" minHeight={400}>
          <BarChart
            data={filteredLtvData}
            layout="vertical"
            margin={{ top: 20, right: 30, left: 10, bottom: 20 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" tickCount={7} />
            <YAxis type="category" dataKey="TipoCliente" width={140} />
            <Tooltip />
            <Bar dataKey="CLV">
              {filteredLtvData.map((entry, index) => {
                const tipoIndex = clientOrder.indexOf(entry.TipoCliente);
                const color = colors[tipoIndex] || "#ccc";
                return <Cell key={`cell-${index}`} fill={color} />;
              })}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Legenda compartilhada */}
      <div className={stylesEstatisticas.legendContainer}>
        <ul className={stylesEstatisticas.legendList}>
          {clientOrder.map((tipo, index) => (
            <li
              key={tipo}
              style={{
                cursor: "pointer",
                opacity: hiddenCategories.includes(tipo) ? 0.5 : 1, // Reduz a opacidade para indicar que está oculto
              }}
              onClick={() => toggleCategory(tipo)}
            >
              <span
                style={{
                  display: "inline-block",
                  width: "1.6vmin",
                  height: "1.6vmin",
                  backgroundColor: colors[index],
                  marginRight: "10px",
                }}
              ></span>
              {tipo}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default isConfigurateModel(Estatisticas);
