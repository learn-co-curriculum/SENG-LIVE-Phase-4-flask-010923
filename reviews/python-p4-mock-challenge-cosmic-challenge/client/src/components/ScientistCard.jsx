import React from "react";
import { Link } from "react-router-dom";

function ScientistCard({ scientist: { id, name }, onDelete }) {
  return (
    <div className="scicard">
      <h3>{name}</h3>
      <Link to={`/scientists/${id}`}>View Missions</Link>
      <span>
        {" "}
        <button onClick={() => onDelete(id)}>
          <strong>X</strong>
        </button>
      </span>
    </div>
  );
}

export default ScientistCard;
