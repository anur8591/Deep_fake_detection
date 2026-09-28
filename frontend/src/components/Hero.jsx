import { Video, Target, BrainCircuit } from 'lucide-react';
import heroImage from '../assets/deepguard-hero.png';

export default function Hero({ onAnalyzeClick }) {
  const scrollToTools = () => {
    document.getElementById('tools')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section className="dg-hero" id="home">
      <div className="dg-container dg-hero-inner">
        <div className="dg-hero-content">
          <div className="dg-hero-badge">
            <span className="dg-live-dot"></span>
            AI-POWERED DEEPFAKE DETECTION
          </div>

          <h1>
            Detect <span className="dg-accent-blue">Deepfakes.</span>
            <br />
            Trust <span className="dg-accent-purple">Reality.</span>
          </h1>

          <p>
            Upload a video and our detection system analyzes it, returning a
            real/fake verdict with a confidence score straight from the
            backend.
          </p>

          <div className="dg-hero-buttons">
            <button className="dg-btn-primary" onClick={onAnalyzeClick}>
              Analyze Media
            </button>
            <button className="dg-btn-secondary" onClick={scrollToTools}>
              View Demo
            </button>
          </div>

          <div className="dg-hero-features">
            <div className="dg-hero-feature">
              <div className="dg-feature-icon"><BrainCircuit size={18} /></div>
              <div>
                <strong>AI-Powered</strong>
                <span>Automated Analysis</span>
              </div>
            </div>
            <div className="dg-hero-feature">
              <div className="dg-feature-icon"><Video size={18} /></div>
              <div>
                <strong>Video Analysis</strong>
                <span>Upload &amp; Detect</span>
              </div>
            </div>
            <div className="dg-hero-feature">
              <div className="dg-feature-icon"><Target size={18} /></div>
              <div>
                <strong>Confidence Score</strong>
                <span>Real Backend Results</span>
              </div>
            </div>
          </div>
        </div>

        <div className="dg-hero-image-wrapper">
          <img src={heroImage} alt="AI deepfake detection" />
          <div className="dg-hero-status">
            <span>⚠</span>
            DEEPFAKE DETECTED
          </div>
        </div>
      </div>
    </section>
  );
}
