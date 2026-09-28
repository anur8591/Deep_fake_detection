import useScrollReveal from '../hooks/useScrollReveal';

const TRUST_ITEMS = [
  {
    icon: '👆',
    title: 'Simple & Free to Use',
    text: 'Select a supported video and submit it to the connected analysis service.',
  },
  {
    icon: '📊',
    title: 'Accurate & Explainable Results',
    text: 'The result includes the prediction and confidence returned by the trained models.',
  },
  {
    icon: '🌍',
    title: 'Real-World Context',
    text: 'Use the prediction as supporting information when reviewing video authenticity.',
  },
  {
    icon: '🛡️',
    title: 'Privacy First',
    text: 'Uploaded videos are processed by the backend service; temporary upload files are removed after analysis.',
  },
];

export default function Trust() {
  const gridRef = useScrollReveal('.trust-card', { threshold: 0.25, stagger: 200 });

  return (
    <section className="trust-section">
      <div className="trust-header">
        <h2>Designed for Clear Results</h2>
        <p>
          DeepGuard presents model predictions and supporting details from the video analysis pipeline.
        </p>
      </div>

      <div className="trust-grid" ref={gridRef}>
        {TRUST_ITEMS.map((item) => (
          <div className="trust-card" key={item.title}>
            <div className="trust-icon">{item.icon}</div>
            <h3>{item.title}</h3>
            <p>{item.text}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
