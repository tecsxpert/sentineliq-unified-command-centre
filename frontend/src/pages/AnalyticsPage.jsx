import { useEffect, useState } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer,
  LineChart, Line,
  PieChart, Pie, Cell
} from 'recharts'
import { getStats } from '../services/api'

const PIE_COLORS = {
  'Active':      '#3b82f6',
  'In Progress': '#eab308',
  'Completed':   '#22c55e',
  'Blocked':     '#ef4444',
}

// Line data by period — built from mockData monthly trend
const LINE_DATA = {
  '30days': [
    { date: 'Apr 1',  records: 3  },
    { date: 'Apr 7',  records: 7  },
    { date: 'Apr 14', records: 14 },
    { date: 'Apr 21', records: 22 },
    { date: 'Apr 28', records: 27 },
    { date: 'May 5',  records: 30 },
  ],
  '3months': [
    { date: 'Feb', records: 9  },
    { date: 'Mar', records: 14 },
    { date: 'Apr', records: 30 },
  ],
  '6months': [
    { date: 'Nov', records: 3  },
    { date: 'Dec', records: 5  },
    { date: 'Jan', records: 7  },
    { date: 'Feb', records: 9  },
    { date: 'Mar', records: 14 },
    { date: 'Apr', records: 30 },
  ],
}

export default function AnalyticsPage() {
  const [period,   setPeriod]   = useState('6months')
  const [barData,  setBarData]  = useState([])
  const [lineData, setLineData] = useState([])
  const [pieData,  setPieData]  = useState([])
  const [loading,  setLoading]  = useState(true)

  useEffect(() => { fetchAnalytics() }, [period])

  const fetchAnalytics = async () => {
    setLoading(true)
    try {
      const stats = await getStats()

      // Bar — records by category
      const bar = Object.entries(stats.byCategory).map(([name, count]) => ({ name, count }))
      setBarData(bar)

      // Line — from period selector
      setLineData(LINE_DATA[period])

      // Pie — by status from real stats
      const pie = Object.entries(stats.byStatus).map(([name, value]) => ({
        name, value, color: PIE_COLORS[name] || '#9ca3af'
      }))
      setPieData(pie)
    } catch (error) {
      console.error('Failed to fetch analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  const RADIAN = Math.PI / 180
  const renderLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5
    const x = cx + radius * Math.cos(-midAngle * RADIAN)
    const y = cy + radius * Math.sin(-midAngle * RADIAN)
    return (
      <text x={x} y={y} fill="white" textAnchor="middle" dominantBaseline="central" fontSize={12}>
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    )
  }

  const ChartSkeleton = () => (
    <div className="h-64 bg-gray-100 rounded animate-pulse" />
  )

  return (
    <div className="min-h-screen bg-gray-50 p-4 sm:p-8">

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-[#1B4F8A]">Analytics</h1>
          <p className="text-sm text-gray-500 mt-1">Visual breakdown of all records</p>
        </div>
        <div className="flex gap-2">
          {['30days', '3months', '6months'].map((p) => (
            <button key={p} onClick={() => setPeriod(p)}
              className={`px-4 py-2 rounded text-sm font-medium ${
                period === p
                  ? 'bg-[#1B4F8A] text-white'
                  : 'border border-gray-300 text-gray-600 hover:bg-gray-50'
              }`}>
              {p === '30days' ? 'Last 30 Days' : p === '3months' ? '3 Months' : '6 Months'}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">

        {/* Bar Chart — by Category */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-700 mb-6">Records by Category</h2>
          {loading ? <ChartSkeleton /> : (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="count" name="Records" fill="#1B4F8A" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Line Chart — over time */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-700 mb-6">Records Over Time</h2>
          {loading ? <ChartSkeleton /> : (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={lineData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Line type="monotone" dataKey="records" stroke="#1B4F8A"
                  strokeWidth={2} dot={{ fill: '#1B4F8A', r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Pie Chart — by Status */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-700 mb-6">Records by Status</h2>
          {loading ? <ChartSkeleton /> : (
            <div className="flex flex-col sm:flex-row items-center justify-center gap-8 sm:gap-12">
              <PieChart width={280} height={280}>
                <Pie data={pieData} cx={140} cy={140} outerRadius={120}
                  dataKey="value" labelLine={false} label={renderLabel}>
                  {pieData.map((entry, i) => (
                    <Cell key={i} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
              <div className="space-y-3">
                {pieData.map((entry, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <div className="w-4 h-4 rounded-full flex-shrink-0" style={{ backgroundColor: entry.color }} />
                    <span className="text-sm text-gray-600">
                      {entry.name} — <strong>{entry.value}</strong>
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  )
}