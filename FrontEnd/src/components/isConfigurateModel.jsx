import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function isConfigurateModel(Component) {
  return function IsFileUploaded(props) {
    const navigate = useNavigate();

    useEffect(() => {
      const configurateModel = localStorage.getItem('configurateModel'); 

      if (!configurateModel) {
        
        navigate('/modelo'); 
        return;
      }
    }, [navigate]);

    return <Component {...props} />;
  };
}
