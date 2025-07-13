import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = e => {
    e.preventDefault();
    // Replace with real login logic later
    console.log("Logging in with:", form);
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-light flex items-center justify-center">
      <form className="bg-white shadow-md p-8 rounded-lg w-full max-w-sm" onSubmit={handleSubmit}>
        <h2 className="text-2xl font-bold mb-6 text-dark">Login</h2>

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
          className="w-full p-3 mb-4 border border-muted rounded focus:outline-none focus:ring-2 focus:ring-primary"
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
          <Link to="/signup" className="text-primary font-semibold">Sign up</Link>
        </p>
      </form>
    </div>
  );
}

export default Login;
