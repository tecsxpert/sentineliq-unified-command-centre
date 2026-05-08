export default function ExportButton() {
  const exportCSV = () => {
    const rows = [
      ["Task", "Status"],
      ["Dashboard", "Completed"],
      ["Analytics", "In Progress"],
      ["Streaming", "Completed"],
    ];

    const csvContent = rows
      .map((row) => row.join(","))
      .join("\n");

    const blob = new Blob([csvContent], {
      type: "text/csv",
    });

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download = "analytics-report.csv";

    link.click();
  };

  return (
    <button
      onClick={exportCSV}
      className="bg-blue-700 hover:bg-blue-800 text-white px-5 py-2 rounded-xl"
    >
      Export CSV
    </button>
  );
}