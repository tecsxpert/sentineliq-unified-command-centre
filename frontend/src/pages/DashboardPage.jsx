import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend
} from 'recharts'
import { CardGridSkeleton, ChartSkeleton } from '../components/Skeleton'
import { getStats } from '../services/api'   // ← ONLY change from before

export default function DashboardPage() {
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [chartData, setChartData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    setLoading(true)
    try {
      const data = await getStats()
      setStats(data)

      // Build chart data from byCategory + byStatus breakdown
      const chartRows = Object.entries(data.byCategory).map(([name, total]) => ({
        name,
        Total: total,
      }))
      setChartData(chartRows)
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const KPICard = ({ title, value, color }) => (
    <div className={`bg-white rounded-lg shadow p-4 sm:p-6 border-l-4 ${color}`}>
      {loading ? (
        <div className="h-8 bg-gray-200 rounded animate-pulse w-16 mb-2"></div>
      ) : (
        <p className="text-2xl sm:text-3xl font-bold text-gray-800">{value}</p>
      )}
      <p className="text-xs sm:text-sm text-gray-500 mt-1">{title}</p>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-50 p-4 sm:p-6 lg:p-8">

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 mb-6 sm:mb-8">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-[#1B4F8A]">Dashboard</h1>
          <p className="text-xs sm:text-sm text-gray-500 mt-1">Overview of all records</p>
        </div>
        <button
          onClick={() => navigate('/records')}
          className="self-start sm:self-auto border border-gray-300 text-gray-600 px-4 py-2 rounded hover:bg-gray-50 text-sm min-h-[44px]"
        >
          View All Records
        </button>
      </div>

      {/* KPI Cards */}
      {loading ? (
        <div className="mb-6 sm:mb-8">
          <CardGridSkeleton cards={4} />
        </div>
      ) : (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6 mb-6 sm:mb-8">
          <KPICard title="Total Records"  value={stats?.total}      color="border-blue-500"   />
          <KPICard title="Active"         value={stats?.active}     color="border-indigo-500" />
          <KPICard title="Completed"      value={stats?.completed}  color="border-green-500"  />
          <KPICard title="Blocked"        value={stats?.blocked}    color="border-red-500"    />
        </div>
      )}

      {/* Bar Chart — records by category */}
      <div className="bg-white rounded-lg shadow p-4 sm:p-6 mb-6">
        <h2 className="text-base sm:text-lg font-semibold text-gray-700 mb-4 sm:mb-6">
          Records by Category
        </h2>
        {loading ? (
          <ChartSkeleton height={250} />
        ) : (
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={chartData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Legend wrapperStyle={{ fontSize: '12px' }} />
              <Bar dataKey="Total" fill="#1B4F8A" />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* Monthly Trend Chart */}
      <div className="bg-white rounded-lg shadow p-4 sm:p-6">
        <h2 className="text-base sm:text-lg font-semibold text-gray-700 mb-4 sm:mb-6">
          Monthly Trend
        </h2>
        {loading ? (
          <ChartSkeleton height={200} />
        ) : (
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={stats?.monthlyTrend} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="count" name="Records" fill="#22c55e" />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>

    </div>
  )
}