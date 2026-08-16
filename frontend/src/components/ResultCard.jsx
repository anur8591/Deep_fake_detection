import {
  AlertTriangle,
  CheckCircle2,
  ShieldAlert,
  Activity,
} from "lucide-react";

function ResultCard() {

  // TEMPORARY DEMO RESULT
  // Later this will come from FastAPI.

  const result = "FAKE";
  const confidence = 94.17;
  const technique = "DeepFakes";

  const isFake = result === "FAKE";

  return (
    <div className={`result-card ${isFake ? "fake" : "real"}`}>

      <div className="result-top">

        <div>
          <p className="section-label">
            ANALYSIS RESULT
          </p>

          <h3>Detection Summary</h3>
        </div>

        <Activity size={22} />

      </div>

      <div className="result-main">

        <div className="result-icon">

          {isFake ? (
            <AlertTriangle size={32} />
          ) : (
            <CheckCircle2 size={32} />
          )}

        </div>

        <h2>{result}</h2>

        <p className="result-description">
          {isFake
            ? "The video shows signs of manipulation."
            : "No significant signs of manipulation detected."
          }
        </p>

      </div>

      <div className="confidence">

        <div className="confidence-header">
          <span>Detection Confidence</span>

          <strong>
            {confidence}%
          </strong>
        </div>

        <div className="confidence-track">

          <div
            className="confidence-fill"
            style={{
              width: `${confidence}%`,
            }}
          />

        </div>

      </div>

      {isFake && (
        <div className="technique-box">

          <div className="technique-icon">
            <ShieldAlert size={18} />
          </div>

          <div>
            <span>Detected Technique</span>

            <strong>
              {technique}
            </strong>
          </div>

        </div>
      )}

      <div className="result-stats">

        <div>
          <span>Frames</span>
          <strong>128</strong>
        </div>

        <div>
          <span>Model</span>
          <strong>CNN</strong>
        </div>

        <div>
          <span>Processing</span>
          <strong>4.82s</strong>
        </div>

      </div>

      <div className="result-footer">
        <span>
          Analysis completed successfully
        </span>

        <span className="status-dot"></span>
      </div>

    </div>
  );
}

export default ResultCard;