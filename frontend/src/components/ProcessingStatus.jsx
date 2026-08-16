import { Check, Circle, LoaderCircle } from "lucide-react";

const stages = [
  "Video loaded",
  "Extracting frames",
  "Preprocessing frames",
  "Running CNN model",
  "Generating prediction",
];

function ProcessingStatus({ currentStage }) {
  return (
    <div className="processing-card">
      <div className="processing-header">
        <div>
          <p className="section-label">ANALYSIS IN PROGRESS</p>
          <h3>Analyzing your video</h3>
        </div>

        <LoaderCircle className="processing-spinner" size={28} />
      </div>

      <div className="processing-stages">
        {stages.map((stage, index) => {
          const stageNumber = index + 1;

          const completed = currentStage > stageNumber;
          const active = currentStage === stageNumber;

          return (
            <div
              className={`processing-stage ${
                completed ? "completed" : ""
              } ${active ? "active" : ""}`}
              key={stage}
            >
              <div className="stage-icon">
                {completed ? (
                  <Check size={16} />
                ) : active ? (
                  <LoaderCircle size={16} className="stage-spinner" />
                ) : (
                  <Circle size={12} />
                )}
              </div>

              <span>{stage}</span>
            </div>
          );
        })}
      </div>

      <div className="progress-container">
        <div
          className="progress-bar"
          style={{
            width: `${(currentStage / stages.length) * 100}%`,
          }}
        />
      </div>

      <p className="processing-note">
        This is a temporary frontend simulation. The actual CNN pipeline
        will be connected here.
      </p>
    </div>
  );
}

export default ProcessingStatus;