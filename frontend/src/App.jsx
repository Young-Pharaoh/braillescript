import React, { useState } from 'react';
import Header from './components/Header';
import TextInput from './components/TextInput';
import ExportBar from './components/ExportBar';
import BrailleDisplay from './components/BrailleDisplay';
import { transcribeText } from './api/brailleApi';

export default function App() {
  const [text, setText] = useState('');
  const [cells, setCells] = useState([]);
  const [unicodeBraille, setUnicodeBraille] = useState('');
  const [showLabels, setShowLabels] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [transcribedText, setTranscribedText] = useState('');

  const handleTranscribe = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError('');
    try {
      const data = await transcribeText(text, showLabels);
      setCells(data.cells);
      setUnicodeBraille(data.unicode_braille);
      setTranscribedText(data.original);
    } catch (err) {
      setError(err.message || 'Error al transcribir el texto.');
      setCells([]);
      setUnicodeBraille('');
      setTranscribedText('');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Header />

      <TextInput
        text={text}
        onTextChange={setText}
        showLabels={showLabels}
        onToggleLabels={setShowLabels}
        onTranscribe={handleTranscribe}
        loading={loading}
      />

      {error && (
        <div className="error-banner" id="error-banner" role="alert">
          {error}
        </div>
      )}

      <ExportBar
        text={transcribedText}
        showLabels={showLabels}
        disabled={!cells.length}
      />

      <BrailleDisplay
        cells={cells}
        unicodeBraille={unicodeBraille}
        showLabels={showLabels}
      />
    </div>
  );
}
