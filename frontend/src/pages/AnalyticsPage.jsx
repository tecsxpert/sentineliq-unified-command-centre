import { useEffect, useState } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend,
  LineChart, Line,
  PieChart, Pie, Cell
} from 'recharts'
import API from '../services/api'

// Dummy data
const DUMMY_BAR_DATA = [
  { name: 'Bug', count: 6 },
  { name: 'Feature', count: 8 },
  { name: 'DevOps', count: 4 },
  { name: 'Security', count: 3 },
  { name: 'Docs', count: 3 },
]

const DUMMY_LINE_DATA = {
  '30days': [
    { date: 'Apr 1', records: 2 },
    { date: 'Apr 7', records: 5 },
    { date: 'Apr 14', records: 8 },
    { date: 'Apr 21', records: 12 },
    { date: 'Apr 28', records: 18 },
    { date: 'May 5', records: 24 },
  ],
  '3months': [
    { date: 'Feb', records: 5 },
    { date: 'Mar', records: 12 },
    { date: 'Apr', records: 24 },
  ],
  '6months': [
    { date: 'Nov', records: 2 },
    { date: 'Dec', records: 5 },
    { date: 'Jan', records: 8 },
    { date: 'Feb', records: 12 },
    { date: 'Mar', records: 18 },
    { date: 'Apr', records: 24 },
  ],
}

const DUMMY_PIE_DATA = [
  { name: 'Completed', value: 8, color: '#22c55e' },
  { name: 'In Progress', value: 10, color: '#eab308' },
  { name: 'Not Started', value: 6, color: '#9ca3af' },
]

export default function AnalyticsPage() {
  const [period, setPeriod] = useState('6months')
  const [barData, setBarData] = useState([])
  const [lineData, setLineData] = useState([])
  const [pieData, setPieData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [period])

  const fetchAnalytics = async () => {
    setLoading(true)
    try {
      // Uncomment when backend is ready:
      // const res = await API.get(`/api/items/analytics?period=${period}`)
      // setBarData(res.data.byCategory)
      // setLineData(res.data.overTime)
      // setPieData(res.data.byStatus)

      setTimeout(() => {
        setBarData(DUMMY_BAR_DATA)
        setLineData(DUMMY_LINE_DATA[period])
        setPieData(DUMMY_PIE_DATA)
        setLoading(false)
      }, 800)
    } catch (error) {
      console.error('Failed to fetch analytics:', error)
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

  return (
    <div className="min-h-screen bg-gray-50 p-8">

      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-[#1B4F8A]">Analytics</h1>
          <p className="text-sm text-gray-500 mt-1">Visual breakdown of all records</p>
        </div>

        {/* Period Selector */}
        <div className="flex gap-2">
          {['30days', '3months', '6months'].map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-4 py-2 rounded text-sm font-medium ${
                period === p
                  ? 'bg-[#1B4F8A] text-white'
                  : 'border border-gray-300 text-gray-600 hover:bg-gray-50'
              }`}
            >
              {p === '30days' ? 'Last 30 Days' : p === '3months' ? '3 Months' : '6 Months'}
            </button>
          ))}
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 gap-6">

        {/* Bar Chart — by Category */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-700 mb-6">Records by Category</h2>
          {loading ? (
            <div className="h-64 bg-gray-100 rounded animate-pulse"></div>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" name="Records" fill="#1B4F8A" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Line Chart — over time */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-700 mb-6">Records Over Time</h2>
          {loading ? (
            <div className="h-64 bg-gray-100 rounded animate-pulse"></div>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={lineData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="records"
                  stroke="#1B4F8A"
                  strokeWidth={2}
                  dot={{ fill: '#1B4F8A', r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Pie Chart — by Status */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-700 mb-6">Records by Status</h2>
          {loading ? (
            <div className="h-64 bg-gray-100 rounded animate-pulse"></div>
          ) : (
            <div className="flex items-center justify-center gap-12">
              <PieChart width={300} height={300}>
                <Pie
                  data={pieData}
                  cx={150}
                  cy={150}
                  outerRadius={120}
                  dataKey="value"
                  labelLine={false}
                  label={renderLabel}
                >
                  {pieData.map((entry, index) => (
                    <Cell key={index} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>

              {/* Legend */}
              <div className="space-y-3">
                {pieData.map((entry, index) => (
                  <div key={index} className="flex items-center gap-2">
                    <div
                      className="w-4 h-4 rounded-full"
                      style={{ backgroundColor: entry.color }}
                    ></div>
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