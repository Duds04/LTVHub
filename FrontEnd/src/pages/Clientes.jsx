import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import stylesCliente from "../style/Clientes.module.css";
import isConfigurateModel from "../components/isConfigurateModel"; // Importando o HOC
import ErrorModal from "../components/ErrorModal"; // Importando o ErrorModal
import LoadingModal from "../components/LoadingModal"; // Importando o LoadingModal

const Clientes = () => {
  const [searchTerm, setSearchTerm] = useState(""); // Termo de pesquisa
  const [filter, setFilter] = useState(""); // Filtro de tipo de cliente
  const [sortCriteria, setSortCriteria] = useState(""); // Critério de ordenação
  const [clientes, setClientes] = useState([]); // Estado para armazenar os clientes
  const [currentPage, setCurrentPage] = useState(1); // Página atual
  const [pageRangeStart, setPageRangeStart] = useState(0); // Faixa inicial da página (1-5, 6-10, etc.)
  const [error, setError] = useState(null); // Estado para controlar a mensagem de erro
  const [loading, setLoading] = useState(true); // Estado para controlar o carregamento
  const itemsPerPage = 6; // Itens por página

  const navigate = useNavigate();

  useEffect(() => {
    // Função para buscar os clientes do backend
    const fetchClientes = async () => {
      setLoading(true); // Inicia o carregamento
      try {
        const response = await fetch("/clientes");
        const data = await response.json();
        if (response.ok) {
          setClientes(data);
        } else {
          console.error("Erro ao buscar clientes:", data.error);
          setError(data.error || "Erro ao buscar clientes.");
        }
      } catch (error) {
        console.error("Erro ao buscar clientes:", error);
        setError("Erro ao buscar clientes.");
      } finally {
        setLoading(false); // Finaliza o carregamento
      }
    };

    fetchClientes();
  }, []);

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value); // Atualiza o estado de pesquisa
  };

  const handleFilterChange = (event) => {
    setFilter(event.target.value); // Atualiza o filtro de tipo de cliente
  };

  const handleSortChange = (event) => {
    setSortCriteria(event.target.value); // Atualiza o critério de ordenação
  };

  const handleDetailsClick = (id) => {
    navigate(`/cliente/${id}`); // Navega para a página de detalhes
  };

  const sortedClients = [...clientes].sort((a, b) => {
    switch (sortCriteria) {
      case "id":
        return a.id - b.id;
      case "ltv":
        return b.CLV - a.CLV;
      case "frequency":
        return b.frequency - a.frequency;
      case "monetary_value":
        return b.monetary_value - a.monetary_value;
      case "type":
        return a.type.localeCompare(b.type);
      default:
        return 0;
    }
  });

  const filteredClients = sortedClients.filter((client) => {
    // Converte todos os dados do cliente para string para a comparação
    const searchString = `${client.id} ${client.type}`.toLowerCase();
    
    const matchesSearch = searchString.includes(searchTerm.toLowerCase()); // Verifica se o termo de pesquisa está em qualquer campo

    const matchesFilter = filter ? client.type === filter : true; // Verifica o filtro de tipo de cliente, se houver

    return matchesSearch && matchesFilter; // Retorna os clientes que correspondem à pesquisa e ao filtro
  });

  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentClients = filteredClients.slice(startIndex, startIndex + itemsPerPage); // Pega os clientes da página atual

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber); // Muda a página
  };

  const totalPages = Math.ceil(filteredClients.length / itemsPerPage); // Total de páginas

  // Lógica para exibir as páginas em faixas de 5 (1-5, 6-10, etc.)
  const handleNextRange = () => {
    if (pageRangeStart + 5 < totalPages) {
      setPageRangeStart(pageRangeStart + 5); // Avança para o próximo conjunto de 5 páginas
      setCurrentPage(pageRangeStart + 6); // Avança para a primeira página da nova faixa
    }
  };

  const handlePrevRange = () => {
    if (pageRangeStart > 0) {
      setPageRangeStart(pageRangeStart - 5); // Retrocede para o conjunto anterior de 5 páginas
      setCurrentPage(pageRangeStart); // Volta para a primeira página da faixa anterior
    }
  };

  // Função para pegar os tipos de clientes únicos
  const clientTypes = [...new Set(clientes.map(client => client.type))];

  return (
    <div className={stylesCliente.container}>
      <h1 className={stylesCliente.title}>CLIENTES</h1>
      <div className={stylesCliente.searchFilterContainer}>
        <input
          type="text"
          className={stylesCliente.searchInput}
          placeholder="Busque por ID ou Tipo de Cliente"
          value={searchTerm} // Valor do input
          onChange={handleSearchChange} // Atualiza o termo de pesquisa
        />
        <div className={stylesCliente.sortContainer}>
          <select
            id="sort"
            className={stylesCliente.sortSelect}
            value={sortCriteria}
            onChange={handleSortChange} // Atualiza o critério de ordenação
          >
            <option value="" disabled>Ordenar por</option>
            <option value="id">ID do Cliente</option>
            <option value="ltv">Lifetime Value (LTV)</option>
            <option value="frequency">Número Esperado de Compras</option>
            <option value="monetary_value">Valor Esperado por Transação</option>
            <option value="type">Categoria do Cliente</option>
          </select>
        </div>
        <div className={stylesCliente.filterContainer}>
          <select
            className={stylesCliente.filterSelect}
            value={filter}
            onChange={handleFilterChange} // Atualiza o filtro
          >
            <option value="" disabled >Filtros</option>
            {clientTypes.map((type, index) => (
              <option key={index} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (<LoadingModal />) : (
        <>
          <div className={stylesCliente.cardsContainer}>
            {currentClients.map((client) => (
              <div className={stylesCliente.clientCard} key={client.id}>
                <h3 className={stylesCliente.clientId}>ID Cliente: {client.id}</h3>
                <p className={stylesCliente.clientInfo}>
                  <strong>Tipo de Cliente:</strong> {client.type}
                </p>
                <p className={stylesCliente.clientInfo}>
                  <strong>Número Esperado de Compras:</strong> {client.frequency}
                </p>
                <p className={stylesCliente.clientInfo}>
                  <strong>Valor Esperado por Transação:</strong> $
                  {client.monetary_value.toFixed(2)}
                </p>
                <p className={stylesCliente.clientInfo}>
                  <strong>LTV:</strong> {client.CLV}
                </p>
                <button
                  className={stylesCliente.detailsButton}
                  onClick={() => handleDetailsClick(client.id)}
                >
                  Detalhes
                </button>
              </div>
            ))}
          </div>

          {/* Paginação */}
          <div className={stylesCliente.pagination}>
            {/* Botão para voltar para o conjunto anterior de páginas */}
            <button
              className={`${stylesCliente.pageButton} ${
                pageRangeStart === 0 ? stylesCliente.disabled : ""
              }`}
              onClick={handlePrevRange}
              disabled={pageRangeStart === 0}
            >
              &lt;&lt;
            </button>

            <button
              className={`${stylesCliente.pageButton} ${
                currentPage === 1 ? stylesCliente.disabled : ""
              }`}
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
            >
              &lt;
            </button>

            {/* Botões das páginas, exibindo somente 5 por vez */}
            {[...Array(5)].map((_, index) => {
              const pageNumber = pageRangeStart + index + 1;
              if (pageNumber <= totalPages) {
                return (
                  <button
                    key={pageNumber}
                    className={`${stylesCliente.pageButton} ${
                      currentPage === pageNumber ? stylesCliente.active : ""
                    }`}
                    onClick={() => handlePageChange(pageNumber)}
                  >
                    {pageNumber}
                  </button>
                );
              }
              return null; // Não renderiza botões para páginas além do total
            })}

            <button
              className={`${stylesCliente.pageButton} ${
                currentPage === totalPages ? stylesCliente.disabled : ""
              }`}
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
            >
              &gt;
            </button>

            {/* Botão para avançar para o próximo conjunto de páginas */}
            <button
              className={`${stylesCliente.pageButton} ${
                pageRangeStart + 5 >= totalPages ? stylesCliente.disabled : ""
              }`}
              onClick={handleNextRange}
              disabled={pageRangeStart + 5 >= totalPages}
            >
              &gt;&gt;
            </button>
          </div>
        </>
      )}

      {/* Modal de erro */}
      {error && <ErrorModal message={error} onClose={() => setError(null)} />}
    </div>
  );
};

export default isConfigurateModel(Clientes);