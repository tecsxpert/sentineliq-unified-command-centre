import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import API from '../services/api'

// Dummy record until backend is ready
const DUMMY_RECORD = {
  id: 1,
  title: 'Fix login bug',
  category: 'Bug',
  status: 'In Progress',
  description: 'Users are unable to login with correct credentials. The JWT token is not being generated properly after successful authentication.',
  createdAt: '2026-04-14',
  updatedAt: '2026-04-20',
  score: 72,
  assignedTo: 'Likhith Rao',
  priority: 'High',
}

const statusColors = {
  'Completed': 'bg-green-100 text-green-800',
  'In Progress': 'bg-yellow-100 text-yellow-800',
  'Not Started': 'bg-gray-100 text-gray-700',
}

const priorityColors = {
  'High': 'bg-red-100 text-red-700',
  'Medium': 'bg-orange-100 text-orange-700',
  'Low': 'bg-blue-100 text-blue-700',
}

const scoreColor = (score) => {
  if (score >= 75) return 'text-green-600'
  if (score >= 50) return 'text-yellow-600'
  return 'text-red-600'
}

export default function DetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [record, setRecord] = useState(null)
  const [loading, setLoading] = useState(true)
  const [aiLoading, setAiLoading] = useState(false)
  const [aiResult, setAiResult] = useState(null)
  const [aiError, setAiError] = useState('')

  useEffect(() => {
    fetchRecord()
  }, [id])

  const fetchRecord = async () => {
    setLoading(true)
    try {
      // Uncomment when backend is ready:
      // const res = await API.get(`/api/items/${id}`)
      // setRecord(res.data)

      setTimeout(() => {
        setRecord(DUMMY_RECORD)
        setLoading(false)
      }, 800)
    } catch (error) {
      console.error('Failed to fetch record:', error)
      setLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this record?')) return
    try {
      // await API.delete(`/api/items/${id}`)
      navigate('/')
    } catch (error) {
      console.error('Failed to delete:', error)
    }
  }

  const handleAskAI = async () => {
    setAiLoading(true)
    setAiError('')
    setAiResult(null)
    try {
      // Uncomment when AI service is ready:
      // const res = await API.post('/api/ai/recommend', { itemId: id })
      // setAiResult(res.data)

      // Dummy AI response
      setTimeout(() => {
        setAiResult({
          recommendations: [
            { action_type: 'Fix', description: 'Review JWT token generation logic in AuthService.java', priority: 'High' },
            { action_type: 'Test', description: 'Add unit tests for login edge cases including wrong password', priority: 'Medium' },
            { action_type: 'Monitor', description: 'Add logging to track failed login attempts for security', priority: 'Low' },
          ]
        })
        setAiLoading(false)
      }, 1500)
    } catch (error) {
      setAiError('AI service unavailable. Please try again.')
      setAiLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto space-y-4">
          {Array(5).fill(0).map((_, i) => (
            <div key={i} className="h-12 bg-gray-200 rounded animate-pulse"></div>
          ))}
        </div>
      </div>
    )
  }

  if (!record) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-400 text-lg">Record not found.</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <button
            onClick={() => navigate('/records')}
            className="text-gray-500 hover:text-gray-700 text-sm"
          >
            ← Back to Records
          </button>
          <div className="flex gap-3">
            <button
              onClick={() => navigate(`/edit/${id}`)}
              className="bg-[#1B4F8A] text-white px-4 py-2 rounded hover:bg-blue-800 text-sm"
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 text-sm"
            >
              Delete
            </button>
          </div>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-lg shadow p-8 mb-6">

          {/* Title + Badges */}
          <div className="flex justify-between items-start mb-6">
            <h1 className="text-2xl font-bold text-gray-800">{record.title}</h1>
            <div className="flex gap-2">
              <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColors[record.status]}`}>
                {record.status}
              </span>
              <span className={`px-3 py-1 rounded-full text-xs font-semibold ${priorityColors[record.priority]}`}>
                {record.priority}
              </span>
            </div>
          </div>

          {/* Fields Grid */}
          <div className="grid grid-cols-2 gap-6 mb-6">
            <div>
              <p className="text-xs text-gray-400 uppercase mb-1">Category</p>
              <p className="text-gray-700 font-medium">{record.category}</p>
            </div>
            <div>
              <p className="text-xs text-gray-400 uppercase mb-1">Assigned To</p>
              <p className="text-gray-700 font-medium">{record.assignedTo}</p>
            </div>
            <div>
              <p className="text-xs text-gray-400 uppercase mb-1">Created At</p>
              <p className="text-gray-700 font-medium">{record.createdAt}</p>
            </div>
            <div>
              <p className="text-xs text-gray-400 uppercase mb-1">Updated At</p>
              <p className="text-gray-700 font-medium">{record.updatedAt}</p>
            </div>
            <div>
              <p className="text-xs text-gray-400 uppercase mb-1">Score</p>
              <p className={`text-2xl font-bold ${scoreColor(record.score)}`}>
                {record.score}/100
              </p>
            </div>
          </div>

          {/* Description */}
          <div>
            <p className="text-xs text-gray-400 uppercase mb-2">Description</p>
            <p className="text-gray-700 leading-relaxed">{record.description}</p>
          </div>
        </div>

        {/* AI Analysis Card */}
        <div className="bg-white rounded-lg shadow p-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-gray-700">🤖 AI Analysis</h2>
            <button
              onClick={handleAskAI}
              disabled={aiLoading}
              className="bg-[#1B4F8A] text-white px-4 py-2 rounded hover:bg-blue-800 text-sm disabled:opacity-50"
            >
              {aiLoading ? 'Analysing...' : 'Ask AI'}
            </button>
          </div>

          {/* Loading */}
          {aiLoading && (
            <div className="space-y-3">
              {Array(3).fill(0).map((_, i) => (
                <div key={i} className="h-8 bg-gray-100 rounded animate-pulse"></div>
              ))}
            </div>
          )}

          {/* Error */}
          {aiError && (
            <div className="text-red-500 text-sm flex justify-between items-center">
              <span>{aiError}</span>
              <button onClick={handleAskAI} className="underline">Retry</button>
            </div>
          )}

          {/* AI Result */}
          {aiResult && (
            <div className="space-y-3">
              {aiResult.recommendations.map((rec, i) => (
                <div key={i} className="flex items-start gap-3 p-3 bg-blue-50 rounded">
                  <span className={`px-2 py-1 rounded text-xs font-bold ${
                    rec.priority === 'High' ? 'bg-red-100 text-red-700' :
                    rec.priority === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                    'bg-green-100 text-green-700'
                  }`}>
                    {rec.action_type}
                  </span>
                  <div>
                    <p className="text-sm text-gray-700">{rec.description}</p>
                    <p className="text-xs text-gray-400 mt-1">Priority: {rec.priority}</p>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Default state */}
          {!aiLoading && !aiResult && !aiError && (
            <p className="text-gray-400 text-sm">
              Click "Ask AI" to get intelligent recommendations for this record.
            </p>
          )}
        </div>

      </div>
    </div>
  )
}