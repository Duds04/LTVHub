import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import stylesCliente from "../style/Clientes.module.css";
import isConfigurateModel from "../components/isConfigurateModel"; // Importando o HOC


const Clientes = () => {
  const [searchTerm, setSearchTerm] = useState(""); // Termo de pesquisa
  const [filter, setFilter] = useState(""); // Filtro de tipo de cliente
  const [clientes, setClientes] = useState([
    {
      id: 1,
      tipo: "Cliente A",
      numCompras: 5,
      LTV: 1200,
      valorPorTransacao: 240,
    },
    {
      id: 2,
      tipo: "Cliente B",
      numCompras: 3,
      LTV: 800,
      valorPorTransacao: 266.67,
    },
    {
      id: 3,
      tipo: "Cliente A",
      numCompras: 8,
      LTV: 1500,
      valorPorTransacao: 187.5,
    },
    {
      id: 4,
      tipo: "Cliente C",
      numCompras: 1,
      LTV: 300,
      valorPorTransacao: 300,
    },
    {
      id: 5,
      tipo: "Cliente B",
      numCompras: 4,
      LTV: 700,
      valorPorTransacao: 175,
    },
    {
      id: 6,
      tipo: "Cliente A",
      numCompras: 10,
      LTV: 2000,
      valorPorTransacao: 200,
    },
    {
      id: 7,
      tipo: "Cliente D",
      numCompras: 2,
      LTV: 500,
      valorPorTransacao: 250,
    },
    {
      id: 8,
      tipo: "Cliente C",
      numCompras: 7,
      LTV: 1400,
      valorPorTransacao: 200,
    },
    {
      id: 9,
      tipo: "Cliente B",
      numCompras: 6,
      LTV: 1100,
      valorPorTransacao: 183.33,
    },
    {
      id: 10,
      tipo: "Cliente A",
      numCompras: 12,
      LTV: 2500,
      valorPorTransacao: 208.33,
    },
  ]);
  const [currentPage, setCurrentPage] = useState(1); // Página atual
  const itemsPerPage = 6; // Itens por página

  const navigate = useNavigate();

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value); // Atualiza o estado de pesquisa
  };

  const handleFilterChange = (event) => {
    setFilter(event.target.value); // Atualiza o filtro de tipo de cliente
  };

  const handleDetailsClick = (id) => {
    navigate(`/cliente/${id}`); // Navega para a página de detalhes
  };

  const filteredClients = clientes.filter((client) => {
    // Converte todos os dados do cliente para string para a comparação
    const searchString = `${client.id} ${client.tipo} ${client.numCompras} ${client.LTV} ${client.valorPorTransacao}`.toLowerCase();
    
    const matchesSearch = searchString.includes(searchTerm.toLowerCase()); // Verifica se o termo de pesquisa está em qualquer campo

    const matchesFilter = filter ? client.tipo === filter : true; // Verifica o filtro de tipo de cliente, se houver

    return matchesSearch && matchesFilter; // Retorna os clientes que correspondem à pesquisa e ao filtro
  });

  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentClients = filteredClients.slice(startIndex, startIndex + itemsPerPage); // Pega os clientes da página atual

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber); // Muda a página
  };

  const totalPages = Math.ceil(filteredClients.length / itemsPerPage); // Total de páginas

  return (
    <div className={stylesCliente.container}>
      <h1 className={stylesCliente.title}>CLIENTES</h1>
      <div className={stylesCliente.searchFilterContainer}>
        <input
          type="text"
          className={stylesCliente.searchInput}
          placeholder="Buscar Cliente"
          value={searchTerm} // Valor do input
          onChange={handleSearchChange} // Atualiza o termo de pesquisa
        />
        <div className={stylesCliente.filterContainer}>
          <select
            className={stylesCliente.filterSelect}
            value={filter}
            onChange={handleFilterChange} // Atualiza o filtro
          >
            <option value="">Filtros</option>
            <option value="Cliente A">Cliente A</option>
            <option value="Cliente B">Cliente B</option>
            <option value="Cliente C">Cliente C</option>
            <option value="Cliente D">Cliente D</option>
          </select>
        </div>
      </div>

      <div className={stylesCliente.cardsContainer}>
        {currentClients.map((client) => (
          <div className={stylesCliente.clientCard} key={client.id}>
            <h3 className={stylesCliente.clientId}>ID Cliente: {client.id}</h3>
            <p className={stylesCliente.clientInfo}>
              <strong>Tipo de Cliente:</strong> {client.tipo}
            </p>
            <p className={stylesCliente.clientInfo}>
              <strong>Número Esperado de Compras:</strong> {client.numCompras}
            </p>
            <p className={stylesCliente.clientInfo}>
              <strong>Valor Esperado por Transação:</strong> $
              {client.valorPorTransacao.toFixed(2)}
            </p>
            <p className={stylesCliente.clientInfo}>
              <strong>LTV:</strong> {client.LTV}
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
        <button
          className={`${stylesCliente.pageButton} ${
            currentPage === 1 ? stylesCliente.disabled : ""
          }`}
          onClick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage === 1}
        >
          &lt;
        </button>
        {[...Array(totalPages)].map((_, index) => (
          <button
            key={index}
            className={`${stylesCliente.pageButton} ${
              currentPage === index + 1 ? stylesCliente.active : ""
            }`}
            onClick={() => handlePageChange(index + 1)}
          >
            {index + 1}
          </button>
        ))}
        <button
          className={`${stylesCliente.pageButton} ${
            currentPage === totalPages ? stylesCliente.disabled : ""
          }`}
          onClick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          &gt;
        </button>
      </div>
    </div>
  );
};

export default isConfigurateModel(Clientes);
