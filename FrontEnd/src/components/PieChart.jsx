import React from "react";
import { Pie } from "react-chartjs-2";
import "chart.js/auto";
import { Chart as ChartJS, Tooltip } from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";

ChartJS.register(ChartDataLabels);

const PieChart = ({ data }) => {
  const order = [
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

  const orderedData = order
    .map((tipo, index) => {
      const entry = Object.values(data).find((item) => item.Tipo === tipo);
      return entry
        ? { ...entry, Cor: colors[index] }
        : { Tipo: tipo, Porcentagem: 0, ValorAbsoluto: 0, Cor: colors[index] };
    })
    .filter((item) => item.Porcentagem > 0); // Filtra valores com porcentagem maior que 0

  const chartData = {
    labels: orderedData.map((item) => item.Tipo),
    datasets: [
      {
        data: orderedData.map((item) =>
          parseFloat(item.Porcentagem.toFixed(2))
        ),
        backgroundColor: orderedData.map((item) => item.Cor),
        borderWidth: 1,
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            const index = context.dataIndex;
            const valorAbsoluto = orderedData[index].ValorAbsoluto.toFixed(2);
            const porcentagem = orderedData[index].Porcentagem.toFixed(2);
            return `Valor Absoluto: ${valorAbsoluto}\nPorcentagem: ${porcentagem}%`;
          },
        },
      },
      datalabels: {
        formatter: (value) => `${value}%`,
        color: "#000",
        anchor: "end",
        align: "end",
        font: {
          size: 13,
        },
      },
    },
    layout: {
      padding: {
        top: 20,
        bottom: 50,
        left: 50,
        right: 50,
      },
    },
  };

  return <Pie data={chartData} options={options} />;
};

export default PieChart;
