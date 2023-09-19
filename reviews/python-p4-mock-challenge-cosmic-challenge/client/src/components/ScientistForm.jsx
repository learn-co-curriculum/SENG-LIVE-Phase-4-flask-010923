import React, { useState } from "react";

export default function ScientistForm({
  onScientistRequest,
  scientist = {
    name: "",
    field_of_study: "",
  },
  edit,
}) {
  const [formData, setFormData] = useState(scientist);
  const [errors, setErrors] = useState([]);

  async function postScientist() {
    const config = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    };
    const res = await fetch("/scientists", config);
    if (res.ok) {
      const newSci = await res.json();
      onScientistRequest(newSci);
      setFormData({
        name: "",
        field_of_study: "",
      });
      setErrors([]);
    } else {
      const messages = await res.json();
      setErrors(messages.errors);
    }
  }

  async function updateScientist() {
    const updateData = {
      name: formData.name,
      field_of_study: formData.field_of_study,
    };
    const config = {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updateData),
    };
    const res = await fetch(`/scientists/${scientist.id}`, config);
    if (res.ok) {
      onScientistRequest();
      setFormData({
        name: "",
        field_of_study: "",
      });
      setErrors([]);
    } else {
      const messages = await res.json();
      setErrors(messages.errors);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    if (edit) {
      updateScientist();
    } else {
      postScientist();
    }
  }

  function handleChange(e) {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
  }

  return (
    <section>
      <form onSubmit={handleSubmit}>
        <h2>{scientist.name ? "Edit Scientist" : "Add New Scientist"}</h2>
        <div>
          <label htmlFor="name">Name:</label>
        </div>
        <div>
          <input
            type="text"
            id="name"
            placeholder="Enter name"
            value={formData.name}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="field_of_study">Field of Study:</label>
        </div>
        <div>
          <input
            type="text"
            id="field_of_study"
            placeholder="Enter field of study"
            value={formData.field_of_study}
            onChange={handleChange}
          />
        </div>
        {errors.map((err) => (
          <p key={err} style={{ color: "red" }}>
            {err}
          </p>
        ))}
        <button type="submit">Submit</button>
      </form>
    </section>
  );
}
