import { useRef, useState } from "react";
import { Upload, Video, X, RotateCcw } from "lucide-react";

function VideoUploader({
  onAnalyze,
  onVideoSelected,
  onReset,
}) {
  const inputRef = useRef(null);

  const [video, setVideo] = useState(null);
  const [videoURL, setVideoURL] = useState("");

  const handleVideo = (file) => {
    if (!file) return;

    if (!file.type.startsWith("video/")) {
      alert("Please select a video file.");
      return;
    }

    setVideo(file);

    const url = URL.createObjectURL(file);

    setVideoURL(url);

    // Tell parent that a new video was selected
    onVideoSelected(file);
  };

  const handleFileChange = (event) => {
    handleVideo(event.target.files[0]);
  };

  const handleDrop = (event) => {
    event.preventDefault();

    const file = event.dataTransfer.files[0];

    handleVideo(file);
  };

  const removeVideo = () => {
    setVideo(null);
    setVideoURL("");

    if (inputRef.current) {
      inputRef.current.value = "";
    }

    onReset();
  };

  return (
    <div className="upload-wrapper">

      <div className="section-heading left-heading">
        <p className="section-label">
          VIDEO ANALYSIS
        </p>

        <h2>Analyze a video</h2>

        <p>
          Upload a video and check whether it contains
          manipulated content.
        </p>
      </div>

      {!video ? (
        <div
          className="upload-box"
          onDragOver={(event) => event.preventDefault()}
          onDrop={handleDrop}
        >
          <div className="upload-icon">
            <Upload size={30} />
          </div>

          <h3>Drop your video here</h3>

          <p>
            or select a video from your computer
          </p>

          <button
            className="upload-button"
            onClick={() => inputRef.current.click()}
          >
            <Video size={18} />
            Choose Video
          </button>

          <input
            ref={inputRef}
            type="file"
            accept="video/*"
            onChange={handleFileChange}
            hidden
          />

          <span className="upload-info">
            MP4, AVI, MOV • Maximum size 100MB
          </span>
        </div>
      ) : (
        <div className="video-preview-card">

          <div className="video-header">

            <div>
              <p className="video-label">
                SELECTED VIDEO
              </p>

              <h3 title={video.name}>
                {video.name}
              </h3>
            </div>

            <button
              className="remove-button"
              onClick={removeVideo}
              title="Choose another video"
            >
              <X size={20} />
            </button>

          </div>

          <div className="video-container">
            <video
              src={videoURL}
              controls
            />
          </div>

          <div className="video-details">
            <span>
              {(video.size / (1024 * 1024)).toFixed(2)} MB
            </span>

            <span>
              {video.type || "Video file"}
            </span>
          </div>

          <div className="video-actions">

            <button
              className="analyze-button"
              onClick={() => onAnalyze(video)}
            >
              Analyze Video
            </button>

            <button
              className="change-video-button"
              onClick={removeVideo}
            >
              <RotateCcw size={16} />
              Choose Another
            </button>

          </div>

        </div>
      )}
    </div>
  );
}

export default VideoUploader;