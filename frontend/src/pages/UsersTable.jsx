import { useEffect, useState } from "react";
import api from "../api";

export default function UsersTable() {
  const [users, setUsers] = useState([]);

  useEffect(()=>{
    api.get("/admin/users").then(r=>setUsers(r.data));
  },[]);

  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-2">Registered Users</h2>
      <table className="table-auto w-full border">
        <thead className="bg-gray-100">
          <tr><th>ID</th><th>Username</th><th>Role</th></tr>
        </thead>
        <tbody>
          {users.map(u=>(
            <tr key={u.id} className="border-t">
              <td className="px-2 py-1">{u.id}</td>
              <td className="px-2 py-1">{u.username}</td>
              <td className="px-2 py-1">{u.role}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
