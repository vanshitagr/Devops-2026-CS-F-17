import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { CATEGORIES, LOCATIONS } from "../constants";

export default function PostGig() {
  const [form, setForm] = useState({
    title: "",
    description: "",
    category: CATEGORIES[0],
    budget: "",
    location: LOCATIONS[0],
    deadline: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await api.post("/gigs", form);
      navigate(`/gigs/${res.data._id}`);
    } catch (err) {
      setError(err.response?.data?.message || "Could not post gig");
    } finally {
      setLoading(false);
    }
  };

  const minDate = new Date().toISOString().split("T")[0];

  return (
    <div className="page">
      <div className="form-card">
        <h2>Post a new gig</h2>
        <p className="muted">Describe the task clearly so others can bid confidently.</p>
        {error && <div className="error-box">{error}</div>}
        <form onSubmit={handleSubmit}>
          <label>Title</label>
          <input
            name="title"
            placeholder="e.g. Help shifting hostel room"
            value={form.title}
            onChange={handleChange}
            required
          />

          <label>Description</label>
          <textarea
            name="description"
            rows={5}
            placeholder="Give details: what, where exactly, how long it'll take..."
            value={form.description}
            onChange={handleChange}
            required
          />

          <div className="form-row">
            <div>
              <label>Category</label>
              <select name="category" value={form.category} onChange={handleChange}>
                {CATEGORIES.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label>Location</label>
              <select name="location" value={form.location} onChange={handleChange}>
                {LOCATIONS.map((l) => (
                  <option key={l} value={l}>
                    {l}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div>
              <label>Budget (₹)</label>
              <input
                name="budget"
                type="number"
                min={0}
                placeholder="300"
                value={form.budget}
                onChange={handleChange}
                required
              />
            </div>
            <div>
              <label>Deadline</label>
              <input
                name="deadline"
                type="date"
                min={minDate}
                value={form.deadline}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Posting..." : "Post Gig"}
          </button>
        </form>
      </div>
    </div>
  );
}
