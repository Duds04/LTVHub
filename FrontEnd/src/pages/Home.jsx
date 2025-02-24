import React, { useState, useEffect } from "react";
import stylesHome from "../style/Home.module.css";
import { FaPaperPlane } from 'react-icons/fa'; // Ícone do avião de papel
import { useNavigate } from 'react-router-dom'; // Usando o useNavigate para navegação

const Home = () => {
  const [fileName, setFileName] = useState("");
  const [file, setFile] = useState(null); // Estado para armazenar o arquivo
  const [isUploaded, setIsUploaded] = useState(false); // Estado para o toggle do envio
  const navigate = useNavigate(); // Hook para navegação

  // Função para lidar com a mudança no input de arquivo
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFileName(selectedFile.name); // Atualiza o nome do arquivo
      setFile(selectedFile); // Armazena o arquivo
      setIsUploaded(false);   // Resetando o estado para "não enviado"
      localStorage.removeItem('fileUploaded');
    } else {
      setFileName(""); // Se nenhum arquivo for selecionado, o nome é limpo
      setFile(null); // Limpa o arquivo
    }
  };

  // Função para simular o envio do arquivo e redirecionar para o modelo
  const handleFileUpload = async () => {
    if (file) {  // Verifica se o arquivo foi selecionado
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('/upload', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          setIsUploaded(true); // Altera o estado para "enviado"
          
          // Armazenando a chave "fileUploaded" no localStorage para indicar que o arquivo foi enviado
          localStorage.setItem('fileUploaded', 'true');

          // Após o upload do arquivo, redireciona para a página do modelo
          navigate("/modelo");  // Aqui, "/modelo" é o caminho da página de configuração do modelo
        } else {
          console.error('Erro ao enviar o arquivo');
        }
      } catch (error) {
        console.error('Erro ao enviar o arquivo', error);
      }
    }
  };

  // Resetar o localStorage quando a rota for "/"
  useEffect(() => {
    if (window.location.pathname === "/") {
      localStorage.removeItem('fileUploaded'); // Remove a chave do localStorage ao voltar para a página inicial
    }
  }, [window.location.pathname]);

  return (
    <div className={stylesHome.homeContainer}>
      <div className={stylesHome.section}>
        <h1 className={stylesHome.title}>LTV HUB</h1>
        <p className={stylesHome.description}>
          Bem-vindo ao LTV HUB, sua solução completa para calcular o Lifetime Value (LTV) de forma prática e eficiente. 
          Configure modelos preditivos e descubra insights financeiros detalhados para impulsionar suas estratégias de negócio.
        </p>
        <p className={stylesHome.description}>
          O cálculo do Lifetime Value pode ser realizado utilizando diferentes modelos estatísticos e preditivos. 
          Aqui estão os modelos disponíveis:
        </p>
        <h2 className={stylesHome.subTitle}>Modelos de Predição de Frequência:</h2>
        <p className={stylesHome.description}>
          <ul>
            <li><strong>BG/NBD:</strong> Modelo baseado no comportamento de compra dos clientes.</li>
            <li><strong>Pareto:</strong> Modelo para estimar a probabilidade de recompra.</li>
            <li><strong>Machine Learning:</strong> Abordagem personalizada usando algoritmos de aprendizado de máquina.</li>
          </ul>
        </p>
        <h2 className={stylesHome.subTitle}>Modelos de Predição Monetária:</h2>
        <p className={stylesHome.description}>
          <ul>
            <li><strong>Gamma-Gamma:</strong> Modelo estatístico para prever o valor médio das transações.</li>
            <li><strong>Machine Learning:</strong> Abordagem avançada para prever valores monetários.</li>
          </ul>
        </p>
        <p className={stylesHome.description}>
          Escolha o modelo que melhor atende às suas necessidades para configurar e gerar previsões detalhadas.
        </p>
      </div>
      <div className={stylesHome.section}>
        <h1 className={stylesHome.title}>UPLOAD</h1>
        <p className={stylesHome.description}>
          Faça o upload do seu arquivo <strong>CSV</strong> contendo as informações de usuários e transações. 
          Este arquivo deve incluir, obrigatoriamente, as seguintes colunas:
        </p>
        <p className={stylesHome.description}>
          <ul>
            <li><strong>Coluna de ID Usuário:</strong> Identificação única dos usuários.</li>
            <li><strong>Coluna de Data das Transações:</strong> Datas em que as transações foram realizadas.</li>
            <li><strong>Coluna de Valor das Transações:</strong> Valores das transações realizadas pelos usuários.</li>
          </ul>
        </p>
        <p className={stylesHome.description}>
          Escolha um arquivo e clique em "Enviar Arquivo" para continuar.
        </p>
        
        {/* Container para o input e botão */}
        <div className={stylesHome.uploadContainer}>
          <div className={stylesHome.uploadWrapper}>
            {/* Label e Input de Arquivo */}
            <label htmlFor="upload-file" className={stylesHome.uploadLabel}>
              {fileName ? fileName : "Selecione o arquivo"}
            </label>
            <input 
              type="file" 
              id="upload-file" 
              className={stylesHome.uploadInput} 
              onChange={handleFileChange}  // Chama a função quando um arquivo é selecionado
            />

            {/* Botão de envio com ícone de avião de papel */}
            <button 
              className={`${stylesHome.uploadButton} ${isUploaded ? stylesHome.uploadButtonToggled : ''}`} 
              onClick={handleFileUpload} // Simula o envio do arquivo
              disabled={!fileName || isUploaded} // Desabilita o botão se não houver arquivo ou se o arquivo já foi enviado
            >
              <FaPaperPlane className={stylesHome.uploadButtonIcon} />
              <span className={stylesHome.uploadButtonText}>
                {isUploaded ? 'Enviado' : 'Enviar Arquivo'}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
