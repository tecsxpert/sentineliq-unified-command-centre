import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";

export default function AnalysePage() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    text: "",
    focusAreas: [],
  });

  const [errors, setErrors] = useState({});
  const [analysing, setAnalysing] = useState(false);
  const [results, setResults] = useState(null);

  const focusAreaOptions = [
    { value: "security", label: "Security" },
    { value: "compliance", label: "Compliance" },
    { value: "business", label: "Business" },
    { value: "technical", label: "Technical" },
    { value: "operational", label: "Operational" },
  ];

  const validate = () => {
    const newErrors = {};
    if (!formData.text.trim()) newErrors.text = "Document text is required";
    if (formData.text.trim().length < 50)
      newErrors.text = "Document text must be at least 50 characters";
    if (formData.text.trim().length > 10000)
      newErrors.text =
        "Document text exceeds maximum length of 10000 characters";
    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    setErrors({ ...errors, [name]: "" });
  };

  const handleFocusAreaChange = (area) => {
    setFormData((prev) => ({
      ...prev,
      focusAreas: prev.focusAreas.includes(area)
        ? prev.focusAreas.filter((a) => a !== area)
        : [...prev.focusAreas, area],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setAnalysing(true);
    setResults(null);

    try {
      const response = await API.post("/analyse-document", {
        text: formData.text.trim(),
        focus_areas:
          formData.focusAreas.length > 0 ? formData.focusAreas : undefined,
      });

      if (response.data.status === "success") {
        setResults(response.data.data);
      } else {
        throw new Error(response.data.message || "Analysis failed");
      }
    } catch (error) {
      console.error("Analysis failed:", error);
      setErrors({
        submit:
          error.response?.data?.message ||
          error.message ||
          "Analysis failed. Please try again.",
      });
    } finally {
      setAnalysing(false);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case "critical":
        return "bg-red-100 text-red-800 border-red-200";
      case "high":
        return "bg-red-50 text-red-700 border-red-200";
      case "medium":
        return "bg-yellow-50 text-yellow-700 border-yellow-200";
      case "low":
        return "bg-green-50 text-green-700 border-green-200";
      default:
        return "bg-gray-50 text-gray-700 border-gray-200";
    }
  };

  const getCategoryColor = (category, type) => {
    const colors = {
      insight: {
        technical: "bg-blue-50 text-blue-700 border-blue-200",
        business: "bg-green-50 text-green-700 border-green-200",
        operational: "bg-purple-50 text-purple-700 border-purple-200",
        strategic: "bg-indigo-50 text-indigo-700 border-indigo-200",
        compliance: "bg-orange-50 text-orange-700 border-orange-200",
        performance: "bg-cyan-50 text-cyan-700 border-cyan-200",
        security: "bg-red-50 text-red-700 border-red-200",
        general: "bg-gray-50 text-gray-700 border-gray-200",
      },
      risk: {
        security: "bg-red-100 text-red-800 border-red-300",
        compliance: "bg-orange-100 text-orange-800 border-orange-300",
        operational: "bg-purple-100 text-purple-800 border-purple-300",
        financial: "bg-yellow-100 text-yellow-800 border-yellow-300",
        reputational: "bg-pink-100 text-pink-800 border-pink-300",
        technical: "bg-blue-100 text-blue-800 border-blue-300",
        strategic: "bg-indigo-100 text-indigo-800 border-indigo-300",
        general: "bg-gray-100 text-gray-800 border-gray-300",
      },
    };
    return (
      colors[type]?.[category] ||
      colors[type]?.general ||
      "bg-gray-50 text-gray-700 border-gray-200"
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto bg-white rounded-lg shadow p-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-[#1B4F8A]">
            Document Analysis
          </h1>
          <button
            onClick={() => navigate("/")}
            className="text-gray-500 hover:text-gray-700"
          >
            ← Back to Dashboard
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6 mb-8">
          {/* Document Text */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Document Text <span className="text-red-500">*</span>
            </label>
            <textarea
              name="text"
              value={formData.text}
              onChange={handleChange}
              placeholder="Paste your document text here for analysis..."
              rows={12}
              className={`w-full border rounded px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.text ? "border-red-500" : "border-gray-300"
              }`}
            />
            <div className="flex justify-between items-center mt-1">
              <div>
                {errors.text && (
                  <p className="text-red-500 text-xs">{errors.text}</p>
                )}
              </div>
              <div className="text-xs text-gray-500">
                {formData.text.length}/10000 characters
              </div>
            </div>
          </div>

          {/* Focus Areas */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Focus Areas (Optional)
            </label>
            <div className="flex flex-wrap gap-3">
              {focusAreaOptions.map((option) => (
                <label key={option.value} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.focusAreas.includes(option.value)}
                    onChange={() => handleFocusAreaChange(option.value)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">
                    {option.label}
                  </span>
                </label>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Select specific areas to focus the analysis on. Leave empty for
              comprehensive analysis.
            </p>
          </div>

          {/* Submit Error */}
          {errors.submit && (
            <div className="p-3 bg-red-50 border border-red-200 rounded">
              <p className="text-red-800 text-sm">{errors.submit}</p>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={analysing}
            className={`w-full py-3 px-4 rounded text-white font-medium ${
              analysing
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-[#1B4F8A] hover:bg-[#15396B] focus:outline-none focus:ring-2 focus:ring-blue-500"
            }`}
          >
            {analysing ? "Analyzing Document..." : "Analyze Document"}
          </button>
        </form>

        {/* Results */}
        {results && (
          <div className="space-y-8 border-t pt-8">
            {/* Summary */}
            <div className="bg-gray-50 rounded-lg p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4">
                Analysis Summary
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {results.metadata.insights_count}
                  </div>
                  <div className="text-sm text-gray-600">Insights Found</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">
                    {results.metadata.risks_count}
                  </div>
                  <div className="text-sm text-gray-600">Risks Identified</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-600">
                    {results.metadata.document_length}
                  </div>
                  <div className="text-sm text-gray-600">
                    Characters Analyzed
                  </div>
                </div>
              </div>
            </div>

            {/* Insights */}
            {results.insights && results.insights.length > 0 && (
              <div>
                <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                  <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium mr-3">
                    Insights
                  </span>
                  Key Findings & Opportunities
                </h2>
                <div className="space-y-4">
                  {results.insights.map((insight, index) => (
                    <div
                      key={index}
                      className="border border-gray-200 rounded-lg p-6"
                    >
                      <div className="flex justify-between items-start mb-3">
                        <h3 className="font-semibold text-gray-800">
                          {insight.title}
                        </h3>
                        <div className="flex gap-2">
                          <span
                            className={`px-2 py-1 text-xs rounded border ${getCategoryColor(insight.category, "insight")}`}
                          >
                            {insight.category}
                          </span>
                          <span
                            className={`px-2 py-1 text-xs rounded border ${getSeverityColor(insight.severity)}`}
                          >
                            {insight.severity}
                          </span>
                        </div>
                      </div>
                      <p className="text-gray-600 mb-3">
                        {insight.description}
                      </p>
                      <div className="flex justify-between items-center text-xs text-gray-500">
                        <span>
                          Confidence: {Math.round(insight.confidence * 100)}%
                        </span>
                        <span>Type: {insight.type}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Risks */}
            {results.risks && results.risks.length > 0 && (
              <div>
                <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                  <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium mr-3">
                    Risks
                  </span>
                  Potential Issues & Threats
                </h2>
                <div className="space-y-4">
                  {results.risks.map((risk, index) => (
                    <div
                      key={index}
                      className="border border-red-200 rounded-lg p-6 bg-red-50"
                    >
                      <div className="flex justify-between items-start mb-3">
                        <h3 className="font-semibold text-red-800">
                          {risk.title}
                        </h3>
                        <div className="flex gap-2">
                          <span
                            className={`px-2 py-1 text-xs rounded border ${getCategoryColor(risk.category, "risk")}`}
                          >
                            {risk.category}
                          </span>
                          <span
                            className={`px-2 py-1 text-xs rounded border ${getSeverityColor(risk.severity)}`}
                          >
                            {risk.severity}
                          </span>
                        </div>
                      </div>
                      <p className="text-red-700 mb-3">{risk.description}</p>
                      <div className="flex justify-between items-center text-xs text-red-600">
                        <span>
                          Confidence: {Math.round(risk.confidence * 100)}%
                        </span>
                        <span>Type: {risk.type}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Metadata */}
            <div className="text-sm text-gray-500 border-t pt-4">
              <p>
                Analysis completed at:{" "}
                {new Date(results.metadata.analysis_timestamp).toLocaleString()}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
