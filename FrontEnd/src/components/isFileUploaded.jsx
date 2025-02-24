import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function isFileUploaded(Component) {
  return function IsFileUploaded(props) {
    const navigate = useNavigate();

    useEffect(() => {
      const fileUploaded = localStorage.getItem('fileUploaded'); // Verifica se o arquivo foi enviado

      if (!fileUploaded) {
        
        navigate('/'); // Se o arquivo não foi enviado, redireciona para a página inicial
        return;
      }
    }, [navigate]);

    return <Component {...props} />;
  };
}
