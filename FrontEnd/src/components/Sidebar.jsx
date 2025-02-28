import React from 'react';
import { Link } from 'react-router-dom';
import { FaHome, FaCog, FaUsers, FaChartBar, FaGithub, FaLinkedin, FaEnvelope, FaGlobe } from 'react-icons/fa';
import stylesSidebar from '../style/Sidebar.module.css';  

const Sidebar = () => {
  return (
    <div className={stylesSidebar.sidebar}>
      {/* Logo no topo */}
      <div className={stylesSidebar.logoContainer}>
        {/* <img src="/static/react/assets/logo.svg" alt="Logo" className={stylesSidebar.logo} /> */}
        <img src="./assets/logo.svg" alt="Logo" className={stylesSidebar.logo} />

      </div>

      {/* Menu de navegação */}
      <nav className={stylesSidebar.navMenu}>
        <ul>
          <li>
            <Link to="/" className={stylesSidebar.navItem}>
              <FaHome className={stylesSidebar.icon} /> Tela Inicial
            </Link>
          </li>
          <li>
            <Link to="/modelo" className={stylesSidebar.navItem}>
              <FaCog className={stylesSidebar.icon} /> Modelo
            </Link>
          </li>
          <li>
            <Link to="/clientes" className={stylesSidebar.navItem}>
              <FaUsers className={stylesSidebar.icon} /> Clientes
            </Link>
          </li>
          <li>
            <Link to="/estatisticas" className={stylesSidebar.navItem}>
              <FaChartBar className={stylesSidebar.icon} /> Estatísticas
            </Link>
          </li>
        </ul>
      </nav>

      {/* Rodapé com Redes Sociais */}
      <div className={stylesSidebar.footer}>
        <div className={stylesSidebar.socialLinks}>
          <ul className={stylesSidebar.socialList}>
            <li>
              <a href="https://github.com/Duds04/ltvhub-front" target="_blank" rel="noopener noreferrer">
                <FaGithub className={stylesSidebar.icon} />
              </a>
            </li>
            <li>
              <a href="https://www.linkedin.com/search/results/all/?keywords=nesped&origin=GLOBAL_SEARCH_HEADER&sid=v.N" target="_blank" rel="noopener noreferrer">
                <FaLinkedin className={stylesSidebar.icon} />
              </a>
            </li>
            <li>
              <a href="mailto:nesped.ufv@gmail.com">
                <FaEnvelope className={stylesSidebar.icon} />
              </a>
            </li>
            <li>
              <a href="https://nesped.caf.ufv.br/" target="_blank" rel="noopener noreferrer">
                <FaGlobe className={stylesSidebar.icon} />
              </a>
            </li>
          </ul>
        </div>
        <div className={stylesSidebar.copyright}>
          © NesPeD Lab
        </div>
      </div>
    </div>
  );
};

export default Sidebar;