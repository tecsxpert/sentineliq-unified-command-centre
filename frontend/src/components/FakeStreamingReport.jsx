import { useState } from "react";

export default function FakeStreamingReport() {
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);

  const generateReport = () => {
    setLoading(true);
    setReport("");

    const text =
      "AI Report Generated Successfully.\n\nDashboard analytics completed.\n\nFrontend system working correctly.\n\nAll modules operating normally.";

    let index = 0;

    const interval = setInterval(() => {
      setReport((prev) => prev + text[index]);

      index++;

      if (index >= text.length) {
        clearInterval(interval);
        setLoading(false);
      }
    }, 30);
  };

  return (
    <div className="bg-white rounded-2xl shadow p-5">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">
          AI Streaming Report
        </h2>

        <button
          onClick={generateReport}
          className="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-xl"
        >
          Generate Report
        </button>
      </div>

      {loading && (
        <p className="text-blue-600 animate-pulse mb-3">
          Generating Report...
        </p>
      )}

      <div className="bg-gray-100 rounded-xl p-4 min-h-[200px] whitespace-pre-wrap">
        {report || "No report generated yet"}
      </div>
    </div>
  );
}