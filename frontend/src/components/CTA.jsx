import useScrollReveal from '../hooks/useScrollReveal';

export default function CTA({ onTryClick }) {
  // The original observes a single element (.cta-content), which this selector also matches.
  const sectionRef = useScrollReveal('.cta-content', { threshold: 0.4 });

  return (
    <section className="cta-section" ref={sectionRef}>
      <div className="cta-glow"></div>

      <div className="cta-content">
        <h2>Free Online Deepfake Detection at Your Fingertips</h2>
        <p>
          Upload a supported video format to receive a prediction from the connected analysis backend.
        </p>

        <button className="cta-btn" onClick={onTryClick}>
          Try Deepfake Detection Now →
        </button>
      </div>
    </section>
  );
}
