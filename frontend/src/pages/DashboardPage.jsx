import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import API from "../services/api";

// Dummy stats until backend is ready
const DUMMY_STATS = {
  total: 24,
  completed: 8,
  inProgress: 10,
  notStarted: 6,
};

const DUMMY_CHART_DATA = [
  { name: "Bug", completed: 3, inProgress: 2, notStarted: 1 },
  { name: "Feature", completed: 2, inProgress: 4, notStarted: 2 },
  { name: "DevOps", completed: 1, inProgress: 2, notStarted: 1 },
  { name: "Security", completed: 1, inProgress: 1, notStarted: 1 },
  { name: "Docs", completed: 1, inProgress: 1, notStarted: 1 },
];

export default function DashboardPage() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    setLoading(true);
    try {
      // Uncomment when backend is ready:
      // const res = await API.get('/api/items/stats')
      // setStats(res.data)
      // setChartData(res.data.byCategory)

      setTimeout(() => {
        setStats(DUMMY_STATS);
        setChartData(DUMMY_CHART_DATA);
        setLoading(false);
      }, 800);
    } catch (error) {
      console.error("Failed to fetch stats:", error);
      setLoading(false);
    }
  };

  const KPICard = ({ title, value, color, icon }) => (
    <div className={`bg-white rounded-lg shadow p-6 border-l-4 ${color}`}>
      {loading ? (
        <div className="h-8 bg-gray-200 rounded animate-pulse w-16 mb-2"></div>
      ) : (
        <p className="text-3xl font-bold text-gray-800">{value}</p>
      )}
      <p className="text-sm text-gray-500 mt-1">{title}</p>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-[#1B4F8A]">Dashboard</h1>
          <p className="text-sm text-gray-500 mt-1">Overview of all records</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => navigate("/reports")}
            className="bg-[#1B4F8A] text-white px-4 py-2 rounded hover:bg-[#15396B] text-sm"
          >
            Generate AI Report
          </button>
          <button
            onClick={() => navigate("/analyse")}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 text-sm"
          >
            Analyze Document
          </button>
          <button
            onClick={() => navigate("/records")}
            className="border border-gray-300 text-gray-600 px-4 py-2 rounded hover:bg-gray-50 text-sm"
          >
            View All Records
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <KPICard
          title="Total Records"
          value={stats?.total}
          color="border-blue-500"
        />
        <KPICard
          title="Completed"
          value={stats?.completed}
          color="border-green-500"
        />
        <KPICard
          title="In Progress"
          value={stats?.inProgress}
          color="border-yellow-500"
        />
        <KPICard
          title="Not Started"
          value={stats?.notStarted}
          color="border-gray-400"
        />
      </div>

      {/* Bar Chart */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-700 mb-6">
          Records by Category
        </h2>
        {loading ? (
          <div className="h-64 bg-gray-100 rounded animate-pulse"></div>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="completed" name="Completed" fill="#22c55e" />
              <Bar dataKey="inProgress" name="In Progress" fill="#eab308" />
              <Bar dataKey="notStarted" name="Not Started" fill="#9ca3af" />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
