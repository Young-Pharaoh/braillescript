import React from 'react';
import BrailleCell from './BrailleCell';

/**
 * BrailleDisplay – Shows Unicode Braille string and the rendered cell grid.
 */
export default function BrailleDisplay({ cells = [], unicodeBraille = '', showLabels = true }) {
  if (!cells.length) return null;

  return (
    <section className="braille-display" id="braille-display">
      {/* Unicode string */}
      <div className="braille-display__unicode-section">
        <div className="braille-display__section-label">Braille Unicode</div>
        <div className="braille-display__unicode">{unicodeBraille}</div>
      </div>

      {/* Visual cell grid */}
      <div className="braille-display__unicode-section">
        <div className="braille-display__section-label">Celdas Braille</div>
        <div className="braille-display__cells-grid">
          {cells.map((cell, i) => (
            <BrailleCell
              key={i}
              dots={cell.dots}
              char={cell.char}
              showLabel={showLabels}
              index={i}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
