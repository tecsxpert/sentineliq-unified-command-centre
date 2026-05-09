import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { DetailSkeleton } from '../components/Skeleton'

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

  useEffect(() => { fetchRecord() }, [id])

  const fetchRecord = async () => {
    setLoading(true)
    try {
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
      <div className="min-h-screen bg-gray-50 p-4 sm:p-8">
        <div className="max-w-4xl mx-auto">
          <DetailSkeleton />
        </div>
      </div>
    )
  }

  if (!record) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <p className="text-gray-400 text-lg">Record not found.</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 sm:p-6 lg:p-8">
      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 mb-6">
          <button
            onClick={() => navigate('/records')}
            className="self-start text-gray-500 hover:text-gray-700 text-sm min-h-[44px] flex items-center"
          >
            ← Back to Records
          </button>
          <div className="flex gap-2 sm:gap-3">
            <button
              onClick={() => navigate(`/edit/${id}`)}
              className="flex-1 sm:flex-none bg-[#1B4F8A] text-white px-4 py-2 rounded hover:bg-blue-800 text-sm min-h-[44px]"
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              className="flex-1 sm:flex-none bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 text-sm min-h-[44px]"
            >
              Delete
            </button>
          </div>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-lg shadow p-4 sm:p-6 lg:p-8 mb-6">

          {/* Title + Badges */}
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-3 mb-6">
            <h1 className="text-xl sm:text-2xl font-bold text-gray-800">{record.title}</h1>
            <div className="flex gap-2 flex-wrap">
              <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColors[record.status]}`}>
                {record.status}
              </span>
              <span className={`px-3 py-1 rounded-full text-xs font-semibold ${priorityColors[record.priority]}`}>
                {record.priority}
              </span>
            </div>
          </div>

          {/* Fields Grid — 1 col on mobile, 2 on tablet+ */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6 mb-6">
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
            <p className="text-gray-700 leading-relaxed text-sm sm:text-base">{record.description}</p>
          </div>
        </div>

        {/* AI Analysis Card */}
        <div className="bg-white rounded-lg shadow p-4 sm:p-6 lg:p-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-base sm:text-lg font-semibold text-gray-700">🤖 AI Analysis</h2>
            <button
              onClick={handleAskAI}
              disabled={aiLoading}
              className="bg-[#1B4F8A] text-white px-3 sm:px-4 py-2 rounded hover:bg-blue-800 text-sm disabled:opacity-50 min-h-[44px]"
            >
              {aiLoading ? 'Analysing...' : 'Ask AI'}
            </button>
          </div>

          {aiLoading && (
            <div className="space-y-3">
              {Array(3).fill(0).map((_, i) => (
                <div key={i} className="h-8 bg-gray-100 rounded animate-pulse"></div>
              ))}
            </div>
          )}

          {aiError && (
            <div className="text-red-500 text-sm flex justify-between items-center">
              <span>{aiError}</span>
              <button onClick={handleAskAI} className="underline min-h-[44px]">Retry</button>
            </div>
          )}

          {aiResult && (
            <div className="space-y-3">
              {aiResult.recommendations.map((rec, i) => (
                <div key={i} className="flex flex-col sm:flex-row sm:items-start gap-2 sm:gap-3 p-3 bg-blue-50 rounded">
                  <span className={`self-start px-2 py-1 rounded text-xs font-bold whitespace-nowrap ${
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