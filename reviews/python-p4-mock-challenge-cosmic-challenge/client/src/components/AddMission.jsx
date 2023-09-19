import React, { useState, useEffect } from "react";

function AddMission({ onAddMission, scientistId }) {
  const [formData, setFormData] = useState({
    name: "",
    planet_id: "",
  });
  const [planets, setPlanets] = useState([]);
  const [errors, setErrors] = useState([]);

  useEffect(() => {
    const fetchPlanets = async () => {
      const res = await fetch("/planets");
      const planetArr = await res.json();
      setPlanets(planetArr);
    };

    fetchPlanets().catch(console.error);
  }, []);

  function handleChange(e) {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const newMission = {
      name: formData.name,
      scientist_id: scientistId,
      planet_id: Number(formData.planet_id),
    };
    const config = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newMission),
    };
    const res = await fetch("/missions", config);
    if (res.ok) {
      const missionJson = await res.json();
      onAddMission(missionJson);
      setFormData({
        name: "",
        planet_id: "",
      });
      setErrors([]);
    } else {
      const messages = res.json();
      setErrors(messages.errors);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add New Mission</h2>
      <div>
        <label htmlFor="name">Name:</label>
        <input
          type="text"
          id="name"
          value={formData.name}
          onChange={handleChange}
        />
      </div>
      <div>
        <label htmlFor="planet_id">planet</label>
        <select
          id="planet_id"
          value={formData.planet_id}
          onChange={handleChange}
        >
          <option value="">Select planet...</option>
          {planets.map((planet) => (
            <option key={planet.id} value={planet.id}>
              {planet.name}
            </option>
          ))}
        </select>
      </div>
      {errors.map((err) => (
        <p key={err} style={{ color: "red" }}>
          {err}
        </p>
      ))}
      <button type="submit">Submit</button>
    </form>
  );
}

export default AddMission;
