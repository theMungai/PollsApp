import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api";
import Layout from "../components/Layout";

export default function Register() {
  const [form, setForm] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/auth/register", form);
      alert("Registered successfully! You can now log in.");
      navigate("/login");
    } catch (error) {
      alert(error.response?.data?.msg || "Registration failed.");
      console.error("Registration error:", error);
    }
  };

  return (
    <Layout>
      <div className="max-w-md mx-auto mt-20 p-8 bg-white shadow-lg rounded-2xl font-sans">
        <h1 className="text-3xl font-bold text-center mb-6 text-gray-800">Create Account 📝</h1>
        <form onSubmit={handleSubmit} className="space-y-5">
          <input
            name="username"
            placeholder="Username"
            value={form.username}
            onChange={handleChange}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <input
            name="password"
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition"
          >
            Register
          </button>
        </form>

        <p className="mt-6 text-center text-gray-600 text-sm">
          Already have an account?{" "}
          <Link to="/login" className="text-blue-600 font-medium hover:underline">
            Login
          </Link>
        </p>
      </div>
    </Layout>
  );
}
