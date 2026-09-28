const API_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

export async function analyzeMedia(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_URL}/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    let message = `Analysis failed (${response.status})`;
    try {
      const payload = await response.json();
      if (payload.detail) message = payload.detail;
    } catch {
      // Keep the status-based message when the server response isn't JSON.
    }
    throw new Error(message);
  }

  return response.json();
}
