import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api"; // make sure api.auth.register is available

function Signup() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    phone: "",
    location: "",
    date_of_birth: "",
    profile_picture: null,
    password: "",
    password2: "",
    role: "user",
  });

  const navigate = useNavigate();
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    setForm({
      ...form,
      [name]: name === "profile_picture" ? files[0] : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const formData = new FormData();
      for (const key in form) {
        if (form[key] !== null && form[key] !== "") {
          formData.append(key, form[key]);
        }
      }

      await api.auth.register(formData);
      navigate("/login");
    } catch (err) {
      setError(err.response?.data || "Registration failed");
    }
  };

  return (
    <div className="min-h-screen bg-light flex items-center justify-center px-4">
      <form
        className="bg-white shadow-md p-8 rounded-lg w-full max-w-md"
        onSubmit={handleSubmit}
        encType="multipart/form-data"
      >
        <h2 className="text-2xl font-bold mb-6 text-dark">Create Account</h2>

        {error && (
          <div className="text-red-500 text-sm mb-4">
            {typeof error === "string" ? (
              error
            ) : (
              Object.entries(error).map(([key, val]) => (
                <p key={key}>{key}: {val}</p>
              ))
            )}
          </div>
        )}

        <input
          type="text"
          name="username"
          placeholder="Username"
          value={form.username}
          onChange={handleChange}
          className="w-full p-3 mb-4 border border-muted rounded"
          required
        />

        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          className="w-full p-3 mb-4 border border-muted rounded"
          required
        />

        <input
          type="tel"
          name="phone"
          placeholder="Phone Number"
          value={form.phone}
          onChange={handleChange}
          className="w-full p-3 mb-4 border border-muted rounded"
          required
        />

        <input
          type="text"
          name="location"
          placeholder="Location"
          value={form.location}
          onChange={handleChange}
          className="w-full p-3 mb-4 border border-muted rounded"
        />

        <input
          type="date"
          name="date_of_birth"
          value={form.date_of_birth}
          onChange={handleChange}
          className="w-full p-3 mb-4 border border-muted rounded"
        />

        <select
          name="role"
          value={form.role}
          onChange={handleChange}
          className="w-full p-3 mb-4 border border-muted rounded"
          required
        >
          <option value="">Select Role</option>
          <option value="user">User</option>
          <option value="theater_owner">Theater Owner</option>
          <option value="movie_owner">Movie Owner</option>
        </select>

        <input
          type="file"
          name="profile_picture"
          accept="image/*"
          onChange={handleChange}
          className="w-full p-3 mb-4 border border-muted rounded"
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          className="w-full p-3 mb-4 border border-muted rounded"
          required
        />

        <input
          type="password"
          name="password2"
          placeholder="Confirm Password"
          value={form.password2}
          onChange={handleChange}
          className="w-full p-3 mb-6 border border-muted rounded"
          required
        />

        <button
          type="submit"
          className="w-full bg-primary text-white py-3 rounded hover:bg-red-600"
        >
          Sign Up
        </button>

        <p className="mt-4 text-sm text-center text-muted">
          Already have an account?{" "}
          <Link to="/login" className="text-primary font-semibold">Login</Link>
        </p>
      </form>
    </div>
  );
}

export default Signup;
