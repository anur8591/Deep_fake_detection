import { AlertCircle } from 'lucide-react';

export default function ErrorState({ message, onRetry }) {
  return (
    <div className="dg-error-result">
      <div className="dg-empty-icon">
        <AlertCircle size={28} />
      </div>
      <h3>Analysis Failed</h3>
      <p>{message || 'Something went wrong while analyzing this video.'}</p>
      {onRetry && (
        <button type="button" className="dg-retry-button" onClick={onRetry}>
          Try Again
        </button>
      )}
    </div>
  );
}
