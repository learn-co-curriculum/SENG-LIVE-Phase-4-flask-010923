import React from "react";

function PlanetCard({ planet, image }) {
  return (
    <div className="planetCard">
      <h4>Name: {planet.name}</h4>
    </div>
  );
}

export default PlanetCard;
