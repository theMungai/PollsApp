import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";

export default function Dashboard() {
  const [polls, setPolls] = useState([]);

  useEffect(() => {
    api.get("/polls")
      .then((res) => setPolls(res.data))
      .catch((err) => {
        console.error("Failed to fetch polls:", err);
      });
  }, []);

  return (
    <div className="max-w-3xl mx-auto mt-8 px-4 font-sans">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">📊 Active Polls</h2>

      {polls.length === 0 ? (
        <p className="text-gray-500">No polls available at the moment.</p>
      ) : (
        <ul className="space-y-4">
          {polls.map((p) => (
            <li
              key={p.id}
              className="border border-gray-200 rounded-xl p-4 shadow-sm hover:shadow-md transition"
            >
              <Link
                to={`/polls/${p.id}`}
                className="text-lg font-medium text-blue-600 hover:underline"
              >
                {p.question}
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
