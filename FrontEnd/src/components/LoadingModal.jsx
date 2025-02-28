import React from "react";
import styles from "../style/LoadingModal.module.css";

const LoadingModal = () => {
  return (
    <div className={styles.loadingModal}>
      <div className={styles.loadingSpinner}></div>
      <p className={styles.loadingText}>Carregando...</p>
    </div>
  );
};

export default LoadingModal;
