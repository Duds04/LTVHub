import React, { createContext, useState, useContext } from "react";

// Criando o contexto para verificar o estado de upload
const FileContext = createContext();

export const useFileContext = () => useContext(FileContext);

export const FileProvider = ({ children }) => {
  const [isFileUploaded, setIsFileUploaded] = useState(false); // Estado para saber se o arquivo foi enviado

  return (
    <FileContext.Provider value={{ isFileUploaded, setIsFileUploaded }}>
      {children}
    </FileContext.Provider>
  );
};
