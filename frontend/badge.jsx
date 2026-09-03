export default function Badge({ children, color }) {
  return (
    <span className="badge" style={color ? { color, background: `${color}1a` } : undefined}>
      {children}
    </span>
  );
}