import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import api from "../api";

export default function Profile() {
  const { user, setUser } = useAuth();
  const [form, setForm] = useState({
    name: user?.name || "",
    course: user?.course || "",
    year: user?.year || "",
    phone: user?.phone || "",
    bio: user?.bio || "",
    skills: (user?.skills || []).join(", "),
  });
  const [saved, setSaved] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await api.put("/auth/me", {
      ...form,
      skills: form.skills.split(",").map((s) => s.trim()).filter(Boolean),
    });
    setUser(res.data.user);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  if (!user) return null;

  return (
    <div className="page">
      <div className="form-card">
        <h2>My Profile</h2>
        <div className="profile-stats">
          <div>
            <span className="meta-value">★ {user.rating || 0}</span>
            <span className="meta-label">Rating ({user.ratingCount || 0} reviews)</span>
          </div>
          <div>
            <span className="meta-value">{user.gigsCompleted || 0}</span>
            <span className="meta-label">Gigs Completed</span>
          </div>
        </div>

        {saved && <div className="success-box">Profile updated!</div>}

        <form onSubmit={handleSubmit}>
          <label>Name</label>
          <input name="name" value={form.name} onChange={handleChange} />

          <label>Email</label>
          <input value={user.email} disabled />

          <div className="form-row">
            <div>
              <label>Course</label>
              <input name="course" value={form.course} onChange={handleChange} />
            </div>
            <div>
              <label>Year</label>
              <input name="year" value={form.year} onChange={handleChange} />
            </div>
          </div>

          <label>Phone</label>
          <input name="phone" value={form.phone} onChange={handleChange} />

          <label>Bio</label>
          <textarea name="bio" rows={3} value={form.bio} onChange={handleChange} />

          <label>Skills (comma separated)</label>
          <input
            name="skills"
            placeholder="React, Poster Design, Tutoring"
            value={form.skills}
            onChange={handleChange}
          />

          <button type="submit" className="btn-primary">
            Save Changes
          </button>
        </form>
      </div>
    </div>
  );
}
