import { useState } from "react";
import "./JobForm.css"; // You can style this how you like

const today = new Date().toISOString().split("T")[0]; // e.g., '2025-04-21'

function JobForm({ onClose, onJobAdded }) {
  const [formData, setFormData] = useState({
    company_name: "",
    application_id: "",
    position_title: "",
    status: "applied",
    applied_on: today,
    source: "",
    notes: ""
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch("http://localhost:8000/jobs/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(formData)
    });

    if (!res.ok) {
      const error = await res.json();
      alert(`Error: ${error.detail}`);
      return;
    }

    const newJob = await res.json();
    onJobAdded(newJob);
    onClose(); // Close modal after saving
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>Add Job Application</h3>
        <form onSubmit={handleSubmit}>
          <input name="company_name" placeholder="Company" onChange={handleChange} required />
          <input name="application_id" placeholder="Application ID (optional)" onChange={handleChange} />
          <input name="position_title" placeholder="Position" onChange={handleChange} required />
          <label>
            Status:
            <select
              name="status"
              value={formData.status}
              onChange={handleChange}
              className="custom-select"
            >
              <option value="applied">Applied</option>
              <option value="interview">Interview</option>
              <option value="rejected">Rejected</option>
              <option value="offer">Offer</option>
            </select>
          </label>

          <label>
            Applied On:
            <input
              className="custom-select"
              type="date"
              name="applied_on"
              value={formData.applied_on}
              onChange={handleChange}
            />
          </label>
          <input name="source" placeholder="Source" onChange={handleChange} />
          <textarea name="notes" placeholder="Notes" onChange={handleChange} />
          <div style={{ display: "flex", justifyContent: "space-between", marginTop: "1rem" }}>
            <button type="button" onClick={onClose}>Cancel</button>
            <button type="submit">Save</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default JobForm;
