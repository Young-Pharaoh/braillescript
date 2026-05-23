import React from 'react';

/**
 * TextInput – Textarea, toggle, and transcribe button.
 */
export default function TextInput({
  text,
  onTextChange,
  showLabels,
  onToggleLabels,
  onTranscribe,
  loading,
}) {
  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      onTranscribe();
    }
  };

  return (
    <section className="text-input-section" id="text-input-section">
      <label className="text-input__label" htmlFor="spanish-input">
        Texto en español
      </label>
      <textarea
        id="spanish-input"
        className="text-input__textarea"
        placeholder="Escribe aquí tu texto en español… por ejemplo: Hola Mundo 123"
        value={text}
        onChange={(e) => onTextChange(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={loading}
      />
      <div className="text-input__controls">
        <label className="text-input__toggle" htmlFor="toggle-labels">
          <input
            type="checkbox"
            id="toggle-labels"
            className="toggle-switch"
            checked={showLabels}
            onChange={(e) => onToggleLabels(e.target.checked)}
          />
          Mostrar etiquetas
        </label>
        <button
          id="btn-transcribe"
          className="btn-transcribe"
          onClick={onTranscribe}
          disabled={loading || !text.trim()}
        >
          {loading && <span className="spinner" />}
          {loading ? 'Transcribiendo…' : 'Transcribir'}
        </button>
      </div>
    </section>
  );
}
