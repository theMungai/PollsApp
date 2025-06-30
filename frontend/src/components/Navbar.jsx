import { Link, useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import { useState } from "react";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="bg-blue-600 text-white fixed top-0 w-full z-50 shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex-shrink-0 text-xl font-bold">🗳️  PollsApp</div>
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-white focus:outline-none"
            >
              ☰
            </button>
          </div>

          <div className="hidden md:flex space-x-4 items-center">
            {user && (
              <>
                <Link to="/dashboard">Dashboard</Link>
                {user.role === "admin" && (
                  <>
                    <Link to="/admin">Admin</Link>
                    <Link to="/admin/create">Create Poll</Link>
                    <Link to="/admin/users">Users</Link>
                  </>
                )}
                <button
                  onClick={handleLogout}
                  className="bg-red-500 px-2 py-1 rounded"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && user && (
        <div className="md:hidden px-4 pb-4 space-y-2">
          <Link to="/dashboard" onClick={() => setIsOpen(false)}>
            Dashboard
          </Link>
          {user.role === "admin" && (
            <>
              <Link to="/admin" onClick={() => setIsOpen(false)}>
                Admin
              </Link>
              <Link to="/admin/create" onClick={() => setIsOpen(false)}>
                Create Poll
              </Link>
              <Link to="/admin/users" onClick={() => setIsOpen(false)}>
                Users
              </Link>
            </>
          )}
          <button
            onClick={() => {
              setIsOpen(false);
              handleLogout();
            }}
            className="bg-red-500 px-2 py-1 rounded"
          >
            Logout
          </button>
        </div>
      )}
    </nav>
  );
}
