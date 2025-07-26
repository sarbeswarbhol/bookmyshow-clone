import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { Pencil, Save } from "lucide-react";
import api from "../api";

function Profile() {
  const [user, setUser] = useState(null);
  const [form, setForm] = useState({});
  const [imageFile, setImageFile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.user.getProfile();
        setUser(res.data);
        setForm(res.data);
      } catch (err) {
        navigate("/login");
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [navigate]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImageFile(file);
  };

  const handleSave = async () => {
    try {
      const formData = new FormData();

      const allowedFields = [
        "username",
        "email",
        "phone",
        "location",
        "date_of_birth",
        "gender",
      ];

      allowedFields.forEach((field) => {
        if (form[field]) {
          formData.append(field, form[field]);
        }
      });

      // Only append profile_picture if imageFile is selected
      if (imageFile) {
        console.log(imageFile);
        formData.append("profile_picture", imageFile);
      }

      const res = await api.user.updateProfile(formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setUser(res.data.user);
      setForm(res.data.user);
      setImageFile(null);
      setIsEditing(false);
    } catch (err) {
      console.error("Update failed", err);
      alert("Update failed");
    }
  };

  const handleLogout = () => {
    api.auth.logout();
    navigate("/login");
  };

  if (loading) return <div className="p-6">Loading profile...</div>;
  if (!user) return null;

  return (
    <div className="min-h-screen bg-light p-6">
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow relative text-center">
        {/* ✏️ Edit / Save Button */}
        <button
          onClick={isEditing ? handleSave : () => setIsEditing(true)}
          className="absolute top-4 right-4 text-gray-500 hover:text-primary"
          title={isEditing ? "Save Profile" : "Edit Profile"}>
          {isEditing ? <Save size={20} /> : <Pencil size={20} />}
        </button>

        {/* 🖼️ Profile Picture */}
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

        {/* 🖼️ File Input for New Profile Picture */}
        {isEditing && (
          <div className="mb-4">
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              className="text-sm"
            />
          </div>
        )}

        {/* Fields */}
        <h2 className="text-2xl font-bold text-dark mb-1">
          {isEditing ? (
            <input
              type="text"
              name="username"
              value={form.username || ""}
              onChange={handleInputChange}
              className="text-center border rounded px-2 py-1 w-full max-w-xs"
            />
          ) : (
            user.username
          )}
        </h2>

        <p className="text-muted mb-1">
          <strong>Phone:</strong>{" "}
          {isEditing ? (
            <input
              type="text"
              name="phone"
              value={form.phone || ""}
              onChange={handleInputChange}
              className="border rounded px-2 py-1"
            />
          ) : (
            user.phone
          )}
        </p>

        <p className="text-muted mb-1">
          <strong>Email:</strong>{" "}
          {isEditing ? (
            <input
              type="email"
              name="email"
              value={form.email || ""}
              onChange={handleInputChange}
              className="border rounded px-2 py-1"
            />
          ) : (
            user.email || "N/A"
          )}
        </p>

        <p className="text-muted mb-1">
          <strong>Location:</strong>{" "}
          {isEditing ? (
            <input
              type="text"
              name="location"
              value={form.location || ""}
              onChange={handleInputChange}
              className="border rounded px-2 py-1"
            />
          ) : (
            user.location || "N/A"
          )}
        </p>

        <p className="text-muted mb-1">
          <strong>DOB:</strong>{" "}
          {isEditing ? (
            <input
              type="date"
              name="date_of_birth"
              value={form.date_of_birth || ""}
              onChange={handleInputChange}
              className="border rounded px-2 py-1"
            />
          ) : (
            user.date_of_birth || "N/A"
          )}
        </p>

        <p className="text-muted mb-1">
          <strong>Gender:</strong>{" "}
          {isEditing ? (
            <select
              name="gender"
              value={form.gender || ""}
              onChange={handleInputChange}
              className="border rounded px-2 py-1">
              <option value="">Select</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          ) : (
            user.gender || "N/A"
          )}
        </p>

        <p className="text-muted mb-4">
          <strong>Role:</strong> {user.role}
        </p>

        <button
          className="mt-6 bg-primary text-white px-6 py-2 rounded hover:bg-red-600"
          onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
}

export default Profile;
