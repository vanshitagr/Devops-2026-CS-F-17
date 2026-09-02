import { Link } from "react-router-dom";

const statusColors = {
  open: "#1a7f37",
  assigned: "#9a6700",
  completed: "#57606a",
  cancelled: "#cf222e",
};

export default function GigCard({ gig }) {
  const deadline = new Date(gig.deadline).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
  });

  return (
    <Link to={`/gigs/${gig._id}`} className="gig-card">
      <div className="gig-card-top">
        <span className="badge">{gig.category}</span>
        <span
          className="status-dot"
          style={{ color: statusColors[gig.status] || "#57606a" }}
        >
          ● {gig.status}
        </span>
      </div>
      <h3>{gig.title}</h3>
      <p className="gig-desc">{gig.description.slice(0, 100)}...</p>
      <div className="gig-card-bottom">
        <span className="budget">₹{gig.budget}</span>
        <span className="location">📍 {gig.location}</span>
        <span className="deadline">⏰ {deadline}</span>
      </div>
      {gig.postedBy?.name && (
        <div className="posted-by">Posted by {gig.postedBy.name}</div>
      )}
    </Link>
  );
}
