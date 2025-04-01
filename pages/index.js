import { useState } from "react";

export default function Home() {
  const [password, setPassword] = useState("");
  const [result, setResult] = useState("");

  const checkPassword = async (e) => {
    e.preventDefault();

    // Prepare form data
    const formData = new URLSearchParams();
    formData.append("password", password);

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/check-password/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData.toString(),
    });

    const data = await res.json();
    setResult(data.message || data.estimated_time);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
      <h1 className="text-3xl font-bold mb-6">Password Strength Checker</h1>

      <form onSubmit={checkPassword} className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <input
          type="password"
          className="p-2 border border-gray-600 rounded w-full text-white"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button
          type="submit"
          className="mt-4 bg-blue-600 px-4 py-2 rounded text-white w-full hover:bg-blue-700"
        >
          Check Password
        </button>
      </form>

      {result && (
        <div className="mt-4 bg-gray-700 p-4 rounded w-1/2 text-center">
          <p className="font-bold">Result:</p>
          <p>{result}</p>
        </div>
      )}
    </div>
  );
}
