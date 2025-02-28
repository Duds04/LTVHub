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

  // Função para obter dados para o gráfico de barras (soma das compras por mês)
  const getLastPurchasesData = () => {
    const months = Array(12).fill(0);
    compras.forEach((compra) => {
      const dateParts = compra.date.split('/');
      const month = parseInt(dateParts[1], 10) - 1; // Subtrai 1 para ajustar ao índice do array (0-11)
      months[month] += compra.monetary; // Somando o valor das compras por mês
    });
    return months.map((value, index) => ({
      month: new Date(0, index).toLocaleString("default", { month: "short" }),
      total: parseFloat(value.toFixed(2)), // Arredondando o valor total para dois dígitos
    }));
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
        Header: "Valor da Compra",
        accessor: "monetary",
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
      initialState: { pageSize: 5, sortBy: [{ id: "id_transaction", desc: false }] }, // Ordenação padrão pela coluna "ID da Transação"
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
      {loading && <LoadingModal />} {/* Exibe o LoadingModal enquanto os dados estão sendo carregados */}
      {cliente && (<h1 className={stylesDetalheCliente.title}>DETALHE DO CLIENTE {cliente.id}</h1>)}

      <div className={stylesDetalheCliente.split}>
        <div className={stylesDetalheCliente.left}>
          {/* Informações do cliente */}
          {cliente && (
            <div className={stylesDetalheCliente.clientDetails}>
              <h2 className={stylesDetalheCliente.clientId}>ID do Cliente: <span className={stylesDetalheCliente.id}>{id}</span></h2> 
              <h2 className={stylesDetalheCliente.clientType}> <strong>Tipo de Cliente: </strong>{cliente.type}</h2>
              <p>
                <strong>Descrição do Tipo: </strong> {cliente.description}
              </p>
              <p>
                <strong>Como Lidar com Esse Tipo de Cliente: </strong>
                {cliente.howToManage}
              </p>
              <p>
                <strong>Número Esperado de Compras: </strong>
                {cliente.frequency}
              </p>
              <p>
                <strong>Valor Esperado por Compra: </strong> $
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
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={lastPurchasesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar
                  dataKey="total"
                  name = "Total"
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