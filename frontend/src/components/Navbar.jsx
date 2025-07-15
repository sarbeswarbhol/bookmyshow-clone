import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

function Navbar() {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access");
    setIsLoggedIn(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <nav className="bg-dark text-white px-6 py-4 flex justify-between items-center shadow-md">
      <Link to="/" className="text-2xl font-bold text-primary">
        BookMyShow
      </Link>

      <div className="space-x-4 flex items-center">
        <Link to="/" className="hover:text-primary">Home</Link>
        {isLoggedIn && <Link to="/profile" className="hover:text-primary">Profile</Link>}

        {isLoggedIn ? (
          <button
            onClick={handleLogout}
            className="bg-red-500 px-4 py-2 rounded-md text-white hover:bg-red-600"
          >
            Logout
          </button>
        ) : (
          <>
            <Link
              to="/login"
              className="bg-primary px-4 py-2 rounded-md text-white hover:bg-red-600"
            >
              Login
            </Link>
            <Link
              to="/signup"
              className="border border-primary text-primary px-4 py-2 rounded-md hover:bg-primary hover:text-white"
            >
              Sign Up
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
