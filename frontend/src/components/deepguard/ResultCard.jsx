import { AlertTriangle, CheckCircle2, Activity, RotateCcw } from 'lucide-react';

export default function ResultCard({ result, processingTimeMs, onReanalyze }) {
  const isFake = result.result?.toUpperCase() === 'FAKE';
  const confidence = Math.max(0, Math.min(100, Number(result.confidence) || 0));
  const processingLabel =
    typeof processingTimeMs === 'number' ? `${(processingTimeMs / 1000).toFixed(2)}s` : '—';

  return (
    <div className={`dg-result-card ${isFake ? 'fake' : 'real'}`}>
      <div className="dg-result-top">
        <div>
          <p className="dg-section-label">ANALYSIS RESULT</p>
          <h3>Detection Summary</h3>
        </div>
        <Activity size={19} />
      </div>

      <div className="dg-result-main">
        <div className="dg-result-icon">
          {isFake ? <AlertTriangle size={31} /> : <CheckCircle2 size={31} />}
        </div>
        <h2>{result.result?.toUpperCase() || 'UNKNOWN'}</h2>
        <p className="dg-result-description">
          {isFake ? 'The analysis detected signs of manipulation.' : 'The analysis classified this video as real.'}
        </p>
      </div>

      <div className="dg-confidence">
        <div className="dg-confidence-header">
          <span>Detection Confidence</span>
          <strong>{confidence}%</strong>
        </div>
        <div className="dg-confidence-track">
          <div className="dg-confidence-fill" style={{ width: `${confidence}%` }} />
        </div>
      </div>

      {isFake && result.technique && (
        <div className="dg-result-technique">
          <span>Detected Technique</span>
          <strong>{result.technique}</strong>
        </div>
      )}

      <div className="dg-result-stats">
        <div><span>Frames Analyzed</span><strong>{result.frames_analyzed ?? '—'}</strong></div>
        <div><span>Models</span><strong>{Object.keys(result.model_scores || {}).length || '—'}</strong></div>
        <div><span>Processing</span><strong>{processingLabel}</strong></div>
      </div>

      {onReanalyze && (
        <button type="button" className="dg-reanalyze-button" onClick={onReanalyze}>
          <RotateCcw size={14} style={{ verticalAlign: '-2px', marginRight: 6 }} />
          Re-run Analysis
        </button>
      )}
    </div>
  );
}
