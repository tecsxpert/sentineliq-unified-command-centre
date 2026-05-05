import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ReportPage() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    topic: "",
    reportType: "general",
    useRag: true,
    customContext: "",
    topItemsCount: 5,
    stream: true, // Enable streaming by default
  });

  const [errors, setErrors] = useState({});
  const [generating, setGenerating] = useState(false);
  const [report, setReport] = useState(null);
  const [streamingText, setStreamingText] = useState({
    title: "",
    overview: "",
    executiveSummary: "",
  });
  const [progress, setProgress] = useState("");

  const validate = () => {
    const newErrors = {};
    if (!formData.topic.trim()) newErrors.topic = "Topic is required";
    if (formData.topItemsCount < 1 || formData.topItemsCount > 15) {
      newErrors.topItemsCount = "Top items count must be between 1 and 15";
    }
    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]:
        type === "checkbox"
          ? checked
          : type === "number"
            ? parseInt(value)
            : value,
    });
    setErrors({ ...errors, [name]: "" });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setGenerating(true);
    setReport(null);
    setStreamingText({ title: "", overview: "", executiveSummary: "" });
    setProgress("");

    try {
      if (formData.stream) {
        // Use EventSource for streaming
        await generateStreamingReport();
      } else {
        // Use regular fetch for non-streaming
        await generateRegularReport();
      }
    } catch (error) {
      console.error("Report generation failed:", error);
      setProgress("Error generating report");
    } finally {
      setGenerating(false);
    }
  };

  const generateStreamingReport = () => {
    return new Promise((resolve, reject) => {
      const eventSource = new EventSource(
        `${import.meta.env.VITE_API_URL}/api/ai/generate-report?stream=true`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
          },
        },
      );

      // Create a custom request to send the data
      fetch(
        `${import.meta.env.VITE_API_URL}/api/ai/generate-report?stream=true`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            topic: formData.topic,
            report_type: formData.reportType,
            use_rag: formData.useRag,
            custom_context: formData.customContext,
            top_items_count: formData.topItemsCount,
          }),
        },
      )
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to start streaming");
          }
        })
        .catch(reject);

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          if (data.chunk) {
            // Handle streaming text chunks
            if (event.type === "title") {
              setStreamingText((prev) => ({
                ...prev,
                title: prev.title + data.chunk,
              }));
            } else if (event.type === "overview") {
              setStreamingText((prev) => ({
                ...prev,
                overview: prev.overview + data.chunk,
              }));
            } else if (event.type === "executive_summary") {
              setStreamingText((prev) => ({
                ...prev,
                executiveSummary: prev.executiveSummary + data.chunk,
              }));
            }
          } else if (data.message) {
            // Handle progress messages
            setProgress(data.message);
          } else if (data.items) {
            // Handle top items
            setReport((prev) =>
              prev
                ? { ...prev, top_items: data.items }
                : { top_items: data.items },
            );
          } else if (data.recommendations) {
            // Handle recommendations
            setReport((prev) =>
              prev
                ? { ...prev, recommendations: data.recommendations }
                : { recommendations: data.recommendations },
            );
          } else if (data.report) {
            // Handle complete report
            setReport(data.report);
            setProgress("Report generation completed!");
            eventSource.close();
            resolve();
          }
        } catch (error) {
          console.error("Error parsing SSE data:", error);
        }
      };

      eventSource.onerror = (error) => {
        console.error("EventSource error:", error);
        setProgress("Error receiving streaming data");
        eventSource.close();
        reject(error);
      };

      // Timeout after 5 minutes
      setTimeout(() => {
        eventSource.close();
        reject(new Error("Streaming timeout"));
      }, 300000);
    });
  };

  const generateRegularReport = async () => {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/api/ai/generate-report`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          topic: formData.topic,
          report_type: formData.reportType,
          use_rag: formData.useRag,
          custom_context: formData.customContext,
          top_items_count: formData.topItemsCount,
        }),
      },
    );

    if (!response.ok) {
      throw new Error("Failed to generate report");
    }

    const result = await response.json();
    if (result.status === "success") {
      setReport(result.data);
      setProgress("Report generation completed!");
    } else {
      throw new Error(result.message || "Unknown error");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow p-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-[#1B4F8A]">
            Generate AI Report
          </h1>
          <button
            onClick={() => navigate("/")}
            className="text-gray-500 hover:text-gray-700"
          >
            ← Back to Dashboard
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5 mb-8">
          {/* Topic */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Report Topic <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              name="topic"
              value={formData.topic}
              onChange={handleChange}
              placeholder="e.g. Cybersecurity Best Practices, DevOps Automation"
              className={`w-full border rounded px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.topic ? "border-red-500" : "border-gray-300"
              }`}
            />
            {errors.topic && (
              <p className="text-red-500 text-xs mt-1">{errors.topic}</p>
            )}
          </div>

          {/* Report Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Report Type
            </label>
            <select
              name="reportType"
              value={formData.reportType}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="general">General</option>
              <option value="technical">Technical</option>
              <option value="executive">Executive</option>
              <option value="comparative">Comparative</option>
            </select>
          </div>

          {/* Use RAG */}
          <div className="flex items-center">
            <input
              type="checkbox"
              name="useRag"
              checked={formData.useRag}
              onChange={handleChange}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label className="ml-2 block text-sm text-gray-700">
              Use RAG (Retrieval-Augmented Generation) for context
            </label>
          </div>

          {/* Custom Context */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Custom Context (Optional)
            </label>
            <textarea
              name="customContext"
              value={formData.customContext}
              onChange={handleChange}
              placeholder="Additional context or specific information to include..."
              rows={3}
              className="w-full border border-gray-300 rounded px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Top Items Count */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Number of Top Items <span className="text-red-500">*</span>
            </label>
            <input
              type="number"
              name="topItemsCount"
              value={formData.topItemsCount}
              onChange={handleChange}
              min={1}
              max={15}
              className={`w-full border rounded px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.topItemsCount ? "border-red-500" : "border-gray-300"
              }`}
            />
            {errors.topItemsCount && (
              <p className="text-red-500 text-xs mt-1">
                {errors.topItemsCount}
              </p>
            )}
          </div>

          {/* Streaming */}
          <div className="flex items-center">
            <input
              type="checkbox"
              name="stream"
              checked={formData.stream}
              onChange={handleChange}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label className="ml-2 block text-sm text-gray-700">
              Enable streaming (real-time text generation)
            </label>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={generating}
            className={`w-full py-3 px-4 rounded text-white font-medium ${
              generating
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-[#1B4F8A] hover:bg-[#15396B] focus:outline-none focus:ring-2 focus:ring-blue-500"
            }`}
          >
            {generating ? "Generating Report..." : "Generate Report"}
          </button>
        </form>

        {/* Progress */}
        {progress && (
          <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded">
            <p className="text-sm text-blue-800">{progress}</p>
          </div>
        )}

        {/* Streaming Report Display */}
        {generating && formData.stream && (
          <div className="space-y-6">
            {/* Title */}
            {streamingText.title && (
              <div>
                <h2 className="text-xl font-bold text-gray-800 mb-2">Title</h2>
                <p className="text-gray-700">{streamingText.title}</p>
              </div>
            )}

            {/* Executive Summary */}
            {streamingText.executiveSummary && (
              <div>
                <h2 className="text-xl font-bold text-gray-800 mb-2">
                  Executive Summary
                </h2>
                <p className="text-gray-700 whitespace-pre-wrap">
                  {streamingText.executiveSummary}
                </p>
              </div>
            )}

            {/* Overview */}
            {streamingText.overview && (
              <div>
                <h2 className="text-xl font-bold text-gray-800 mb-2">
                  Overview
                </h2>
                <p className="text-gray-700 whitespace-pre-wrap">
                  {streamingText.overview}
                </p>
              </div>
            )}
          </div>
        )}

        {/* Complete Report Display */}
        {report && (
          <div className="space-y-6 border-t pt-6">
            <h2 className="text-2xl font-bold text-[#1B4F8A]">
              Generated Report
            </h2>

            {/* Title */}
            <div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Title</h3>
              <p className="text-lg text-gray-700">{report.title}</p>
            </div>

            {/* Executive Summary */}
            <div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">
                Executive Summary
              </h3>
              <p className="text-gray-700 whitespace-pre-wrap">
                {report.executive_summary}
              </p>
            </div>

            {/* Overview */}
            <div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Overview</h3>
              <p className="text-gray-700 whitespace-pre-wrap">
                {report.overview}
              </p>
            </div>

            {/* Top Items */}
            {report.top_items && report.top_items.length > 0 && (
              <div>
                <h3 className="text-xl font-bold text-gray-800 mb-4">
                  Top Items
                </h3>
                <div className="space-y-4">
                  {report.top_items.map((item, index) => (
                    <div
                      key={index}
                      className="border border-gray-200 rounded p-4"
                    >
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-semibold text-gray-800">
                          {item.title}
                        </h4>
                        <span
                          className={`px-2 py-1 text-xs rounded ${
                            item.impact === "high"
                              ? "bg-red-100 text-red-800"
                              : item.impact === "medium"
                                ? "bg-yellow-100 text-yellow-800"
                                : "bg-green-100 text-green-800"
                          }`}
                        >
                          {item.impact} impact
                        </span>
                      </div>
                      <p className="text-gray-600 text-sm">
                        {item.description}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Recommendations */}
            {report.recommendations && report.recommendations.length > 0 && (
              <div>
                <h3 className="text-xl font-bold text-gray-800 mb-4">
                  Recommendations
                </h3>
                <div className="space-y-4">
                  {report.recommendations.map((rec, index) => (
                    <div
                      key={index}
                      className="border border-gray-200 rounded p-4"
                    >
                      <p className="font-semibold text-gray-800 mb-2">
                        {rec.recommendation}
                      </p>
                      <div className="text-sm text-gray-600 mb-2 whitespace-pre-wrap">
                        {rec.action}
                      </div>
                      <div className="flex gap-4 text-xs text-gray-500">
                        <span>Timeline: {rec.timeline}</span>
                        <span>Effort: {rec.effort}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Metadata */}
            {report.metadata && (
              <div className="text-sm text-gray-500 border-t pt-4">
                <p>
                  Generated:{" "}
                  {new Date(report.metadata.generated_at).toLocaleString()}
                </p>
                <p>Report Type: {report.metadata.report_type}</p>
                <p>Context Used: {report.metadata.context_used}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
