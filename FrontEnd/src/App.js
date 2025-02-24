import React from "react";
import { Route, Routes } from "react-router-dom";
import styles from "./style/App.css"; // Estilo geral da aplicação como módulo CSS

import Sidebar from "./components/Sidebar";
import Home from "./pages/Home";
import FormModel from "./pages/FormModel";
import Estatisticas from "./pages/Estatisticas"
import Clientes from "./pages/Clientes"
import DetalheCliente from "./pages/DetalheCliente";

import { FileProvider } from "./context/FileContext"; // Importando o FileProvider


const App = () => {
  return (
    <div className={styles.appContainer}>
      <div className={styles.sidebar}>
        <Sidebar />
      </div>
      <div className={styles.content}>
        <FileProvider>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/modelo" element={<FormModel />} />
            <Route path="/estatisticas" element={<Estatisticas />} />
            <Route path="/clientes" element={<Clientes />} />
            <Route path="/cliente/:id" element={<DetalheCliente />} />
          </Routes>
        </FileProvider>
      </div>
    </div>
  );
};

export default App;
