import React, { useState, useEffect } from "react";
import styles from "../style/FormModel.module.css";
import isFileUploaded from "../components/isFileUploaded";
import { useNavigate } from "react-router-dom";
import LoadingModal from "../components/LoadingModal";
import ErrorModal from "../components/ErrorModal";
import Select from "react-select";

const FormModel = () => {
  const navigate = useNavigate();

  // Estados do formulário
  const [idColumn, setIdColumn] = useState("");
  const [dateColumn, setDateColumn] = useState("");
  const [amountColumn, setAmountColumn] = useState("");
  const [frequencyModel, setFrequencyModel] = useState("");
  const [monetaryModel, setMonetaryModel] = useState("");
  const [weeksAhead, setWeeksAhead] = useState(180);
  const [columns, setColumns] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!idColumn || !dateColumn || !amountColumn || !frequencyModel || !monetaryModel || !weeksAhead) {
      alert("Todos os campos obrigatórios devem ser preenchidos.");
    } else {
      const formData = {
        idColumn,
        dateColumn,
        amountColumn,
        frequencyModel,
        monetaryModel,
        weeksAhead,
      };

      setLoading(true);

      try {
        const response = await fetch("/submit_form", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData),
        });

        const data = await response.json();
        if (response.ok) {
          console.log("Formulário enviado com sucesso:", data);
          localStorage.setItem("configurateModel", "true");
          navigate("/clientes");
        } else {
          console.error(data.error);
          setError("Não foi possível enviar o formulário. <br />Revise os parâmetros selecionados e tente novamente.");
        }
      } catch (error) {
        console.error("Erro ao processar o formulário:", error);
        setError("Erro ao processar o formulário.<br />Tente novamente da Tela Inicial.");
      } finally {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    if (window.location.pathname === "/modelo") {
      localStorage.removeItem("configurateModel");
    }
  }, [window.location.pathname]);

  useEffect(() => {
    const fetchColumns = async () => {
      try {
        const response = await fetch("/columns");
        const data = await response.json();
        if (response.ok) {
          setColumns(data.columns.map((col) => ({ label: col, value: col })));
        } else {
          console.error("Erro ao buscar colunas:", data.error);
          setError("Erro ao buscar colunas.<br />Tente novamente da Tela Inicial.");
        }
      } catch (error) {
        console.error("Erro ao buscar colunas:", error);
        setError("Erro ao buscar colunas.<br />Tente novamente da Tela Inicial.");
      }
    };

    fetchColumns();
  }, []);

  const customStyles = {
    control: (styles) => ({
      ...styles,
      width: "100%",
      padding: "5px 2px",
      marginTop: "10px",
      border: "2px #ccc",
      borderRadius: "4px",
      fontSize: "2vmin",
      fontWeight: "100",
      boxSizing: "border-box",
      boxShadow: "4px 3px 10px #ccc",
      backgroundColor: "#E9E9ED",
      color: "black",
      marginBottom: "0px",
    }),
    menu: (styles) => ({
      ...styles,
      marginTop: "0px",
    }),
    option: (styles, state) => ({
      ...styles,
      fontSize: "2vmin",
      fontWeight: "100",
      color: "black",
      marginTop: "0px",
      padding: "2px 10px",
      backgroundColor: state.isSelected ? "#E9E9ED" : state.isFocused ? "#E9E9ED" : null,
      ":hover": { backgroundColor: "#E9E9ED" },
    }),
  };

  return (
    <div className={styles.formContainer}>
      <h1 className={styles.title}>CONFIGURAÇÃO DO MODELO</h1>
      <form onSubmit={handleSubmit} className={styles.form}>
        {/* Coluna ID Usuário */}
        <div className={styles.inputGroup}>
          <label htmlFor="idColumn" className={styles.inputLabel}>
            Selecione a coluna de <b>ID</b> usuário
          </label>
          <Select
            id="idColumn"
            value={idColumn ? { label: idColumn, value: idColumn } : null}
            onChange={(selectedOption) => setIdColumn(selectedOption.value)}
            options={columns}
            styles={customStyles} // Aplica os estilos personalizados
            required
            placeholder="Coluna..."
          />
        </div>

        {/* Coluna Data das Transações */}
        <div className={styles.inputGroup}>
          <label htmlFor="dateColumn" className={styles.inputLabel}>
            Selecione a coluna de <b>Data das Transações</b> do usuário
          </label>
          <Select
            id="dateColumn"
            value={dateColumn ? { label: dateColumn, value: dateColumn } : null}
            onChange={(selectedOption) => setDateColumn(selectedOption.value)}
            options={columns}
            styles={customStyles} // Aplica os estilos personalizados
            required
            placeholder="Coluna..."
          />
        </div>

        {/* Coluna Valor das Transações */}
        <div className={styles.inputGroup}>
          <label htmlFor="amountColumn" className={styles.inputLabel}>
            Selecione a coluna de <b>Valor das Transações</b> do usuário
          </label>
          <Select
            id="amountColumn"
            value={amountColumn ? { label: amountColumn, value: amountColumn } : null}
            onChange={(selectedOption) => setAmountColumn(selectedOption.value)}
            options={columns}
            styles={customStyles} // Aplica os estilos personalizados
            required
            placeholder="Coluna..."
          />
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

export default isFileUploaded(FormModel);
