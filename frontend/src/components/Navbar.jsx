import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-dark text-white px-6 py-4 flex justify-between items-center shadow-md">
      <Link to="/" className="text-2xl font-bold text-primary">
        BookMyShow
      </Link>
      <div className="space-x-4">
        <Link to="/" className="hover:text-primary">Home</Link>
        <Link to="/profile" className="hover:text-primary">Profile</Link>
        <Link to="/login" className="bg-primary px-4 py-2 rounded-md text-white hover:bg-red-600">
          Login
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;
