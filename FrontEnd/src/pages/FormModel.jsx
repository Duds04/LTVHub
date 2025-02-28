import React, { useState, useEffect } from "react";
import styles from "../style/FormModel.module.css"; // Importando o CSS
import isFileUploaded from "../components/isFileUploaded"; // Importando o HOC
import { useNavigate } from "react-router-dom"; // Usando o useNavigate para navegação

import LoadingModal from "../components/LoadingModal"; // Importando o componente de carregamento
import ErrorModal from "../components/ErrorModal"; // Importando o ErrorModal

const FormModel = () => {
  const navigate = useNavigate(); // Hook para navegação

  // Estados para armazenar as seleções dos campos
  const [idColumn, setIdColumn] = useState("");
  const [dateColumn, setDateColumn] = useState("");
  const [amountColumn, setAmountColumn] = useState("");
  const [frequencyModel, setFrequencyModel] = useState("");
  const [monetaryModel, setMonetaryModel] = useState("");
  const [weeksAhead, setWeeksAhead] = useState(180); // Valor padrão de 180
  const [columns, setColumns] = useState([]); // Estado para armazenar as colunas do CSV
  const [loading, setLoading] = useState(false); // Estado para controlar o modal de carregamento
  const [error, setError] = useState(null); // Estado para controlar a mensagem de erro

  // Função para validar e enviar o formulário
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Verifica se todos os campos obrigatórios foram preenchidos
    if (
      !idColumn ||
      !dateColumn ||
      !amountColumn ||
      !frequencyModel ||
      !monetaryModel ||
      !weeksAhead
    ) {
      alert("Todos os campos obrigatórios devem ser preenchidos.");
    } else {
      // Coletar os dados do formulário
      const formData = {
        idColumn,
        dateColumn,
        amountColumn,
        frequencyModel,
        monetaryModel,
        weeksAhead,
      };

      // Mostrar o modal de carregamento
      setLoading(true);

      // Enviar os dados para o backend
      try {
        const response = await fetch("/submit_form", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        });

        const data = await response.json();
        if (response.ok) {
          console.log("Formulário enviado com sucesso:", data);
          localStorage.setItem("configurateModel", "true");
          navigate("/clientes");
        } else {
          console.error(data.error);
          setError(
            `Não foi possível enviar o formulário. <br />Por favor, revise os parâmetros selecionados e tente novamente.`
          );
        }
      } catch (error) {
        console.error("Erro ao processar o formulário:", error);
        setError(
          "Erro ao processar o formulário.<br />Tente novamente da Tela Inicial."
        );
      } finally {
        setLoading(false);
      }
    }
  };

  // Resetar o localStorage quando a rota for "/"
  useEffect(() => {
    if (window.location.pathname === "/modelo") {
      localStorage.removeItem("configurateModel");
    }
  }, [window.location.pathname]);

  // Função para buscar as colunas do CSV
  useEffect(() => {
    const fetchColumns = async () => {
      try {
        const response = await fetch("/columns");
        const data = await response.json();
        if (response.ok) {
          setColumns(data.columns);
        } else {
          console.error("Erro ao buscar colunas:", data.error);
          setError(
            data.error ||
              "Erro ao buscar colunas.<br />Tente novamente da Tela Inicial."
          );
        }
      } catch (error) {
        console.error("Erro ao buscar colunas:", error);
        setError(
          "Erro ao buscar colunas.<br />Tente novamente da Tela Inicial."
        );
      }
    };

    fetchColumns();
  }, []);

  return (
    <div className={styles.formContainer}>
      <h1 className={styles.title}>CONFIGURAÇÃO DO MODELO</h1>
      <form onSubmit={handleSubmit} className={styles.form}>
        {/* Coluna ID Usuário */}
        <div className={styles.inputGroup}>
          <label htmlFor="idColumn" className={styles.inputLabel}>
            Selecione a coluna de <b>ID</b> usuário
          </label>
          <select
            id="idColumn"
            value={idColumn}
            onChange={(e) => setIdColumn(e.target.value)}
            className={styles.input}
            required
          >
            <option value="" disabled>
              Coluna...
            </option>
            {columns.map((column) => (
              <option key={column} value={column}>
                {column}
              </option>
            ))}
          </select>
        </div>

        {/* Coluna Data das Transações */}
        <div className={styles.inputGroup}>
          <label htmlFor="dateColumn" className={styles.inputLabel}>
            Selecione a coluna de <b>Data das Transações</b> do usuário
          </label>
          <select
            id="dateColumn"
            value={dateColumn}
            onChange={(e) => setDateColumn(e.target.value)}
            className={styles.input}
            required
          >
            <option value="" disabled>
              Coluna...
            </option>
            {columns.map((column) => (
              <option key={column} value={column}>
                {column}
              </option>
            ))}
          </select>
        </div>

        {/* Coluna Valor das Transações */}
        <div className={styles.inputGroup}>
          <label htmlFor="amountColumn" className={styles.inputLabel}>
            Selecione a coluna de <b>Valor das Transações</b> do usuário
          </label>
          <select
            id="amountColumn"
            value={amountColumn}
            onChange={(e) => setAmountColumn(e.target.value)}
            className={styles.input}
            required
          >
            <option value="" disabled>
              Coluna...
            </option>
            {columns.map((column) => (
              <option key={column} value={column}>
                {column}
              </option>
            ))}
          </select>
        </div>

        {/* Modelo de Predição de Frequência */}
        <div className={styles.inputGroup}>
          <label className={styles.inputLabel}>
            Selecione o Modelo de Predição de Frequência
          </label>
          <div className={styles.radioGroup}>
            <input
              type="radio"
              id="bgNBD"
              name="frequencyModel"
              value="BGFModel"
              onChange={(e) => setFrequencyModel(e.target.value)}
              required
            />
            <label htmlFor="bgNBD">BG/NBD</label>

            <input
              type="radio"
              id="pareto"
              name="frequencyModel"
              value="ParetoModel"
              onChange={(e) => setFrequencyModel(e.target.value)}
              required
            />
            <label htmlFor="pareto">Pareto</label>

            <input
              type="radio"
              id="ml"
              name="frequencyModel"
              value="MachineLearning"
              onChange={(e) => setFrequencyModel(e.target.value)}
              required
            />
            <label htmlFor="ml">Machine Learning</label>
          </div>
        </div>

        {/* Modelo de Predição Monetária */}
        <div className={styles.inputGroup}>
          <label className={styles.inputLabel}>
            Selecione o Modelo de Predição Monetária
          </label>
          <div className={styles.radioGroup}>
            <input
              type="radio"
              id="gammaGamma"
              name="monetaryModel"
              value="GammaGammaModel"
              onChange={(e) => setMonetaryModel(e.target.value)}
              required
            />
            <label htmlFor="gammaGamma">Gamma-Gamma</label>

            <input
              type="radio"
              id="mlMonetary"
              name="monetaryModel"
              value="MachineLearning"
              onChange={(e) => setMonetaryModel(e.target.value)}
              required
            />
            <label htmlFor="mlMonetary">Machine Learning</label>
          </div>
        </div>

        {/* Semanas a frente para cálculo (Numero de Periodos)*/}
        <div className={styles.inputGroup}>
          <label htmlFor="weeksAhead" className={styles.inputLabel}>
            Selecione quantos periodos (em semanas) a frente você deseja
            calcular
          </label>
          <input
            type="number"
            id="weeksAhead"
            value={weeksAhead}
            onChange={(e) => setWeeksAhead(e.target.value)}
            className={styles.input}
            required
            min="1"
            inputMode="numeric"
          />
        </div>

        {/* Botão de envio */}
        <button type="submit" className={styles.submitButton}>
          ENVIAR
        </button>
      </form>

      {/* Renderizar o modal de carregamento */}
      {loading && <LoadingModal />}

      {/* Renderizar o ErrorModal */}
      <ErrorModal message={error} onClose={() => setError(null)} />
    </div>
  );
};

export default isFileUploaded(FormModel); // Envolvendo o componente com o HOC para protegê-lo
