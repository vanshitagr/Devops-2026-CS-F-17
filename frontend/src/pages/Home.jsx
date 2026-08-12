import { useState, useEffect } from "react";
import api from "../api";
import GigCard from "../components/GigCard";
import { CATEGORIES, LOCATIONS } from "../constants";

export default function Home() {
  const [gigs, setGigs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState("");
  const [location, setLocation] = useState("");
  const [search, setSearch] = useState("");

  const fetchGigs = async () => {
    setLoading(true);
    try {
      const params = { status: "open" };
      if (category) params.category = category;
      if (location) params.location = location;
      if (search) params.search = search;
      const res = await api.get("/gigs", { params });
      setGigs(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

// Re-fetch gigs whenever category or location filters change.
// Search is handled separately via the form's onSubmit so we don't
// hit the API on every keystroke.
useEffect(() => {
    fetchGigs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [category, location]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchGigs();
  };

  return (
    <div className="page">
      

      <form className="filters" onSubmit={handleSearchSubmit}>
        <input
          placeholder="Search gigs..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="">All Categories</option>
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
        <select value={location} onChange={(e) => setLocation(e.target.value)}>
          <option value="">All Locations</option>
          {LOCATIONS.map((l) => (
            <option key={l} value={l}>
              {l}
            </option>
          ))}
        </select>
        <button type="submit" className="btn-primary">
          Search
        </button>
      </form>

      {loading ? (
        <p className="muted">Loading gigs...</p>
      ) : gigs.length === 0 ? (
        <p className="muted">No open gigs match your filters right now.</p>
      ) : (
        <div className="gig-grid">
          {gigs.map((g) => (
            <GigCard key={g._id} gig={g} />
          ))}
        </div>
      )}
    </div>
  );
}
