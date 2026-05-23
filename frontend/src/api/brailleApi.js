const API_BASE = '/api';

/**
 * Transcribe Spanish text to Braille via the backend.
 * @param {string} text
 * @param {boolean} showLabels
 * @returns {Promise<{original: string, cells: object[], unicode_braille: string}>}
 */
export async function transcribeText(text, showLabels = true) {
  const res = await fetch(`${API_BASE}/transcribe`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, show_labels: showLabels }),
  });
  if (!res.ok) {
    throw new Error(`Transcription failed: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

/**
 * Build the URL for PNG image export.
 */
export function getImageUrl(text, showLabels = true) {
  const params = new URLSearchParams({
    text,
    show_labels: showLabels,
    format: 'png',
  });
  return `${API_BASE}/export/image?${params}`;
}

/**
 * Build the URL for PDF export.
 */
export function getPdfUrl(text, showLabels = true) {
  const params = new URLSearchParams({
    text,
    show_labels: showLabels,
  });
  return `${API_BASE}/export/pdf?${params}`;
}
