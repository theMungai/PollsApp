import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";

export default function CreatePoll() {
  const nav = useNavigate();
  const [question, setQ] = useState("");
  const [options, setOpts] = useState(["",""]);

  const addOpt = () => setOpts([...options,""]);
  const changeOpt = (i,val) => setOpts(opts => opts.map((o,idx)=>idx===i?val:o));

  const submit = async e => {
    e.preventDefault();
    const poll = { question, options: options.filter(o=>o.trim()) };
    await api.post("/polls", poll);
    nav("/admin");
  };

  return (
    <Layout>
    <div className="max-w-lg mx-auto p-4">
      <h1 className="text-xl font-bold mb-4">Create new poll</h1>
      <form onSubmit={submit} className="space-y-3">
        <input value={question} onChange={e=>setQ(e.target.value)} placeholder="Question" className="input w-full"/>
        {options.map((opt,i)=>(
          <input key={i} value={opt} onChange={e=>changeOpt(i,e.target.value)} placeholder={`Option ${i+1}`} className="input w-full"/>
        ))}
        <button type="button" onClick={addOpt} className="btn">+ Add option</button>
        <button className="btn w-full">Save</button>
      </form>
    </div>
    </Layout>
  );
}
