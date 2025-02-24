import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function isConfigurateModel(Component) {
  return function IsFileUploaded(props) {
    const navigate = useNavigate();

    useEffect(() => {
      const configurateModel = localStorage.getItem('configurateModel'); // Verifica se o arquivo foi enviado

      if (!configurateModel) {
        
        navigate('/modelo'); // Se o arquivo não foi enviado, redireciona para a página inicial
        return;
      }
    }, [navigate]);

    return <Component {...props} />;
  };
}
