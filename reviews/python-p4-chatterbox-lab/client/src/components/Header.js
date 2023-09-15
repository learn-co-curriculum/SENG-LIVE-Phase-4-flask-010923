import React from "react";

function Header({ isDarkMode, onToggleDarkMode }) {
  return (
    <header>
      <h1>Chatterbox</h1>
      <div className="toggle-switch">
        <input
          type="checkbox"
          id="toggle-dark-mode"
          checked={isDarkMode}
          onChange={(e) => onToggleDarkMode(e.target.checked)}
        />
        <label htmlFor="toggle-dark-mode"></label>
      </div>
    </header>
  );
}

export default Header;
