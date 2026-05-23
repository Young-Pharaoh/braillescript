import React from 'react';
import { getImageUrl, getPdfUrl } from '../api/brailleApi';

export default function ExportBar({ text, showLabels, disabled }) {
  if (disabled) return null;

  const handleExportPng = () => {
    window.open(getImageUrl(text, showLabels), '_blank');
  };

  const handleExportPdf = () => {
    window.open(getPdfUrl(text, showLabels), '_blank');
  };

  return (
    <div className="export-bar" id="export-bar">
      <button id="btn-export-png" className="btn-export" onClick={handleExportPng}>
        <span className="btn-export__icon">🖼️</span>
        Exportar PNG
      </button>
      <button id="btn-export-pdf" className="btn-export" onClick={handleExportPdf}>
        <span className="btn-export__icon">📄</span>
        Exportar PDF
      </button>
    </div>
  );
}
