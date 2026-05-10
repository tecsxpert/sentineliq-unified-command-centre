import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { DetailSkeleton } from '../components/Skeleton'
import { getRecordById, deleteRecord, getAiRecommendations, getAuditLog } from '../services/api'

const statusColors = {
  'Completed':   'bg-green-100 text-green-800',
  'In Progress': 'bg-yellow-100 text-yellow-800',
  'Active':      'bg-blue-100 text-blue-800',
  'Blocked':     'bg-red-100 text-red-800',
  'Not Started': 'bg-gray-100 text-gray-700',
}

const priorityColors = {
  'Critical': 'bg-red-100 text-red-700',
  'High':     'bg-orange-100 text-orange-700',
  'Medium':   'bg-yellow-100 text-yellow-700',
  'Low':      'bg-blue-100 text-blue-700',
}

const scoreColor = (score) => {
  if (score >= 80) return 'text-green-600'
  if (score >= 60) return 'text-yellow-600'
  return 'text-red-600'
}

export default function DetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [record,    setRecord]    = useState(null)
  const [auditLog,  setAuditLog]  = useState([])
  const [loading,   setLoading]   = useState(true)
  const [deleting,  setDeleting]  = useState(false)

  const [aiLoading, setAiLoading] = useState(false)
  const [aiResult,  setAiResult]  = useState(null)
  const [aiError,   setAiError]   = useState('')

  useEffect(() => { fetchRecord() }, [id])

  const fetchRecord = async () => {
    setLoading(true)
    try {
      const [rec, log] = await Promise.all([
        getRecordById(id),
        getAuditLog(id),
      ])
      setRecord(rec)
      setAuditLog(log)
    } catch (error) {
      console.error('Failed to fetch record:', error)
      setRecord(null)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this record?')) return
    setDeleting(true)
    try {
      await deleteRecord(id)
      navigate('/records')
    } catch (error) {
      console.error('Failed to delete:', error)
      setDeleting(false)
    }
  }

  const handleAskAI = async () => {
    setAiLoading(true)
    setAiError('')
    setAiResult(null)
    try {
      const result = await getAiRecommendations(id)
      setAiResult(result)
    } catch (error) {
      setAiError('AI service unavailable. Please try again.')
    } finally {
      setAiLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-4 sm:p-8">
        <div className="max-w-4xl mx-auto"><DetailSkeleton /></div>
      </div>
    )
  }

  if (!record) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="text-center">
          <p className="text-gray-400 text-lg mb-4">Record not found.</p>
          <button onClick={() => navigate('/records')}
            className="text-[#1B4F8A] underline text-sm">← Back to Records</button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 sm:p-6 lg:p-8">
      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 mb-6">
          <button onClick={() => navigate('/records')}
            className="self-start text-gray-500 hover:text-gray-700 text-sm min-h-[44px] flex items-center">
            ← Back to Records
          </button>
          <div className="flex gap-2 sm:gap-3">
            <button onClick={() => navigate(`/edit/${id}`)}
              className="flex-1 sm:flex-none bg-[#1B4F8A] text-white px-4 py-2 rounded hover:bg-blue-800 text-sm min-h-[44px]">
              Edit
            </button>
            <button onClick={handleDelete} disabled={deleting}
              className="flex-1 sm:flex-none bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 text-sm min-h-[44px] disabled:opacity-50">
              {deleting ? 'Deleting…' : 'Delete'}
            </button>
          </div>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-lg shadow p-4 sm:p-6 lg:p-8 mb-6">

          {/* Title + Badges */}
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-3 mb-6">
            <h1 className="text-xl sm:text-2xl font-bold text-gray-800">{record.title}</h1>
            <div className="flex gap-2 flex-wrap">
              <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColors[record.status] || 'bg-gray-100 text-gray-700'}`}>
                {record.status}
              </span>
              <span className={`px-3 py-1 rounded-full text-xs font-semibold ${priorityColors[record.priority] || 'bg-gray-100 text-gray-700'}`}>
                {record.priority}
              </span>
            </div>
          </div>

          {/* Fields Grid */}
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
              <p className="text-xs text-gray-400 uppercase mb-1">Due Date</p>
              <p className="text-gray-700 font-medium">{record.dueDate || '—'}</p>
            </div>
            <div>
              <p className="text-xs text-gray-400 uppercase mb-1">Score</p>
              <p className={`text-2xl font-bold ${scoreColor(record.score)}`}>{record.score}/100</p>
            </div>
            <div>
              <p className="text-xs text-gray-400 uppercase mb-1">Created At</p>
              <p className="text-gray-700 font-medium">{record.createdAt?.split('T')[0]}</p>
            </div>
            <div>
              <p className="text-xs text-gray-400 uppercase mb-1">Updated At</p>
              <p className="text-gray-700 font-medium">{record.updatedAt?.split('T')[0]}</p>
            </div>
          </div>

          {/* Tags */}
          {record.tags?.length > 0 && (
            <div className="mb-6">
              <p className="text-xs text-gray-400 uppercase mb-2">Tags</p>
              <div className="flex flex-wrap gap-2">
                {record.tags.map(tag => (
                  <span key={tag} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                    #{tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Description */}
          <div>
            <p className="text-xs text-gray-400 uppercase mb-2">Description</p>
            <p className="text-gray-700 leading-relaxed text-sm sm:text-base">{record.description}</p>
          </div>
        </div>

        {/* AI Analysis Card */}
        <div className="bg-white rounded-lg shadow p-4 sm:p-6 lg:p-8 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-base sm:text-lg font-semibold text-gray-700">🤖 AI Analysis</h2>
            <button onClick={handleAskAI} disabled={aiLoading}
              className="bg-[#1B4F8A] text-white px-3 sm:px-4 py-2 rounded hover:bg-blue-800 text-sm disabled:opacity-50 min-h-[44px]">
              {aiLoading ? 'Analysing...' : 'Ask AI'}
            </button>
          </div>

          {/* Existing AI analysis from record */}
          {!aiResult && !aiLoading && !aiError && record.aiAnalysis && (
            <div className="p-3 bg-gray-50 rounded border-l-4 border-[#1B4F8A] mb-4">
              <p className="text-xs text-gray-400 uppercase mb-1">Last Analysis</p>
              <p className="text-sm text-gray-700">{record.aiAnalysis}</p>
            </div>
          )}

          {aiLoading && (
            <div className="space-y-3">
              {[1,2,3].map(i => (
                <div key={i} className="h-8 bg-gray-100 rounded animate-pulse" />
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
                    rec.priority === 'HIGH'   ? 'bg-red-100 text-red-700' :
                    rec.priority === 'MEDIUM' ? 'bg-yellow-100 text-yellow-700' :
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
              <p className="text-xs text-gray-400 mt-2">
                Model: {aiResult.meta?.model_used} · Confidence: {Math.round((aiResult.meta?.confidence || 0) * 100)}% · {aiResult.meta?.response_time_ms}ms
              </p>
            </div>
          )}

          {!aiLoading && !aiResult && !aiError && !record.aiAnalysis && (
            <p className="text-gray-400 text-sm">
              Click "Ask AI" to get intelligent recommendations for this record.
            </p>
          )}
        </div>

        {/* Audit Log Card */}
        {auditLog.length > 0 && (
          <div className="bg-white rounded-lg shadow p-4 sm:p-6 lg:p-8">
            <h2 className="text-base sm:text-lg font-semibold text-gray-700 mb-4">📋 Audit Log</h2>
            <div className="space-y-3">
              {auditLog.map((log, i) => (
                <div key={i} className="flex items-start gap-3 text-sm border-b pb-3 last:border-0 last:pb-0">
                  <span className={`px-2 py-0.5 rounded text-xs font-bold flex-shrink-0 ${
                    log.action === 'CREATE' ? 'bg-green-100 text-green-700' :
                    log.action === 'DELETE' ? 'bg-red-100 text-red-700' :
                                              'bg-yellow-100 text-yellow-700'
                  }`}>
                    {log.action}
                  </span>
                  <div className="flex-1">
                    <p className="text-gray-700">
                      <span className="font-medium">{log.performedBy}</span>
                      {log.oldValue && log.newValue && (
                        <span className="text-gray-500"> · {log.oldValue} → {log.newValue}</span>
                      )}
                      {!log.oldValue && log.newValue && (
                        <span className="text-gray-500"> · {log.newValue}</span>
                      )}
                    </p>
                    <p className="text-xs text-gray-400 mt-0.5">
                      {log.timestamp ? new Date(log.timestamp).toLocaleString() : ''}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

      </div>
    </div>
  )
}