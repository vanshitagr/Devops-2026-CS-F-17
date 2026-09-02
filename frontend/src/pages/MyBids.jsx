import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api";

export default function MyBids() {
  const [bids, setBids] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/bids/mine")
      .then((res) => setBids(res.data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="page">
      <h1>My Bids</h1>
      {loading ? (
        <p className="muted">Loading...</p>
      ) : bids.length === 0 ? (
        <p className="muted">You haven't placed any bids yet.</p>
      ) : (
        <div className="bid-list">
          {bids.map((b) => (
            <Link to={`/gigs/${b.gig?._id}`} className="bid-item" key={b._id}>
              <div>
                <strong>{b.gig?.title || "Gig removed"}</strong>
                <p>{b.message}</p>
              </div>
              <div className="bid-right">
                <span className="budget">Your bid: ₹{b.amount}</span>
                <span className={`status-pill status-${b.status}`}>{b.status}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
