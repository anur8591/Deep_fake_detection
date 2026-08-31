import { useState } from "react";
import {
  Shield,
  Video,
  Target,
  BrainCircuit,
  Zap,
} from "lucide-react";

import Navbar from "./components/Navbar";
import VideoUploader from "./components/VideoUploader";
import ResultCard from "./components/ResultCard";

import heroImage from "./assets/deepguard-hero.png";
import aboutImage from "./assets/deepguard-about.png";

import "./App.css";


function App() {

  // ================= STATE =================

  const [showResult, setShowResult] = useState(false);

  const [result, setResult] = useState(null);

  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const [error, setError] = useState("");


  // ================= ANALYZE VIDEO =================

  const handleAnalyze = async (video) => {

    if (!video) {
      return;
    }

    // Start loading state
    setIsAnalyzing(true);

    // Hide previous result
    setShowResult(false);

    setResult(null);

    setError("");


    // Create form data
    const formData = new FormData();

    formData.append("file", video);


    try {

      // Send video to FastAPI
      const response = await fetch(
        "http://127.0.0.1:8000/analyze",
        {
          method: "POST",
          body: formData,
        }
      );


      // Check response
      if (!response.ok) {

        throw new Error(
          "Video analysis failed."
        );

      }


      // Convert response to JSON
      const data = await response.json();


      console.log(
        "Backend result:",
        data
      );


      // Store backend result
      setResult(data);

      // Show result card
      setShowResult(true);

    } catch (error) {

      console.error(
        "Analysis error:",
        error
      );


      setError(
        "Unable to analyze the video. Please make sure the backend is running."
      );

    } finally {

      // Stop loading
      setIsAnalyzing(false);

    }
  };


  // ================= RESET =================

  const handleReset = () => {

    setShowResult(false);

    setResult(null);

    setError("");

    setIsAnalyzing(false);

  };


  return (

    <div className="app">

      <Navbar />

      <main>


        {/* ================= HERO ================= */}

        <section
          className="hero-section"
          id="dashboard"
        >

          <div className="hero-content">

            <div className="hero-badge">

              <span className="live-dot"></span>

              AI-POWERED DEEPFAKE DETECTION

            </div>


            <h1>

              Detect <span>Deepfakes.</span>

              <br />

              Trust <strong>Reality.</strong>

            </h1>


            <p>

              Upload a video and our AI model will analyze it
              frame-by-frame to detect manipulated content
              with confidence.

            </p>


            <div className="hero-features">


              <div className="hero-feature">

                <div className="feature-icon">

                  <BrainCircuit size={19} />

                </div>

                <div>

                  <strong>
                    AI-Powered
                  </strong>

                  <span>
                    Deep Learning
                  </span>

                </div>

              </div>


              <div className="hero-feature">

                <div className="feature-icon">

                  <Video size={19} />

                </div>

                <div>

                  <strong>
                    Frame Analysis
                  </strong>

                  <span>
                    Smart Processing
                  </span>

                </div>

              </div>


              <div className="hero-feature">

                <div className="feature-icon">

                  <Target size={19} />

                </div>

                <div>

                  <strong>
                    High Accuracy
                  </strong>

                  <span>
                    Reliable Results
                  </span>

                </div>

              </div>


            </div>

          </div>


          <div className="hero-image-wrapper">

            <img
              src={heroImage}
              alt="AI deepfake detection"
            />

            <div className="hero-status">

              <span>⚠</span>

              DEEPFAKE DETECTED

            </div>

          </div>

        </section>



        {/* ================= ANALYSIS ================= */}

        <section className="analysis-layout">


          {/* ================= UPLOAD ================= */}

          <div className="analysis-card upload-card">

            <div className="card-title">

              <span>01</span>

              <div>

                <h2>
                  Upload Video
                </h2>

                <p>
                  Select a video for analysis
                </p>

              </div>

            </div>


            <VideoUploader

              onAnalyze={handleAnalyze}

              onVideoSelected={() => {

                setShowResult(false);

                setResult(null);

                setError("");

              }}

              onReset={handleReset}

            />

          </div>



          {/* ================= RESULT ================= */}

          <div className="analysis-card result-wrapper">

            <div className="card-title">

              <span>02</span>

              <div>

                <h2>
                  Analysis Result
                </h2>

                <p>
                  AI detection summary
                </p>

              </div>

            </div>



            {/* ANALYZING */}

            {isAnalyzing ? (

              <div className="empty-result">

                <div className="empty-icon">

                  <Zap size={30} />

                </div>


                <h3>
                  Analyzing Video...
                </h3>


                <p>

                  DeepGuard is extracting frames
                  and analyzing them with the
                  CNN models.

                </p>


                <div className="empty-placeholder">

                  <span>
                    PROCESSING
                  </span>

                  <small>
                    Please wait...
                  </small>

                </div>

              </div>


            ) : error ? (


              /* ================= ERROR ================= */

              <div className="empty-result">

                <div className="empty-icon">

                  <Shield size={30} />

                </div>


                <h3>
                  Analysis Failed
                </h3>


                <p>
                  {error}
                </p>

              </div>


            ) : showResult ? (


              /* ================= RESULT ================= */

              <ResultCard
                result={result}
              />


            ) : (


              /* ================= EMPTY ================= */

              <div className="empty-result">

                <div className="empty-icon">

                  <Shield size={30} />

                </div>


                <h3>
                  Ready for Analysis
                </h3>


                <p>

                  Upload a video and click{" "}

                  <strong>
                    Analyze Video
                  </strong>

                  {" "}to see the detection result.

                </p>


                <div className="empty-placeholder">

                  <span>
                    REAL / FAKE
                  </span>

                  <small>
                    Waiting for video analysis
                  </small>

                </div>

              </div>

            )}

          </div>

        </section>



        {/* ================= PIPELINE ================= */}

        <section
          className="pipeline-section"
          id="how-it-works"
        >

          <div className="section-heading">

            <div className="section-line"></div>

            <h2>
              Detection Pipeline
            </h2>

            <div className="section-line"></div>

            <p>
              How our system works
            </p>

          </div>


          <div className="pipeline">


            <PipelineStep
              number="01"
              icon={<Video size={21} />}
              title="Input Video"
              description="Upload video"
            />


            <div className="pipeline-arrow">
              →
            </div>


            <PipelineStep
              number="02"
              icon={<Video size={21} />}
              title="Extract Frames"
              description="Video converted into frames"
            />


            <div className="pipeline-arrow">
              →
            </div>


            <PipelineStep
              number="03"
              icon={<Zap size={21} />}
              title="Preprocess"
              description="Resize and normalize"
            />


            <div className="pipeline-arrow">
              →
            </div>


            <PipelineStep
              number="04"
              icon={<BrainCircuit size={21} />}
              title="CNN Model"
              description="Deep learning analysis"
            />


            <div className="pipeline-arrow">
              →
            </div>


            <PipelineStep
              number="05"
              icon={<Shield size={21} />}
              title="Prediction"
              description="Real or Fake"
            />

          </div>

        </section>



        {/* ================= ABOUT ================= */}

        <section
          className="about-section"
          id="about"
        >

          <div className="about-image">

            <img
              src={aboutImage}
              alt="Deepfake detection system"
            />

          </div>


          <div className="about-content">

            <div className="about-title">

              <Shield size={25} />

              <h2>

                About <span>DeepGuard</span>

              </h2>

            </div>


            <p>

              DeepGuard is an AI-powered deepfake detection
              system designed to identify manipulated video
              content using deep learning.

            </p>


            <p>

              The system analyzes video frames individually
              and uses a Convolutional Neural Network (CNN)
              to determine whether the content is real or
              artificially manipulated.

            </p>


            <div className="about-features">


              <AboutFeature
                icon={<Target size={20} />}
                title="High Accuracy"
                description="Deep learning model"
              />


              <AboutFeature
                icon={<Zap size={20} />}
                title="Fast Processing"
                description="Frame-by-frame analysis"
              />


              <AboutFeature
                icon={<Shield size={20} />}
                title="Privacy Focused"
                description="Secure video analysis"
              />

            </div>

          </div>

        </section>



        {/* ================= FOOTER ================= */}

        <footer>

          <div className="footer-brand">

            <Shield size={20} />

            <span>
              DeepGuard
            </span>

          </div>


          <p>
            AI-powered Deepfake Detection System
          </p>


          <a
            href="#"
            className="github-link"
          >
            GitHub
          </a>

        </footer>


      </main>

    </div>

  );
}



/* ================= PIPELINE COMPONENT ================= */

function PipelineStep({
  number,
  icon,
  title,
  description,
}) {

  return (

    <div className="pipeline-step">

      <div className="pipeline-icon">

        {icon}

      </div>


      <span className="pipeline-number">

        {number}

      </span>


      <h3>
        {title}
      </h3>


      <p>
        {description}
      </p>

    </div>

  );

}



/* ================= ABOUT COMPONENT ================= */

function AboutFeature({
  icon,
  title,
  description,
}) {

  return (

    <div className="about-feature">

      <div className="about-feature-icon">

        {icon}

      </div>


      <div>

        <strong>
          {title}
        </strong>

        <span>
          {description}
        </span>

      </div>

    </div>

  );

}


export default App;