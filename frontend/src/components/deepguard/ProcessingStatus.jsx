import { LoaderCircle } from 'lucide-react';

/**
 * Shown while the real request to POST /api/analyze is in flight.
 * The progress bar is indeterminate — the backend doesn't report
 * per-stage progress, so this only claims "a request is pending",
 * which is true.
 */
export default function ProcessingStatus({ fileName }) {
  return (
    <div className="dg-processing-card">
      <div className="dg-processing-header">
        <div>
          <p className="dg-section-label">ANALYSIS IN PROGRESS</p>
          <h3>Analyzing {fileName || 'your video'}</h3>
        </div>
        <LoaderCircle className="dg-processing-spinner" size={26} />
      </div>

      <div className="dg-progress-container">
        <div className="dg-progress-bar" />
      </div>

      <p className="dg-processing-note">
        Sending your video to the DeepGuard analysis server and waiting for a
        result. This usually takes a few seconds.
      </p>
    </div>
  );
}
