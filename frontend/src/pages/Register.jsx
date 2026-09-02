import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Register() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    course: "",
    year: "",
    phone: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await register(form);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Create your account</h2>
        <p className="auth-sub">Join GigBoard - built for SKIT Jagatpura students</p>
        {error && <div className="error-box">{error}</div>}

        <label>Full Name</label>
        <input name="name" value={form.name} onChange={handleChange} required />

        <label>College Email</label>
        <input
          name="email"
          type="email"
          placeholder="yourname@skit.ac.in"
          value={form.email}
          onChange={handleChange}
          required
        />

        <label>Password</label>
        <input
          name="password"
          type="password"
          minLength={6}
          value={form.password}
          onChange={handleChange}
          required
        />

        <div className="form-row">
          <div>
            <label>Course</label>
            <input
              name="course"
              placeholder="B.Tech CSE"
              value={form.course}
              onChange={handleChange}
            />
          </div>
          <div>
            <label>Year</label>
            <input
              name="year"
              placeholder="3rd Year"
              value={form.year}
              onChange={handleChange}
            />
          </div>
        </div>

        <label>Phone (optional)</label>
        <input name="phone" value={form.phone} onChange={handleChange} />

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? "Creating account..." : "Sign Up"}
        </button>
        <p className="auth-switch">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );
}
