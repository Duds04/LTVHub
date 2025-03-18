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
import ErrorModal from "../components/ErrorModal"; // Importando o ErrorModal
import LoadingModal from "../components/LoadingModal"; // Importando o LoadingModal

const DetalheCliente = () => {
  const { id } = useParams(); // Captura o ID do cliente da URL
  const navigate = useNavigate(); // Hook de navegação

  // Estado para armazenar os dados do cliente e compras
  const [cliente, setCliente] = useState(null);
  const [compras, setCompras] = useState([]);
  const [error, setError] = useState(null); // Estado para controlar a mensagem de erro
  const [loading, setLoading] = useState(true); // Estado para controlar o carregamento

  // Função para buscar os dados do cliente do backend
  useEffect(() => {
    const fetchClienteData = async () => {
      try {
        const response = await fetch(`/cliente/${id}`);
        const data = await response.json();
        if (response.ok) {
          setCliente(data);
          setCompras(data.transactions); // Atualiza o estado de compras com os dados de transactions
        } else {
          console.error("Erro ao buscar dados do cliente:", data.error);
          setError(data.error || "Erro ao buscar dados do cliente.");
        }
      } catch (error) {
        console.error("Erro ao buscar dados do cliente:", error);
        setError("Erro ao buscar dados do cliente.");
      } finally {
        setLoading(false); // Define o estado de carregamento como falso após a conclusão da solicitação
      }
    };

    fetchClienteData();
  }, [id]);

  // Função para obter dados para o gráfico de barras (soma das compras por mês e por ano)
  const getLastPurchasesData = () => {
    const purchasesByYearMonth = {};

    compras.forEach((compra) => {
      const dateParts = compra.date.split("/");
      const year = dateParts[2];
      const month = parseInt(dateParts[1], 10) - 1; // Subtrai 1 para ajustar ao índice do array (0-11)

      const yearMonthKey = `${year}-${month < 9 ? `0${month + 1}` : month + 1}`; // Combina ano e mês no formato "YYYY-MM"

      if (!purchasesByYearMonth[yearMonthKey]) {
        purchasesByYearMonth[yearMonthKey] = 0;
      }

      purchasesByYearMonth[yearMonthKey] += compra.monetary; // Somando o valor das compras por mês/ano
    });

    // Formatação dos dados para o gráfico
    const formattedData = [];
    for (const yearMonth in purchasesByYearMonth) {
      const [year, month] = yearMonth.split("-");
      const monthName = new Date(0, parseInt(month) - 1).toLocaleString(
        "default",
        { month: "short" }
      );
      formattedData.push({
        year,
        month: `${monthName}/${year}`, // Formato Mês/Ano
        total: parseFloat(purchasesByYearMonth[yearMonth].toFixed(2)),
      });
    }

    return formattedData;
  };

  const lastPurchasesData = getLastPurchasesData();
  console.log(lastPurchasesData); // Para verificar os dados do gráfico

  // Configuração da tabela
  const columns = React.useMemo(
    () => [
      {
        Header: "ID da Transação",
        accessor: "id_transaction",
      },
      {
        Header: "Valor da Transação",
        accessor: "monetary",
        Cell: ({ value }) => `$${parseFloat(value).toFixed(2)}`, // Adiciona o símbolo de dólar à coluna "monetary"
      },
      {
        Header: "Data da Compra",
        accessor: "date",
        disableSortBy: true,
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
      initialState: {
        pageSize: 5,
        sortBy: [{ id: "id_transaction", desc: false }],
      }, // Ordenação padrão pela coluna "ID da Transação"
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
      {loading && <LoadingModal />}{" "}
      {/* Exibe o LoadingModal enquanto os dados estão sendo carregados */}
      {cliente && (
        <h1 className={stylesDetalheCliente.title}>
          DETALHE DO CLIENTE {cliente.id}
        </h1>
      )}
      <div className={stylesDetalheCliente.split}>
        <div className={stylesDetalheCliente.left}>
          {/* Informações do cliente */}
          {cliente && (
            <div className={stylesDetalheCliente.clientDetails}>
              <h2 className={stylesDetalheCliente.clientId}>
                ID do Cliente:{" "}
                <span className={stylesDetalheCliente.id}>{id}</span>
              </h2>
              <h2 className={stylesDetalheCliente.clientType}>
                {" "}
                <strong>Tipo de Cliente: </strong>
                {cliente.type}
              </h2>
              <p>
                <strong>Descrição do Tipo: </strong> {cliente.description}
              </p>
              <p>
                <strong>Como Lidar com Esse Tipo de Cliente: </strong>
                {cliente.howToManage}
              </p>
              <p>
                <strong>Número Esperado de Transações: </strong>
                {cliente.frequency}
              </p>
              <p>
                <strong>Valor Esperado por Transação: </strong> $
                {cliente.monetary_value.toFixed(2)}
              </p>
              <p>
                <strong>LTV:</strong> ${cliente.CLV.toFixed(2)}
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
                        className={stylesDetalheCliente.tableHeader}
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
            <ResponsiveContainer width="100%" height={500}>
              <BarChart
                data={lastPurchasesData}
                margin={{ top: 20, right: 30, left: 20, bottom: 80 }} // Aumente a margem inferior
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="month"
                  angle={-45} 
                  textAnchor="end" 
                  interval={0} 
                  label={{ value: "Tempo (Mês/Ano)", position: "insideBottom", dy: 75 }} 
                />
                <YAxis
                  label={{
                    value: "Valor Esperado ($)",
                    angle: -90,
                    position: "insideLeft",
                    dy: 50,
                  }}
                />
                <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
                <Legend verticalAlign="top" height={36} align="center" />
                <Bar
                  dataKey="total"
                  name="Total ($)"
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
      {/* Modal de erro */}
      {error && <ErrorModal message={error} onClose={() => setError(null)} />}
    </div>
  );
};

export default DetalheCliente;
