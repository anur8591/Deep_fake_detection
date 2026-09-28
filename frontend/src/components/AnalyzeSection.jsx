import { useState } from 'react';
import { Shield, Video, Zap, BrainCircuit, Target } from 'lucide-react';

import VideoUploader from './deepguard/VideoUploader';
import ProcessingStatus from './deepguard/ProcessingStatus';
import ResultCard from './deepguard/ResultCard';
import ErrorState from './deepguard/ErrorState';

import { analyzeMedia } from '../api';
import aboutImage from '../assets/deepguard-about.png';

// 'idle' | 'loading' | 'done' | 'error'
const STATUS = { IDLE: 'idle', LOADING: 'loading', DONE: 'done', ERROR: 'error' };

export default function AnalyzeSection() {
  const [status, setStatus] = useState(STATUS.IDLE);
  const [currentFile, setCurrentFile] = useState(null);
  const [result, setResult] = useState(null);
  const [processingTimeMs, setProcessingTimeMs] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const runAnalysis = async (file) => {
    setStatus(STATUS.LOADING);
    setErrorMessage('');
    const startedAt = performance.now();

    try {
      const data = await analyzeMedia(file);
      setResult(data);
      setProcessingTimeMs(performance.now() - startedAt);
      setStatus(STATUS.DONE);
    } catch (err) {
      const friendly =
        err.message === 'Failed to fetch'
          ? 'Could not reach the analysis server. Make sure the backend is running on ' +
            (import.meta.env.VITE_API_URL || 'http://localhost:8000') + '.'
          : err.message;
      setErrorMessage(friendly);
      setStatus(STATUS.ERROR);
    }
  };

  const handleAnalyze = (file) => {
    setCurrentFile(file);
    runAnalysis(file);
  };

  const handleVideoSelected = () => {
    setStatus(STATUS.IDLE);
    setResult(null);
    setErrorMessage('');
  };

  const handleReset = () => {
    setCurrentFile(null);
    setStatus(STATUS.IDLE);
    setResult(null);
    setErrorMessage('');
  };

  const handleReanalyze = () => {
    if (currentFile) runAnalysis(currentFile);
  };

  return (
    <>
      {/* ===== Upload / Result — id="tools" kept so Navbar's "Tools" anchor still works ===== */}
      <section className="dg-analyze-section" id="tools">
        <div className="dg-container">
          <div className="dg-sec-h1"><h1>Deepfake Detection Tools</h1></div>

          <div className="dg-analysis-layout">
            <div className="dg-analysis-card">
              <div className="dg-card-title">
                <span>01</span>
                <div>
                  <h2>Upload Video</h2>
                  <p>Select a video for analysis</p>
                </div>
              </div>

              <VideoUploader
                onAnalyze={handleAnalyze}
                onVideoSelected={handleVideoSelected}
                onReset={handleReset}
                isAnalyzing={status === STATUS.LOADING}
              />
            </div>

            <div className="dg-analysis-card">
              <div className="dg-card-title">
                <span>02</span>
                <div>
                  <h2>Analysis Result</h2>
                  <p>AI detection summary</p>
                </div>
              </div>

              {status === STATUS.LOADING && <ProcessingStatus fileName={currentFile?.name} />}

              {status === STATUS.DONE && result && (
                <ResultCard result={result} processingTimeMs={processingTimeMs} onReanalyze={handleReanalyze} />
              )}

              {status === STATUS.ERROR && (
                <ErrorState message={errorMessage} onRetry={handleReanalyze} />
              )}

              {status === STATUS.IDLE && (
                <div className="dg-empty-result">
                  <div className="dg-empty-icon"><Shield size={30} /></div>
                  <h3>Ready for Analysis</h3>
                  <p>Upload a video and click <strong>Analyze Video</strong> to see the detection result.</p>
                  <div className="dg-empty-placeholder">
                    <span>REAL / FAKE</span>
                    <small>Waiting for video analysis</small>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* ===== Detection Pipeline ===== */}
      <section className="dg-pipeline-section">
        <div className="dg-container">
          <div className="dg-section-heading">
            <div className="dg-section-line"></div>
            <h2>Detection Pipeline</h2>
            <div className="dg-section-line"></div>
          </div>
          <p className="dg-section-sub">How our system works</p>

          <div className="dg-pipeline">
            <PipelineStep number="01" icon={<Video size={21} />} title="Input Video" description="Upload video" />
            <div className="dg-pipeline-arrow">→</div>
            <PipelineStep number="02" icon={<Zap size={21} />} title="Backend Request" description="Sent to analysis API" />
            <div className="dg-pipeline-arrow">→</div>
            <PipelineStep number="03" icon={<BrainCircuit size={21} />} title="Model Analysis" description="Backend evaluates the file" />
            <div className="dg-pipeline-arrow">→</div>
            <PipelineStep number="04" icon={<Shield size={21} />} title="Prediction" description="Real or Fake + confidence" />
          </div>
        </div>
      </section>

      {/* ===== About DeepGuard ===== */}
      <section className="dg-about-section" id="about">
        <div className="dg-container dg-about-inner">
          <div className="dg-about-image">
            <img src={aboutImage} alt="Deepfake detection system" />
          </div>

          <div className="dg-about-content">
            <div className="dg-about-title">
              <Shield size={25} />
              <h2>About <span>DeepGuard</span></h2>
            </div>

            <p>
              DeepGuard sends uploaded video to this project's FastAPI service,
              where its trained models evaluate extracted video frames for
              signs of manipulation.
            </p>

            <p>
              The result panel displays the prediction, confidence, technique,
              and frame count returned by the analysis service.
            </p>

            <div className="dg-about-features">
              <AboutFeature icon={<Target size={20} />} title="Model Results" description="Predictions from the analysis API" />
              <AboutFeature icon={<Zap size={20} />} title="Fast Feedback" description="Upload, analyze, done" />
              <AboutFeature icon={<Shield size={20} />} title="Client-Side Validation" description="Rejects invalid or oversized files" />
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

function PipelineStep({ number, icon, title, description }) {
  return (
    <div className="dg-pipeline-step">
      <div className="dg-pipeline-icon">{icon}</div>
      <span className="dg-pipeline-number">{number}</span>
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}

function AboutFeature({ icon, title, description }) {
  return (
    <div className="dg-about-feature">
      <div className="dg-about-feature-icon">{icon}</div>
      <div><strong>{title}</strong><span>{description}</span></div>
    </div>
  );
}
