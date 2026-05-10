import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { createRecord, updateRecord, getRecordById } from '../services/api'

const CATEGORIES = ['Infrastructure', 'Security', 'Performance', 'Feature', 'DevOps', 'UX', 'Compliance', 'Data', 'QA', 'Productivity']
const STATUSES   = ['Active', 'In Progress', 'Not Started', 'Blocked', 'Completed']
const PRIORITIES = ['Critical', 'High', 'Medium', 'Low']

export default function FormPage() {
  const navigate    = useNavigate()
  const { id }      = useParams()          // present on /edit/:id, undefined on /create
  const isEdit      = Boolean(id)

  const [formData, setFormData] = useState({
    title:       '',
    category:    '',
    status:      'Active',
    priority:    'Medium',
    assignedTo:  '',
    dueDate:     '',
    description: '',
  })

  const [errors,     setErrors]     = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [loadingRecord, setLoadingRecord] = useState(isEdit)

  // Load existing record when editing
  useEffect(() => {
    if (!isEdit) return
    const load = async () => {
      try {
        const record = await getRecordById(id)
        setFormData({
          title:       record.title       || '',
          category:    record.category    || '',
          status:      record.status      || 'Active',
          priority:    record.priority    || 'Medium',
          assignedTo:  record.assignedTo  || '',
          dueDate:     record.dueDate     || '',
          description: record.description || '',
        })
      } catch (err) {
        console.error('Failed to load record:', err)
      } finally {
        setLoadingRecord(false)
      }
    }
    load()
  }, [id])

  const validate = () => {
    const e = {}
    if (!formData.title.trim())       e.title       = 'Title is required'
    if (!formData.category.trim())    e.category    = 'Category is required'
    if (!formData.description.trim()) e.description = 'Description is required'
    if (!formData.assignedTo.trim())  e.assignedTo  = 'Assigned To is required'
    return e
  }

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }))
    setErrors(prev => ({ ...prev, [e.target.name]: '' }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const validationErrors = validate()
    if (Object.keys(validationErrors).length > 0) { setErrors(validationErrors); return }

    setSubmitting(true)
    try {
      if (isEdit) {
        await updateRecord(id, formData)
        navigate(`/records/${id}`)
      } else {
        const created = await createRecord(formData)
        navigate(`/records/${created.id}`)
      }
    } catch (err) {
      console.error('Failed to save record:', err)
      setSubmitting(false)
    }
  }

  const inputClass = (field) =>
    `w-full border rounded px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[44px] ${
      errors[field] ? 'border-red-500' : 'border-gray-300'
    }`

  if (loadingRecord) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-400 text-sm animate-pulse">Loading record...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 sm:p-6 lg:p-8">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow p-4 sm:p-6 lg:p-8">

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2 mb-6">
          <h1 className="text-xl sm:text-2xl font-bold text-[#1B4F8A]">
            {isEdit ? 'Edit Record' : 'Create New Record'}
          </h1>
          <button onClick={() => navigate(isEdit ? `/records/${id}` : '/records')}
            className="self-start sm:self-auto text-gray-500 hover:text-gray-700 text-sm min-h-[44px] flex items-center">
            ← Back
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-5">

          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Title <span className="text-red-500">*</span>
            </label>
            <input type="text" name="title" value={formData.title} onChange={handleChange}
              placeholder="Enter title" className={inputClass('title')} />
            {errors.title && <p className="text-red-500 text-xs mt-1">{errors.title}</p>}
          </div>

          {/* Category + Priority — side by side */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Category <span className="text-red-500">*</span>
              </label>
              <select name="category" value={formData.category} onChange={handleChange}
                className={inputClass('category')}>
                <option value="">Select category</option>
                {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
              {errors.category && <p className="text-red-500 text-xs mt-1">{errors.category}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
              <select name="priority" value={formData.priority} onChange={handleChange}
                className={inputClass('priority')}>
                {PRIORITIES.map(p => <option key={p} value={p}>{p}</option>)}
              </select>
            </div>
          </div>

          {/* Status + Assigned To — side by side */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select name="status" value={formData.status} onChange={handleChange}
                className={inputClass('status')}>
                {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Assigned To <span className="text-red-500">*</span>
              </label>
              <input type="text" name="assignedTo" value={formData.assignedTo} onChange={handleChange}
                placeholder="e.g. Arjun Mehta" className={inputClass('assignedTo')} />
              {errors.assignedTo && <p className="text-red-500 text-xs mt-1">{errors.assignedTo}</p>}
            </div>
          </div>

          {/* Due Date */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
            <input type="date" name="dueDate" value={formData.dueDate} onChange={handleChange}
              className={inputClass('dueDate')} />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description <span className="text-red-500">*</span>
            </label>
            <textarea name="description" value={formData.description} onChange={handleChange}
              placeholder="Enter a clear description of this record..." rows={4}
              className={`w-full border rounded px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.description ? 'border-red-500' : 'border-gray-300'
              }`} />
            {errors.description && <p className="text-red-500 text-xs mt-1">{errors.description}</p>}
          </div>

          {/* Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 pt-2">
            <button type="submit" disabled={submitting}
              className="w-full sm:w-auto bg-[#1B4F8A] text-white px-6 py-2 rounded hover:bg-blue-800 disabled:opacity-50 min-h-[44px]">
              {submitting ? 'Saving...' : isEdit ? 'Save Changes' : 'Create Record'}
            </button>
            <button type="button" onClick={() => navigate(isEdit ? `/records/${id}` : '/records')}
              className="w-full sm:w-auto border border-gray-300 text-gray-600 px-6 py-2 rounded hover:bg-gray-50 min-h-[44px]">
              Cancel
            </button>
          </div>

        </form>
      </div>
    </div>
  )
}