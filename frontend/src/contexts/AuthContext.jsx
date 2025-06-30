import { createContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";

import api, { setAuthToken } from "../api";

export const AuthContext = createContext();

export default function AuthProvider({ children }) {
  const [user, setUser] = useState(null);   // { id, username, role }
  const [token, setToken] = useState(localStorage.getItem("token"));

  useEffect(() => {                          // keep axios in sync
    setAuthToken(token);
    if (token) {
      const payload = jwtDecode(token);
      setUser({ id: payload.sub, username: payload.username, role: payload.role });
    } else setUser(null);
  }, [token]);

  const login = async (creds) => {
    const { data } = await api.post("/auth/login", creds);
    localStorage.setItem("token", data.access_token);
    setToken(data.access_token);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  const register = (info) => api.post("/auth/register", info);

  return (
    <AuthContext.Provider value={{ user, token, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
}
