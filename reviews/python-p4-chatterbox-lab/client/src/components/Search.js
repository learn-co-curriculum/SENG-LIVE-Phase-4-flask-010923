import React from "react";

function Search({ search, onSearchChange }) {
  return (
    <nav>
      <input
        type="text"
        name="search"
        placeholder="Search..."
        autoComplete="off"
        value={search}
        onChange={e => onSearchChange(e.target.value)}
      />
    </nav>
  );
}

export default Search;
