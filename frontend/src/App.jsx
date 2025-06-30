import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import AuthProvider from "./contexts/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminRoute from "./components/AdminRoute";
import Navbar from "./components/Navbar";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import PollDetail from "./pages/PollDetail";
import AdminDash from "./pages/AdminDashboard";
import CreatePoll from "./pages/CreatePoll";
import UsersTable from "./pages/UsersTable";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <div className="pt-20 px-4">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/" element={<Navigate to="/dashboard" replace />} />

            <Route element={<ProtectedRoute />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/polls/:id" element={<PollDetail />} />
            </Route>

            <Route element={<AdminRoute />}>
              <Route path="/admin" element={<AdminDash />} />
              <Route path="/admin/create" element={<CreatePoll />} />
              <Route path="/admin/users" element={<UsersTable />} />
            </Route>
          </Routes>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}
// test
