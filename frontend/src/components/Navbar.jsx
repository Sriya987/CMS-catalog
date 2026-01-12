import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div className="navbar">
      <strong>CMS Catalog</strong>
      <div>
        <Link to="/programs">Programs</Link>
      </div>
    </div>
  );
}
