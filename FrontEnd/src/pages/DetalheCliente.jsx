import React, { useState, useEffect, useMemo } from "react";
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
import { FaSort, FaSortUp, FaSortDown } from "react-icons/fa";
import stylesDetalheCliente from "../style/DetalheCliente.module.css";
import ErrorModal from "../components/ErrorModal";
import LoadingModal from "../components/LoadingModal";
import InfoTooltip from "../components/InfoTooltip";

const DetalheCliente = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [cliente, setCliente] = useState(null);
  const [compras, setCompras] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [weeksAhead, setWeeksAhead] = useState(null);

  useEffect(() => {
    const fetchClienteData = async () => {
      try {
        const response = await fetch(`/cliente/${id}`);
        const data = await response.json();
        if (response.ok) {
          setCliente(data);
          setCompras(data.transactions);
        } else {
          setError(data.error || "Erro ao buscar dados do cliente.");
        }
      } catch (error) {
        setError("Erro ao buscar dados do cliente.");
      } finally {
        setLoading(false);
      }
    };

    fetchClienteData();
  }, [id]);

  useEffect(() => {
    const fetchWeeksAhead = async () => {
      try {
        const response = await fetch("/weeksahead");
        const data = await response.json();
        if (response.ok) {
          setWeeksAhead(data.weeksAhead);
        } else {
          console.error(data.error || "Erro ao buscar weeksAhead.");
        }
      } catch (error) {
        console.error("Erro ao buscar weeksAhead:", error);
      }
    };

    fetchWeeksAhead();
  }, []);

  const getLastPurchasesData = useMemo(() => {
    const purchasesByYearMonth = {};
    compras.forEach((compra) => {
      const [day, month, year] = compra.date.split("/");
      const key = `${year}-${month}`; 
      purchasesByYearMonth[key] =
        (purchasesByYearMonth[key] || 0) + compra.monetary;
    });

    const formattedData = Object.entries(purchasesByYearMonth).map(
      ([key, total]) => {
        const [year, month] = key.split("-");
        const monthName = new Date(0, parseInt(month) - 1).toLocaleString(
          "default",
          { month: "short" }
        );
        return {
          year,
          month: `${monthName}/${year}`,
          total: parseFloat(total.toFixed(2)),
        };
      }
    );

    if (cliente) {
      formattedData.push({
        year: "Futuro",
        month: "Previsão",
        total: 0,
        futurePrediction: parseFloat(
          (cliente.ExpectedMonetary * cliente.ExpectedFrequency).toFixed(2)
        ),
      });
    }

    return formattedData;
  }, [compras, cliente]);

  const columns = useMemo(
    () => [
      {
        Header: "ID da Transação",
        accessor: "id_transaction",
      },
      {
        Header: "Valor da Transação",
        accessor: "monetary",
        Cell: ({ value }) => `$${parseFloat(value).toFixed(2)}`,
      },
      {
        Header: "Data da Compra",
        accessor: "date",
        disableSortBy: true,
      },
      {
        Header: ({ column }) => (
          <span
            className={stylesDetalheCliente.futurePrediction}
            {...column.getSortByToggleProps()} // Aplica a funcionalidade de ordenação
          >
            Previsão Futura
            <InfoTooltip text="Valor Esperado da Transação vezes Número Esperado." />
          </span>
        ),
        accessor: "futurePrediction",
        Cell: ({ value }) =>
          value ? `$${parseFloat(value).toFixed(2)}` : "N/A",
      },
    ],
    []
  );

  const updatedCompras = useMemo(
    () => [
      ...compras,
      {
        id_transaction: "Previsão",
        monetary: cliente ? cliente.ExpectedMonetary : 0,
        date: weeksAhead ? `Período ${weeksAhead} semanas a frente` : "Futuro",
        futurePrediction: cliente
          ? cliente.ExpectedMonetary * cliente.ExpectedFrequency
          : 0,
      },
    ],
    [compras, cliente, weeksAhead]
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    page,
    prepareRow,
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
      data: updatedCompras,
      initialState: {
        pageSize: 5,
        sortBy: [{ id: "id_transaction", desc: false }],
      },
    },
    useSortBy,
    usePagination
  );

  return (
    <div className={stylesDetalheCliente.container}>
      {loading && <LoadingModal />}
      {cliente && (
        <h1 className={stylesDetalheCliente.title}>
          DETALHE DO CLIENTE {cliente.id}
        </h1>
      )}
      <div className={stylesDetalheCliente.split}>
        <div className={stylesDetalheCliente.left}>
          {cliente && (
            <div className={stylesDetalheCliente.clientDetails}>
              <h2 className={stylesDetalheCliente.clientId}>
                ID do Cliente:{" "}
                <span className={stylesDetalheCliente.id}>{id}</span>
              </h2>
              <h2 className={stylesDetalheCliente.clientType}>
                <strong>Tipo de Cliente:</strong> {cliente.type}
              </h2>
              <p>
                <strong>Descrição do Tipo:</strong> {cliente.description}
              </p>
              <p>
                <strong>Como Lidar com Esse Tipo de Cliente:</strong>{" "}
                {cliente.howToManage}
              </p>
              <p>
                <strong>Número Esperado de Transações:</strong>{" "}
                {cliente.ExpectedFrequency}
              </p>
              <p>
                <strong>Valor Esperado por Transação:</strong> $
                {cliente.ExpectedMonetary.toFixed(2)}
              </p>
              <p>
                <strong>LTV:</strong> ${cliente.CLV.toFixed(2)}
                <InfoTooltip text="Lifetime Value (LTV) é uma métrica que indica o valor total estimado que um cliente trará para a empresa ao longo do tempo." />
              </p>
            </div>
          )}

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
                        <span className={stylesDetalheCliente.sortIcon}>
                          {column.isSorted ? (
                            column.isSortedDesc ? (
                              <FaSortDown />
                            ) : (
                              <FaSortUp />
                            )
                          ) : (
                            <FaSort />
                          )}
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
                      {row.cells.map((cell) => (
                        <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
                      ))}
                    </tr>
                  );
                })}
              </tbody>
            </table>

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

        <div className={stylesDetalheCliente.chartContainer}>
          {getLastPurchasesData.length > 0 ? (
            <ResponsiveContainer width="100%" height={500}>
              <BarChart
                data={getLastPurchasesData}
                margin={{ top: 20, right: 30, left: 20, bottom: 80 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="month"
                  angle={-30}
                  textAnchor="end"
                  interval={0}
                  label={{
                    value: "Tempo (Mês/Ano)",
                    position: "insideBottom",
                    dy: 75,
                  }}
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
                />
                <Bar
                  dataKey="futurePrediction"
                  name="Previsão Futura ($)"
                  fill="#FF0000"
                  radius={[10, 10, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p>Nenhum dado para exibir no gráfico.</p>
          )}
        </div>
      </div>
      <button
        onClick={() => navigate("/clientes")}
        className={stylesDetalheCliente.backButton}
      >
        Voltar para Clientes
      </button>
      {error && <ErrorModal message={error} onClose={() => setError(null)} />}
    </div>
  );
};

export default DetalheCliente;
