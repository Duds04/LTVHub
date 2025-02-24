import React, { useState, useEffect } from "react";
import styles from "../style/FormModel.module.css"; // Importando o CSS
import isFileUploaded from "../components/isFileUploaded"; // Importando o HOC
import { useNavigate } from "react-router-dom"; // Usando o useNavigate para navegação

const FormModel = () => {
  const navigate = useNavigate(); // Hook para navegação

  // Estados para armazenar as seleções dos campos
  const [idColumn, setIdColumn] = useState("");
  const [transactionDateColumn, setTransactionDateColumn] = useState("");
  const [transactionValueColumn, setTransactionValueColumn] = useState("");
  const [frequencyModel, setFrequencyModel] = useState("");
  const [monetaryModel, setMonetaryModel] = useState("");
  const [weeksAhead, setWeeksAhead] = useState(1); // Valor padrão de 1
  const [columns, setColumns] = useState([]); // Estado para armazenar as colunas do CSV

  // Função para validar e enviar o formulário
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Verifica se todos os campos obrigatórios foram preenchidos
    if (
      !idColumn ||
      !transactionDateColumn ||
      !transactionValueColumn ||
      !frequencyModel ||
      !monetaryModel ||
      !weeksAhead
    ) {
      alert("Todos os campos obrigatórios devem ser preenchidos."); // Alerta se algum campo obrigatório estiver vazio
    } else {
      // Coletar os dados do formulário
      const formData = {
        idColumn,
        transactionDateColumn,
        transactionValueColumn,
        frequencyModel,
        monetaryModel,
        weeksAhead,
      };

      // Enviar os dados para o backend
      try {
        const response = await fetch('/submit_form', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        });

        const data = await response.json();
        if (response.ok) {
          console.log("Formulário enviado com sucesso:", data);
          localStorage.setItem("configurateModel", "true");
          navigate("/clientes");
        } else {
          console.error("Erro ao enviar formulário:", data);
        }
      } catch (error) {
        console.error("Erro ao enviar formulário:", error);
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
        }
      } catch (error) {
        console.error("Erro ao buscar colunas:", error);
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
          <label htmlFor="transactionDateColumn" className={styles.inputLabel}>
            Selecione a coluna de <b>Data das Transações</b> do usuário
          </label>
          <select
            id="transactionDateColumn"
            value={transactionDateColumn}
            onChange={(e) => setTransactionDateColumn(e.target.value)}
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
          <label htmlFor="transactionValueColumn" className={styles.inputLabel}>
            Selecione a coluna de <b>Valor das Transações</b> do usuário
          </label>
          <select
            id="transactionValueColumn"
            value={transactionValueColumn}
            onChange={(e) => setTransactionValueColumn(e.target.value)}
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
              value="BG/NBD"
              onChange={(e) => setFrequencyModel(e.target.value)}
              required
            />
            <label htmlFor="bgNBD">BG/NBD</label>

            <input
              type="radio"
              id="pareto"
              name="frequencyModel"
              value="Pareto"
              onChange={(e) => setFrequencyModel(e.target.value)}
              required
            />
            <label htmlFor="pareto">Pareto</label>

            <input
              type="radio"
              id="ml"
              name="frequencyModel"
              data-value="Machine Learning"
              onChange={(e) => setFrequencyModel(e.target.dataset.value)}
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
              value="Gamma-Gamma"
              onChange={(e) => setMonetaryModel(e.target.value)}
              required
            />
            <label htmlFor="gammaGamma">Gamma-Gamma</label>

            <input
              type="radio"
              id="mlMonetary"
              name="monetaryModel"
              data-value="Machine Learning"
              onChange={(e) => setMonetaryModel(e.target.dataset.value)}
              required
            />
            <label htmlFor="mlMonetary">Machine Learning</label>
          </div>
        </div>

        {/* Semanas a frente para cálculo */}
        <div className={styles.inputGroup}>
          <label htmlFor="weeksAhead" className={styles.inputLabel}>
            Selecione quantas semanas a frente você deseja calcular
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
    </div>
  );
};

export default isFileUploaded(FormModel); // Envolvendo o componente com o HOC para protegê-lo