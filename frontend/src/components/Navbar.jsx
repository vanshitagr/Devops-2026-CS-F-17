import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <Link to="/" className="brand">
        <span className="brand-icon">⚡</span> GigBoard
        <span className="brand-sub">SKIT Jagatpura, Jaipur</span>
      </Link>
      <div className="nav-links">
        <Link to="/">Browse Gigs</Link>
        {user && <Link to="/post">Post a Gig</Link>}
        {user && <Link to="/my-gigs">My Gigs</Link>}
        {user && <Link to="/my-bids">My Bids</Link>}
        {user ? (
          <div className="nav-user">
            <Link to="/profile">{user.name}</Link>
            <button onClick={handleLogout} className="btn-link">
              Logout
            </button>
          </div>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register" className="btn-primary-nav">
              Sign Up
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
