import { useState, useEffect, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";
import { useAuth } from "../context/AuthContext";

export default function GigDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [gig, setGig] = useState(null);
  const [bids, setBids] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [bidAmount, setBidAmount] = useState("");
  const [bidMessage, setBidMessage] = useState("");
  const [submittingBid, setSubmittingBid] = useState(false);

  const [ratingValue, setRatingValue] = useState(5);

  const isOwner = user && gig && gig.postedBy?._id === user._id;

  const fetchGig = useCallback(async () => {
    const res = await api.get(`/gigs/${id}`);
    setGig(res.data);
    return res.data;
  }, [id]);

  const fetchBids = useCallback(
    async (gigData) => {
      if (user && gigData && gigData.postedBy?._id === user._id) {
        const res = await api.get(`/gigs/${id}/bids`);
        setBids(res.data);
      }
    },
    [id, user]
  );

  const loadAll = async () => {
    setLoading(true);
    try {
      const gigData = await fetchGig();
      await fetchBids(gigData);
    } catch (err) {
      setError(err.response?.data?.message || "Could not load gig");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id, user]);

  const handleBidSubmit = async (e) => {
    e.preventDefault();
    setSubmittingBid(true);
    setError("");
    try {
      await api.post(`/gigs/${id}/bids`, {
        amount: bidAmount,
        message: bidMessage,
      });
      setBidAmount("");
      setBidMessage("");
      alert("Bid placed! The gig poster will review it.");
    } catch (err) {
      setError(err.response?.data?.message || "Could not place bid");
    } finally {
      setSubmittingBid(false);
    }
  };

  const handleSelectBid = async (bidId) => {
    if (!confirm("Assign this gig to the selected bidder?")) return;
    try {
      await api.put(`/gigs/${id}/select/${bidId}`);
      loadAll();
    } catch (err) {
      alert(err.response?.data?.message || "Could not select bid");
    }
  };

  const handleComplete = async () => {
    try {
      await api.put(`/gigs/${id}/complete`, { rating: ratingValue });
      loadAll();
    } catch (err) {
      alert(err.response?.data?.message || "Could not complete gig");
    }
  };

  const handleCancel = async () => {
    if (!confirm("Cancel this gig? This cannot be undone.")) return;
    try {
      await api.delete(`/gigs/${id}`);
      navigate("/my-gigs");
    } catch (err) {
      alert(err.response?.data?.message || "Could not cancel gig");
    }
  };

  if (loading) return <div className="page">Loading...</div>;
  if (!gig) return <div className="page">Gig not found.</div>;

  const deadline = new Date(gig.deadline).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <div className="page">
      <div className="gig-detail-card">
        <div className="gig-detail-top">
          <span className="badge">{gig.category}</span>
          <span className={`status-pill status-${gig.status}`}>{gig.status}</span>
        </div>
        <h1>{gig.title}</h1>
        <p className="gig-detail-desc">{gig.description}</p>

        <div className="gig-meta-grid">
          <div>
            <span className="meta-label">Budget</span>
            <span className="meta-value">₹{gig.budget}</span>
          </div>
          <div>
            <span className="meta-label">Location</span>
            <span className="meta-value">📍 {gig.location}</span>
          </div>
          <div>
            <span className="meta-label">Deadline</span>
            <span className="meta-value">{deadline}</span>
          </div>
          <div>
            <span className="meta-label">Posted by</span>
            <span className="meta-value">
              {gig.postedBy?.name}
              {gig.postedBy?.rating > 0 && ` (★${gig.postedBy.rating})`}
            </span>
          </div>
        </div>

        {error && <div className="error-box">{error}</div>}

        {/* OWNER VIEW */}
        {isOwner && gig.status === "open" && (
          <div className="section">
            <h3>Bids received ({bids.length})</h3>
            {bids.length === 0 ? (
              <p className="muted">No bids yet. Check back soon.</p>
            ) : (
              <div className="bid-list">
                {bids.map((b) => (
                  <div className="bid-item" key={b._id}>
                    <div>
                      <strong>{b.bidder.name}</strong>{" "}
                      {b.bidder.rating > 0 && (
                        <span className="muted">
                          ★{b.bidder.rating} · {b.bidder.gigsCompleted} gigs done
                        </span>
                      )}
                      <p>{b.message}</p>
                    </div>
                    <div className="bid-right">
                      <span className="budget">₹{b.amount}</span>
                      <button className="btn-small" onClick={() => handleSelectBid(b._id)}>
                        Select
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
            <button className="btn-danger-outline" onClick={handleCancel}>
              Cancel this gig
            </button>
          </div>
        )}

        {isOwner && gig.status === "assigned" && (
          <div className="section">
            <h3>Gig assigned</h3>
            <p>
              Assigned to <strong>{gig.assignedTo?.name || "a bidder"}</strong>. Mark it
              completed once the work is done.
            </p>
            <label>Rate the worker (1-5)</label>
            <select value={ratingValue} onChange={(e) => setRatingValue(e.target.value)}>
              {[5, 4, 3, 2, 1].map((n) => (
                <option key={n} value={n}>
                  {n} star{n > 1 ? "s" : ""}
                </option>
              ))}
            </select>
            <button className="btn-primary" onClick={handleComplete}>
              Mark as Completed
            </button>
          </div>
        )}

        {isOwner && gig.status === "completed" && (
          <div className="section success-box">This gig has been completed. ✅</div>
        )}

        {/* NON-OWNER VIEW */}
        {!isOwner && user && gig.status === "open" && (
          <div className="section">
            <h3>Place a bid</h3>
            <form onSubmit={handleBidSubmit} className="bid-form">
              <label>Your amount (₹)</label>
              <input
                type="number"
                min={0}
                value={bidAmount}
                onChange={(e) => setBidAmount(e.target.value)}
                required
              />
              <label>Message to poster</label>
              <textarea
                rows={3}
                placeholder="Why you're a good fit, your availability, etc."
                value={bidMessage}
                onChange={(e) => setBidMessage(e.target.value)}
                required
              />
              <button type="submit" className="btn-primary" disabled={submittingBid}>
                {submittingBid ? "Placing bid..." : "Place Bid"}
              </button>
            </form>
          </div>
        )}

        {!user && (
          <div className="section muted">Log in to place a bid on this gig.</div>
        )}
      </div>
    </div>
  );
}
