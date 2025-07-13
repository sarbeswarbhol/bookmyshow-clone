import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

function Signup() {
  const [form, setForm] = useState({
    username: "",
    phone: "",
    password: "",
  });
  const navigate = useNavigate();

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = e => {
    e.preventDefault();
    // Replace with real signup logic
    console.log("Signing up with:", form);
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-light flex items-center justify-center">
      <form className="bg-white shadow-md p-8 rounded-lg w-full max-w-sm" onSubmit={handleSubmit}>
        <h2 className="text-2xl font-bold mb-6 text-dark">Create Account</h2>

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
          type="tel"
          name="phone"
          placeholder="Phone Number"
          value={form.phone}
          onChange={handleChange}
          className="w-full p-3 mb-4 border border-muted rounded"
          required
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
