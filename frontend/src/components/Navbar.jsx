export default function Navbar({ onLoginClick }) {
  return (
    <nav className="navbar">
      <div className="nav-left">
        <div className="logo" aria-hidden="true">DG</div>
        <span className="site-name">DeepGuard</span>
      </div>

      <ul className="nav-right">
        <li><a href="#home">Home</a></li>

        <li className="dropdown">
          <a href="#tools">Tools</a>
          <ul className="dropdown-menu">
            <li><a href="#tools">Video Detection</a></li>
          </ul>
        </li>

        <li><a href="#about">About</a></li>
        <li><a href="#contact">Contact</a></li>

        <li>
          <button className="nav-login-btn" onClick={onLoginClick}>
            Login
          </button>
        </li>
      </ul>
    </nav>
  );
}
