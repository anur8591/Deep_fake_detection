import {
  AlertTriangle,
  CheckCircle2,
  ShieldAlert,
  Activity,
} from "lucide-react";

function ResultCard() {

  /* TEMPORARY RESULT */

  const result = "FAKE";

  const confidence = 94.17;

  const technique = "DeepFakes";

  const frames = 128;

  const processingTime = "4.82s";


  const isFake = result === "FAKE";


  return (
    <div
      className={`result-card ${
        isFake ? "fake" : "real"
      }`}
    >

      {/* HEADER */}

      <div className="result-top">

        <div>

          <p className="section-label">
            ANALYSIS RESULT
          </p>

          <h3>
            Detection Summary
          </h3>

        </div>

        <Activity size={19} />

      </div>


      {/* MAIN RESULT */}

      <div className="result-main">

        <div className="result-icon">

          {isFake ? (
            <AlertTriangle size={31} />
          ) : (
            <CheckCircle2 size={31} />
          )}

        </div>


        <h2>
          {result}
        </h2>


        <p className="result-description">

          {isFake
            ? "The video shows signs of manipulation."
            : "No significant signs of manipulation detected."
          }

        </p>

      </div>


      {/* CONFIDENCE */}

      <div className="confidence">

        <div className="confidence-header">

          <span>
            Detection Confidence
          </span>

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


      {/* TECHNIQUE */}

      {isFake && (

        <div className="technique-box">

          <div className="technique-icon">

            <ShieldAlert size={17} />

          </div>


          <div>

            <span>
              Detected Technique
            </span>

            <strong>
              {technique}
            </strong>

          </div>

        </div>

      )}


      {/* STATS */}

      <div className="result-stats">

        <div>

          <span>
            Frames
          </span>

          <strong>
            {frames}
          </strong>

        </div>


        <div>

          <span>
            Model
          </span>

          <strong>
            CNN
          </strong>

        </div>


        <div>

          <span>
            Processing
          </span>

          <strong>
            {processingTime}
          </strong>

        </div>

      </div>

    </div>
  );
}

export default ResultCard;