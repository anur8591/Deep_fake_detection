import useScrollReveal from '../hooks/useScrollReveal';

const STEPS = [
  {
    number: '01',
    title: 'Upload Your Media',
    text: 'Choose an MP4, AVI, MOV, or MKV video to submit for analysis.',
  },
  {
    number: '02',
    title: 'AI Analysis Begins',
    text: 'The backend extracts video frames and evaluates them with the available trained models.',
  },
  {
    number: '03',
    title: 'Get Authenticity Score',
    text: 'Review the real/fake prediction, confidence, analyzed frame count, and technique when available.',
  },
  {
    number: '04',
    title: 'Review the Result',
    text: 'Use the model output as one signal when assessing whether a video may be manipulated.',
  },
];

export default function HowItWorks({ onTryClick }) {
  const stepsRef = useScrollReveal('.step-card', { threshold: 0.3, stagger: 200 });

  return (
    <section className="how-it-works">
      <div className="how-header">
        <h1>How DeepGuard Analyzes Videos</h1>
        <p>
          An overview of the video analysis workflow and the result fields returned by the backend.
        </p>
      </div>

      <div className="how-container">
        <div className="how-steps" ref={stepsRef}>
          {STEPS.map((step) => (
            <div className="step-card" key={step.number}>
              <span className="step-number">{step.number}</span>
              <h3>{step.title}</h3>
              <p>{step.text}</p>
            </div>
          ))}

          <button className="how-cta" onClick={onTryClick}>
            Try Deepfake Detection Now →
          </button>
        </div>

        <div className="how-visual">
          <div className="visual-card">
            <img src="/deep-face.png" alt="AI Detection Preview" />
            <div className="scan-line"></div>
          </div>
        </div>
      </div>
    </section>
  );
}
