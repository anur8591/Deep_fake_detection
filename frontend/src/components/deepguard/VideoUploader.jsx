import { useRef, useState } from 'react';
import { Upload, Video, X, RotateCcw, AlertCircle } from 'lucide-react';

const MAX_SIZE_MB = 100;
const ALLOWED_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv'];

export default function VideoUploader({ onAnalyze, onVideoSelected, onReset, isAnalyzing }) {
  const inputRef = useRef(null);
  const [video, setVideo] = useState(null);
  const [videoURL, setVideoURL] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [validationError, setValidationError] = useState('');

  const validateFile = (file) => {
    const extension = `.${file.name.split('.').pop().toLowerCase()}`;
    if (!file.type.startsWith('video/') && !ALLOWED_EXTENSIONS.includes(extension)) {
      return 'Please choose an MP4, AVI, MOV, or MKV video.';
    }
    if (!ALLOWED_EXTENSIONS.includes(extension)) {
      return 'Supported formats are MP4, AVI, MOV, and MKV.';
    }
    const sizeMB = file.size / (1024 * 1024);
    if (sizeMB > MAX_SIZE_MB) {
      return `File is ${sizeMB.toFixed(1)}MB, which is over the ${MAX_SIZE_MB}MB limit.`;
    }
    return '';
  };

  const handleVideo = (file) => {
    if (!file) return;
    const error = validateFile(file);
    if (error) {
      setValidationError(error);
      return;
    }
    setValidationError('');
    const url = URL.createObjectURL(file);
    setVideo(file);
    setVideoURL(url);
    onVideoSelected(file);
  };

  const handleFileChange = (event) => handleVideo(event.target.files[0]);

  const handleDrop = (event) => {
    event.preventDefault();
    setDragActive(false);
    handleVideo(event.dataTransfer.files[0]);
  };

  const removeVideo = () => {
    if (videoURL) URL.revokeObjectURL(videoURL);
    setVideo(null);
    setVideoURL('');
    setValidationError('');
    if (inputRef.current) inputRef.current.value = '';
    onReset();
  };

  return (
    <div className="dg-upload-wrapper">
      {!video ? (
        <div
          className={`dg-upload-box${dragActive ? ' drag-active' : ''}`}
          onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
        >
          <div className="dg-upload-icon"><Upload size={30} /></div>
          <h3>Drop your video here</h3>
          <p>or select a video from your computer</p>

          <button type="button" className="dg-upload-button" onClick={() => inputRef.current?.click()}>
            <Video size={18} />
            Choose Video
          </button>

          <input ref={inputRef} type="file" accept=".mp4,.avi,.mov,.mkv,video/mp4,video/quicktime,video/x-msvideo" onChange={handleFileChange} hidden />

          <span className="dg-upload-info">MP4, AVI, MOV • Maximum size {MAX_SIZE_MB}MB</span>

          {validationError && (
            <div className="dg-upload-error">
              <AlertCircle size={16} />
              <span>{validationError}</span>
            </div>
          )}
        </div>
      ) : (
        <div className="dg-video-preview-card">
          <div className="dg-video-header">
            <div>
              <p className="dg-video-label">SELECTED VIDEO</p>
              <h3 title={video.name}>{video.name}</h3>
            </div>
            <button type="button" className="dg-remove-button" onClick={removeVideo} disabled={isAnalyzing} title="Remove video">
              <X size={19} />
            </button>
          </div>

          <div className="dg-video-container">
            <video src={videoURL} controls />
          </div>

          <div className="dg-video-details">
            <span>{(video.size / (1024 * 1024)).toFixed(2)} MB</span>
            <span>{video.type || 'Video file'}</span>
          </div>

          <div className="dg-video-actions">
            <button type="button" className="dg-analyze-button" onClick={() => onAnalyze(video)} disabled={isAnalyzing}>
              {isAnalyzing ? 'Analyzing…' : 'Analyze Video'}
            </button>
            <button type="button" className="dg-change-video-button" onClick={removeVideo} disabled={isAnalyzing}>
              <RotateCcw size={15} />
              Choose Another
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
