import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useTable, usePagination, useSortBy } from "react-table";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { FaSort, FaSortUp, FaSortDown } from "react-icons/fa"; // Importando os ícones do React Icons
import stylesDetalheCliente from "../style/DetalheCliente.module.css";

// Dados simulados de compras para demonstrar
const compraData = [
  { id: 1, valor: 200, data: "2024-01-15", clienteId: 1 },
  { id: 2, valor: 250, data: "2024-02-20", clienteId: 1 },
  { id: 3, valor: 300, data: "2024-03-05", clienteId: 1 },
  { id: 4, valor: 150, data: "2024-04-11", clienteId: 2 },
  { id: 5, valor: 220, data: "2024-05-25", clienteId: 2 },
  { id: 6, valor: 170, data: "2024-06-12", clienteId: 1 },
  { id: 7, valor: 210, data: "2024-07-22", clienteId: 3 },
  { id: 8, valor: 180, data: "2024-08-13", clienteId: 1 },
  { id: 9, valor: 260, data: "2024-09-04", clienteId: 2 },
  { id: 10, valor: 300, data: "2024-10-17", clienteId: 1 },
  { id: 11, valor: 150, data: "2024-11-05", clienteId: 3 },
  { id: 12, valor: 280, data: "2024-12-02", clienteId: 1 },
];

const DetalheCliente = () => {
  const { id } = useParams(); // Captura o ID do cliente da URL
  const navigate = useNavigate(); // Hook de navegação

  // Estado para armazenar os dados do cliente e compras
  const [cliente, setCliente] = useState(null);
  const [compras, setCompras] = useState([]);

  // Simulação de busca de dados do cliente por ID
  useEffect(() => {
    const clienteData = {
      1: {
        tipo: "Cliente A",
        descricaoTipo: "Clientes com alto LTV e frequentes compras.",
        comoLidar:
          "Oferecer programas de fidelidade e descontos para aumento da recorrência.",
        numCompras: 12,
        valorPorCompra: 250,
        LTV: 3000,
      },
      2: {
        tipo: "Cliente B",
        descricaoTipo: "Clientes com compras esporádicas.",
        comoLidar: "Enviar promoções ocasionais e buscar fidelização.",
        numCompras: 8,
        valorPorCompra: 180,
        LTV: 1500,
      },
      3: {
        tipo: "Cliente C",
        descricaoTipo: "Clientes com baixo valor de compras.",
        comoLidar:
          "Melhorar o engajamento e incentivos para aumento do ticket médio.",
        numCompras: 5,
        valorPorCompra: 120,
        LTV: 800,
      },
    };

    setCliente(clienteData[id]);
    setCompras(
      compraData.filter((compra) => compra.clienteId === parseInt(id))
    );
  }, [id]);

  // Função para obter dados para o gráfico de barras (soma das compras por mês)
  const getLastPurchasesData = () => {
    const months = Array(12).fill(0);
    compras.forEach((compra) => {
      const month = new Date(compra.data).getMonth(); // 0-11
      months[month] += compra.valor; // Somando o valor das compras por mês
    });
    return months.map((value, index) => ({
      month: new Date(0, index).toLocaleString("default", { month: "short" }),
      total: value, // Total de compras para aquele mês
    }));
  };

  const lastPurchasesData = getLastPurchasesData();
  console.log(lastPurchasesData); // Para verificar os dados do gráfico

  // Configuração da tabela
  const columns = React.useMemo(
    () => [
      {
        Header: "ID da Compra",
        accessor: "id",
      },
      {
        Header: "Valor da Compra",
        accessor: "valor",
      },
      {
        Header: "Data da Compra",
        accessor: "data",
      },
    ],
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    page,
    canPreviousPage,
    canNextPage,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    state: { pageIndex },
  } = useTable(
    {
      columns,
      data: compras,
      initialState: { pageSize: 5, sortBy: [{ id: "id", desc: false }] }, // Ordenação padrão pela coluna "ID"
    },
    useSortBy,
    usePagination
  );

  // Função para voltar à página de clientes
  const handleGoBack = () => {
    navigate("/clientes"); // Navega para a URL /clientes
  };

  return (
    <div className={stylesDetalheCliente.container}>
      <h1 className={stylesDetalheCliente.title}>DETALHE DO CLIENTE</h1>

      <div className={stylesDetalheCliente.split}>
        <div className={stylesDetalheCliente.left}>
          {/* Informações do cliente */}
          {cliente && (
            <div className={stylesDetalheCliente.clientDetails}>
              <h2>Tipo de Cliente: {cliente.tipo}</h2>
              <p>
                <strong>Descrição do Tipo:</strong> {cliente.descricaoTipo}
              </p>
              <p>
                <strong>Como Lidar com Esse Tipo de Cliente:</strong>{" "}
                {cliente.comoLidar}
              </p>
              <p>
                <strong>Número Esperado de Compras:</strong>{" "}
                {cliente.numCompras}
              </p>
              <p>
                <strong>Valor Esperado por Compra:</strong> $
                {cliente.valorPorCompra.toFixed(2)}
              </p>
              <p>
                <strong>LTV:</strong> ${cliente.LTV.toFixed(2)}
              </p>
            </div>
          )}

          {/* Tabela de compras */}
          <div className={stylesDetalheCliente.tableContainer}>
            <table {...getTableProps()} className={stylesDetalheCliente.table}>
              <thead>
                {headerGroups.map((headerGroup) => (
                  <tr {...headerGroup.getHeaderGroupProps()}>
                    {headerGroup.headers.map((column) => (
                      <th
                        {...column.getHeaderProps(
                          column.getSortByToggleProps()
                        )}
                      >
                        {column.render("Header")}
                        <span>
                          {column.isSorted ? (
                            column.isSortedDesc ? (
                              <FaSortDown />
                            ) : (
                              <FaSortUp />
                            )
                          ) : (
                            <FaSort />
                          )}{" "}
                          {/* Ícones de ordenação com React Icons */}
                        </span>
                      </th>
                    ))}
                  </tr>
                ))}
              </thead>
              <tbody {...getTableBodyProps()}>
                {page.map((row) => {
                  prepareRow(row);
                  return (
                    <tr {...row.getRowProps()}>
                      {row.cells.map((cell) => {
                        return (
                          <td {...cell.getCellProps()}>
                            {cell.render("Cell")}
                          </td>
                        );
                      })}
                    </tr>
                  );
                })}
              </tbody>
            </table>

            {/* Paginação da tabela */}
            <div className={stylesDetalheCliente.pagination}>
              <button
                onClick={() => gotoPage(0)}
                disabled={!canPreviousPage}
                className={stylesDetalheCliente.pageButton}
              >
                {"<<"}
              </button>
              <button
                onClick={() => previousPage()}
                disabled={!canPreviousPage}
                className={stylesDetalheCliente.pageButton}
              >
                {"<"}
              </button>
              <span>
                Página {pageIndex + 1} de {pageCount}
              </span>
              <button
                onClick={() => nextPage()}
                disabled={!canNextPage}
                className={stylesDetalheCliente.pageButton}
              >
                {">"}
              </button>
              <button
                onClick={() => gotoPage(pageCount - 1)}
                disabled={!canNextPage}
                className={stylesDetalheCliente.pageButton}
              >
                {">>"}
              </button>
            </div>
          </div>
        </div>

        {/* Gráfico de barras - Soma das compras por mês */}
        <div className={stylesDetalheCliente.chartContainer}>
          {lastPurchasesData.length > 0 ? (
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={lastPurchasesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar
                  dataKey="total"
                  fill="#006822"
                  radius={[10, 10, 0, 0]}
                  background={{ fill: "#D8E7DE" }}
                />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p>Nenhum dado para exibir no gráfico.</p>
          )}
        </div>
      </div>

      <button
        onClick={handleGoBack}
        className={stylesDetalheCliente.backButton}
      >
        Voltar para Clientes
      </button>
    </div>
  );
};

export default DetalheCliente;
