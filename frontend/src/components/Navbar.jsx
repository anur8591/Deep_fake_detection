import { Shield } from "lucide-react";

function Navbar() {
  return (
    <nav className="navbar">

      <a
        href="#dashboard"
        className="navbar-brand"
      >

        <div className="brand-icon">
          <Shield size={23} />
        </div>

        <div>
          <strong>DeepGuard</strong>
          <span>Deepfake Detection</span>
        </div>

      </a>


      <div className="navbar-links">

        <a href="#dashboard">
          Dashboard
        </a>

        <a href="#how-it-works">
          How It Works
        </a>

        <a href="#about">
          About
        </a>

      </div>


      <a
        href="#"
        className="github-button"
      >
        GitHub
      </a>

    </nav>
  );
}

export default Navbar;