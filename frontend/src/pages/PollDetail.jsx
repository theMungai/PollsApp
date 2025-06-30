import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api";
import useAuth from "../hooks/useAuth";

export default function PollDetail() {
  const { id } = useParams(); // poll ID from route
  const [poll, setPoll] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);
  const [voted, setVoted] = useState(false);
  const [justification, setJustification] = useState("");
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchPoll() {
      try {
        const res = await api.get(`/polls/${id}`);
        setPoll(res.data);
      } catch (error) {
        console.error("Failed to fetch poll:", error);
      }
    }

    fetchPoll();
  }, [id]);

  const handleVote = async () => {
    if (!selectedOption) {
      alert("Please select an option to vote.");
      return;
    }

    try {
      await api.post(`/polls/${id}/vote`, {
        poll_option_id: selectedOption,
        justification,
      });
      setVoted(true);
    } catch (error) {
      console.error("Error submitting vote:", error);
      alert("Could not submit vote. Are you logged in?");
    }
  };

  if (!poll) return <p>Loading poll...</p>;

  return (
    <div className="max-w-xl mx-auto mt-8 p-4 border rounded shadow">
      <h2 className="text-2xl font-semibold mb-4">{poll.question}</h2>

      {user?.role === "admin" ? (
        <div>
          <h3 className="text-lg font-medium mb-2">Votes:</h3>
          {poll.options.map((option) => (
            <div key={option.id} className="mb-2">
              <p className="font-medium">{option.text}</p>
              <p className="text-sm text-gray-600">
                Votes: {option.votes.length}
              </p>
            </div>
          ))}
        </div>
      ) : voted ? (
        <p className="text-green-600 font-medium">Thanks for voting!</p>
      ) : (
        <>
          <form className="space-y-4">
            {poll.options.map((option) => (
              <div key={option.id} className="flex items-center">
                <input
                  type="radio"
                  name="option"
                  value={option.id}
                  checked={selectedOption === option.id}
                  onChange={() => setSelectedOption(option.id)}
                  className="mr-2"
                />
                <label>{option.text}</label>
              </div>
            ))}
            <textarea
              value={justification}
              onChange={(e) => setJustification(e.target.value)}
              placeholder="Why did you choose this option? (optional)"
              className="w-full p-2 border rounded"
              rows={3}
            />
            <button
              type="button"
              onClick={handleVote}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Submit Vote
            </button>
          </form>
        </>
      )}

      <button
        onClick={() => navigate("/dashboard")}
        className="mt-4 text-sm text-blue-500 hover:underline"
      >
        ← Back to Dashboard
      </button>
    </div>
  );
}
