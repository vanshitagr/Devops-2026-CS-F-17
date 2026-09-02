import { useState, useEffect } from "react";
import api from "../api";
import GigCard from "../components/GigCard";

export default function MyGigs() {
  const [posted, setPosted] = useState([]);
  const [working, setWorking] = useState([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState("posted");

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const [p, w] = await Promise.all([
        api.get("/gigs/mine/posted"),
        api.get("/gigs/mine/working"),
      ]);
      setPosted(p.data);
      setWorking(w.data);
      setLoading(false);
    };
    load();
  }, []);

  const list = tab === "posted" ? posted : working;

  return (
    <div className="page">
      <h1>My Gigs</h1>
      <div className="tabs">
        <button
          className={tab === "posted" ? "tab active" : "tab"}
          onClick={() => setTab("posted")}
        >
          Gigs I Posted ({posted.length})
        </button>
        <button
          className={tab === "working" ? "tab active" : "tab"}
          onClick={() => setTab("working")}
        >
          Gigs I'm Working On ({working.length})
        </button>
      </div>

      {loading ? (
        <p className="muted">Loading...</p>
      ) : list.length === 0 ? (
        <p className="muted">Nothing here yet.</p>
      ) : (
        <div className="gig-grid">
          {list.map((g) => (
            <GigCard key={g._id} gig={g} />
          ))}
        </div>
      )}
    </div>
  );
}
