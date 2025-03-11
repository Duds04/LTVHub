import React, { useState } from "react";
import styles from "../style/InfoTooltip.module.css";

const InfoTooltip = ({ text }) => {
  const [visible, setVisible] = useState(false);

  return (
    <div
      className={styles.tooltipContainer}
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      <span className={styles.infoIcon}>ⓘ</span>
      {visible && <div className={styles.tooltip}>{text}</div>}
    </div>
  );
};

export default InfoTooltip;
