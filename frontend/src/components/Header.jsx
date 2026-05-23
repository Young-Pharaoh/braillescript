import React from 'react';

/**
 * Header – "BrailleScript" branding
 */
export default function Header() {
  return (
    <header className="header" id="header">
      <h1 className="header__title">BrailleScript</h1>
      <p className="header__subtitle">Transcriptor Español → Braille</p>
      <hr className="header__divider" />
    </header>
  );
}
