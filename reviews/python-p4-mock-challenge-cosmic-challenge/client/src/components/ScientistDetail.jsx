import React, { useState, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import PlanetCard from "./PlanetCard";
import AddMission from "./AddMission";
import ScientistForm from "./ScientistForm";

function ScientistDetail() {
  const [{ data: scientist, error, status }, setScientist] = useState({
    data: null,
    error: null,
    status: "pending",
  });
  const [showEdit, setShowEdit] = useState(false);

  const { id } = useParams();

  const fetchScientist = useCallback(async () => {
    const res = await fetch(`/scientists/${id}`);
    if (res.ok) {
      const sciJSON = await res.json();
      setScientist({ data: sciJSON, error: null, status: "resolved" });
    } else {
      const sciErr = await res.json();
      setScientist({ data: null, error: sciErr, status: "rejected" });
    }
  }, [id]);

  useEffect(() => {
    fetchScientist().catch(console.error);
  }, [id, fetchScientist]);

  function handleAddMission(newMission) {
    setScientist({
      error,
      status,
      data: {
        ...scientist,
        missions: [...scientist.missions, newMission],
      },
    });
  }

  function handleUpdateScientist() {
    fetchScientist();
    setShowEdit(false);
  }

  const planetCards = scientist?.missions.map((m) => (
    <PlanetCard key={m.planet.id} planet={m.planet} />
  ));

  if (status === "pending") return <h2>Loading...</h2>;
  if (status === "rejected") return <h2>Error: {error.error}</h2>;

  return (
    <div>
      <h2>Scientist Profile:</h2>
      <h3>{scientist.name}</h3>
      <h4>Field of Study: {scientist.field_of_study}</h4>
      <button onClick={() => setShowEdit((showEdit) => !showEdit)}>
        Edit Scientist
      </button>
      {showEdit && (
        <ScientistForm
          scientist={scientist}
          onScientistRequest={handleUpdateScientist}
          edit={true}
        />
      )}
      <hr />
      <h2>Mission Planets:</h2>
      <div className="planetList">{planetCards}</div>
      <hr />
      <AddMission onAddMission={handleAddMission} scientistId={scientist.id} />
    </div>
  );
}

export default ScientistDetail;
