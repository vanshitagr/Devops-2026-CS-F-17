import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="page" style={{ textAlign: "center", paddingTop: 60 }}>
      <h1 style={{ fontSize: 48, marginBottom: 8 }}>404</h1>
      <p className="muted" style={{ marginBottom: 20 }}>
        This page doesn't exist — it may have been moved or the gig was removed.
      </p>
      <Link to="/" className="btn-primary" style={{ display: "inline-block" }}>
        Back to Browse Gigs
      </Link>
    </div>
  );
}