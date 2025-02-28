import React from 'react';
import styles from '../style/ErrorModal.module.css';

const ErrorModal = ({ message, onClose }) => {
  if (!message) return null;

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <h2 className={styles.title}> <span>🚨</span> Erro</h2>
        <p className={styles.message} dangerouslySetInnerHTML={{ __html: message }} />
        <button className={styles.closeButton} onClick={onClose}>Fechar</button>
      </div>
    </div>
  );
};

export default ErrorModal;
