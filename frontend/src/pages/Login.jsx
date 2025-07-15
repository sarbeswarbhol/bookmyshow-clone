import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api"; // make sure api.auth.login is set up

function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.auth.login(form); // call your DRF login endpoint
      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);
      localStorage.setItem("user", JSON.stringify(res.data.user));
      navigate("/");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Invalid credentials. Please try again."
      );
    }
  };

  return (
    <div className="min-h-screen bg-light flex items-center justify-center px-4">
      <form
        className="bg-white shadow-md p-8 rounded-lg w-full max-w-sm"
        onSubmit={handleSubmit}
      >
        <h2 className="text-2xl font-bold mb-6 text-dark">Login</h2>

        {error && (
          <div className="mb-4 text-red-600 text-sm text-center">{error}</div>
        )}

        <input
          type="text"
          name="username"
          placeholder="Username or Phone"
          value={form.username}
          onChange={handleChange}
          className="w-full p-3 mb-4 border border-muted rounded focus:outline-none focus:ring-2 focus:ring-primary"
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          className="w-full p-3 mb-6 border border-muted rounded focus:outline-none focus:ring-2 focus:ring-primary"
          required
        />

        <button
          type="submit"
          className="w-full bg-primary text-white py-3 rounded hover:bg-red-600"
        >
          Login
        </button>

        <p className="mt-4 text-sm text-center text-muted">
          Don’t have an account?{" "}
          <Link to="/signup" className="text-primary font-semibold">
            Sign up
          </Link>
        </p>
      </form>
    </div>
  );
}

export default Login;
