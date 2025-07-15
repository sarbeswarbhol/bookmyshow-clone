import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api";

function Profile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const res = await api.user.getProfile();
        setUser(res.data);
      } catch (err) {
        navigate("/login");
      } finally {
        setLoading(false);
      }
    };

    fetchProfileData();
  }, [navigate]);

  const handleLogout = () => {
    api.auth.logout();
    navigate("/login");
  };

  if (loading) return <div className="p-6">Loading profile...</div>;
  if (!user) return null;

  return (
    <div className="min-h-screen bg-light p-6">
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow text-center">
        {/* 🖼️ Profile Image or Fallback */}
        {user.profile_picture ? (
          <img
            src={user.profile_picture}
            alt="Profile"
            className="w-32 h-32 rounded-full mx-auto mb-4 object-cover border-4 border-primary"
          />
        ) : (
          <div className="w-32 h-32 rounded-full bg-gray-200 flex items-center justify-center mx-auto mb-4 text-gray-500 text-sm">
            No Image
          </div>
        )}

        {/* 👤 User Info */}
        <h2 className="text-2xl font-bold text-dark mb-1">{user.username}</h2>
        <p className="text-muted mb-1"><strong>Phone:</strong> {user.phone}</p>
        <p className="text-muted mb-1"><strong>Email:</strong> {user.email || "N/A"}</p>
        <p className="text-muted mb-1"><strong>Location:</strong> {user.location || "N/A"}</p>
        <p className="text-muted mb-4"><strong>Role:</strong> {user.role}</p>

        <button
          className="mt-6 bg-primary text-white px-6 py-2 rounded hover:bg-red-600"
          onClick={handleLogout}
        >
          Logout
        </button>
      </div>
    </div>
  );
}

export default Profile;
