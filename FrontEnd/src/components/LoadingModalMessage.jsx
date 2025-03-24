import React from "react";
import styles from "../style/LoadingModalMessage.module.css";

const LoadingModalMessage = ({ message }) => {
  return (
    <div className={styles.loadingModal}>
      <div className={styles.loadingSpinner}></div>
      <p className={styles.loadingText}>Carregando...</p>
      <p className={styles.dynamicMessage}>{message}</p>
    </div>
  );
};

export default LoadingModalMessage;