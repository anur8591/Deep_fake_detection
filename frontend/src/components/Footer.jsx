import useScrollReveal from '../hooks/useScrollReveal';

export default function Footer() {
  const containerRef = useScrollReveal('.footer-container > div', {
    threshold: 0.2,
    revealClass: 'show',
    once: false,
  });

  return (
    <footer className="footer" id="contact">
      <div className="footer-glow"></div>

      <div className="footer-container" ref={containerRef}>
        <div className="footer-brand">
          <h2>DeepGuard</h2>
          <p>
            DeepGuard analyzes uploaded videos with trained deep learning
            models to help identify manipulated content.
          </p>
        </div>

        <div className="footer-links">
          <h3>Tools</h3>
          <a href="#tools">Video analysis</a>
        </div>

        <div className="footer-links">
          <h3>About</h3>
          <a href="#about">How It Works</a>
          <a href="#">Privacy Policy</a>
        </div>

        <div className="footer-links">
          <h3>Contact</h3>
          <a href="mailto:hello@deepguard.local">Email DeepGuard</a>

          <div className="footer-icons">
            <a href="mailto:princemaurya756@gmail.com" aria-label="Email">✉️</a>
            <a href="https://www.nexora.com" target="_blank" rel="noreferrer" aria-label="Website">🌐</a>
            <a href="/privacy-policy.html" aria-label="Privacy Policy">🔒</a>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        © 2026 DeepGuard
      </div>
    </footer>
  );
}
