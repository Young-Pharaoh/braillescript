import React from 'react';

/**
 * BrailleCell – Renders a single Braille cell as SVG.
 *
 * Dot positions (within a 60×90 cell):
 *   dot1=(15,15)  dot4=(45,15)
 *   dot2=(15,45)  dot5=(45,45)
 *   dot3=(15,75)  dot6=(45,75)
 */

const DOT_POSITIONS = [
  { dot: 1, cx: 15, cy: 15 },
  { dot: 4, cx: 45, cy: 15 },
  { dot: 2, cx: 15, cy: 45 },
  { dot: 5, cx: 45, cy: 45 },
  { dot: 3, cx: 15, cy: 75 },
  { dot: 6, cx: 45, cy: 75 },
];

const RAISED_COLOR = '#f5f0e0';
const EMPTY_FILL = '#1e1e2a';
const EMPTY_STROKE = '#3a3a4a';
const CELL_BG = '#14141e';
const CELL_BORDER = '#2e2e3e';

export default function BrailleCell({ dots = [], char = '', showLabel = true, index = 0 }) {
  const raisedSet = new Set(dots);
  const isSpace = dots.length === 0 && char === ' ';

  if (isSpace) {
    return (
      <div
        className="braille-cell braille-cell--space"
        style={{ animationDelay: `${index * 20}ms` }}
      />
    );
  }

  const svgHeight = 90;
  const totalHeight = showLabel ? svgHeight + 20 : svgHeight;

  return (
    <div
      className="braille-cell"
      style={{ animationDelay: `${index * 20}ms` }}
    >
      <svg
        className="braille-cell__svg"
        width="60"
        height={svgHeight}
        viewBox="0 0 60 90"
        xmlns="http://www.w3.org/2000/svg"
        role="img"
        aria-label={`Braille cell for "${char}"`}
      >
        {/* Cell background */}
        <rect
          x="1"
          y="1"
          width="58"
          height="88"
          rx="6"
          ry="6"
          fill={CELL_BG}
          stroke={CELL_BORDER}
          strokeWidth="1"
        />

        {/* Dots */}
        {DOT_POSITIONS.map(({ dot, cx, cy }) => {
          const isRaised = raisedSet.has(dot);
          return isRaised ? (
            <g key={dot}>
              {/* Glow / shadow */}
              <circle
                cx={cx}
                cy={cy}
                r="11"
                fill="none"
                stroke="rgba(245, 240, 224, 0.15)"
                strokeWidth="2"
              />
              {/* Raised dot */}
              <circle
                cx={cx}
                cy={cy}
                r="8"
                fill={RAISED_COLOR}
                filter="url(#dotShadow)"
              />
            </g>
          ) : (
            <circle
              key={dot}
              cx={cx}
              cy={cy}
              r="5"
              fill={EMPTY_FILL}
              stroke={EMPTY_STROKE}
              strokeWidth="1"
            />
          );
        })}

        {/* Drop shadow filter */}
        <defs>
          <filter id="dotShadow" x="-30%" y="-30%" width="160%" height="160%">
            <feDropShadow dx="0" dy="1" stdDeviation="2" floodColor="rgba(245,240,224,0.35)" />
          </filter>
        </defs>
      </svg>

      {showLabel && (
        <span className="braille-cell__label">{char}</span>
      )}
    </div>
  );
}
