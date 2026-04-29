import { useEffect, useState, useCallback, useRef } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import API from '../services/api'

const DUMMY_RECORDS = [
  { id: 1, title: 'Fix login bug', category: 'Bug', status: 'In Progress', priority: 'High', createdAt: '2026-04-14' },
  { id: 2, title: 'Add dark mode', category: 'Feature', status: 'Not Started', priority: 'Medium', createdAt: '2026-04-15' },
  { id: 3, title: 'Setup CI/CD pipeline', category: 'DevOps', status: 'Completed', priority: 'High', createdAt: '2026-04-10' },
  { id: 4, title: 'Fix XSS vulnerability', category: 'Security', status: 'In Progress', priority: 'High', createdAt: '2026-04-18' },
  { id: 5, title: 'Update API docs', category: 'Docs', status: 'Completed', priority: 'Low', createdAt: '2026-04-12' },
  { id: 6, title: 'Add pagination to API', category: 'Feature', status: 'Not Started', priority: 'Medium', createdAt: '2026-04-20' },
  { id: 7, title: 'Fix memory leak', category: 'Bug', status: 'Completed', priority: 'High', createdAt: '2026-04-08' },
  { id: 8, title: 'Write unit tests', category: 'Docs', status: 'In Progress', priority: 'Low', createdAt: '2026-04-22' },
]

const statusColors = {
  'Completed': 'bg-green-100 text-green-800',
  'In Progress': 'bg-yellow-100 text-yellow-800',
  'Not Started': 'bg-gray-100 text-gray-700',
}

export default function ListPage() {
  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams()

  // Read initial values from URL
  const [searchText, setSearchText] = useState(searchParams.get('search') || '')
  const [statusFilter, setStatusFilter] = useState(searchParams.get('status') || '')
  const [dateFrom, setDateFrom] = useState(searchParams.get('dateFrom') || '')
  const [dateTo, setDateTo] = useState(searchParams.get('dateTo') || '')
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [sortField, setSortField] = useState('createdAt')
  const [sortDir, setSortDir] = useState('desc')
  const [page, setPage] = useState(1)
  const ITEMS_PER_PAGE = 5

  const debounceRef = useRef(null)

  // Debounced search — fires 300ms after user stops typing
  const handleSearchChange = (e) => {
    const value = e.target.value
    setSearchText(value)
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      updateURL({ search: value })
    }, 300)
  }

  const handleStatusChange = (e) => {
    const value = e.target.value
    setStatusFilter(value)
    updateURL({ status: value })
  }

  const handleDateFrom = (e) => {
    const value = e.target.value
    setDateFrom(value)
    updateURL({ dateFrom: value })
  }

  const handleDateTo = (e) => {
    const value = e.target.value
    setDateTo(value)
    updateURL({ dateTo: value })
  }

  const updateURL = (newParams) => {
    const current = {
      search: searchParams.get('search') || '',
      status: searchParams.get('status') || '',
      dateFrom: searchParams.get('dateFrom') || '',
      dateTo: searchParams.get('dateTo') || '',
      ...newParams,
    }
    // Remove empty params
    const cleaned = Object.fromEntries(
      Object.entries(current).filter(([_, v]) => v !== '')
    )
    setSearchParams(cleaned)
  }

  const clearFilters = () => {
    setSearchText('')
    setStatusFilter('')
    setDateFrom('')
    setDateTo('')
    setSearchParams({})
  }

  // Filter + sort logic
  useEffect(() => {
    setLoading(true)
    setTimeout(() => {
      let filtered = [...DUMMY_RECORDS]

      if (searchText) {
        filtered = filtered.filter(r =>
          r.title.toLowerCase().includes(searchText.toLowerCase()) ||
          r.category.toLowerCase().includes(searchText.toLowerCase())
        )
      }

      if (statusFilter) {
        filtered = filtered.filter(r => r.status === statusFilter)
      }

      if (dateFrom) {
        filtered = filtered.filter(r => r.createdAt >= dateFrom)
      }

      if (dateTo) {
        filtered = filtered.filter(r => r.createdAt <= dateTo)
      }

      filtered.sort((a, b) => {
        if (a[sortField] < b[sortField]) return sortDir === 'asc' ? -1 : 1
        if (a[sortField] > b[sortField]) return sortDir === 'asc' ? 1 : -1
        return 0
      })

      setRecords(filtered)
      setPage(1)
      setLoading(false)
    }, 300)
  }, [searchText, statusFilter, dateFrom, dateTo, sortField, sortDir])

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDir('asc')
    }
  }

  const paginated = records.slice((page - 1) * ITEMS_PER_PAGE, page * ITEMS_PER_PAGE)
  const totalPages = Math.ceil(records.length / ITEMS_PER_PAGE)

  const hasActiveFilters = searchText || statusFilter || dateFrom || dateTo

  return (
    <div className="min-h-screen bg-gray-50 p-8">

      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-[#1B4F8A]">All Records</h1>
          <p className="text-sm text-gray-500 mt-1">{records.length} record{records.length !== 1 ? 's' : ''} found</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => navigate('/')}
            className="border border-gray-300 text-gray-600 px-4 py-2 rounded hover:bg-gray-50 text-sm"
          >
            Dashboard
          </button>
          <button
            onClick={() => navigate('/create')}
            className="bg-[#1B4F8A] text-white px-4 py-2 rounded hover:bg-blue-800 text-sm"
          >
            + New Record
          </button>
        </div>
      </div>

      {/* Search + Filter Bar */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="flex flex-wrap gap-3 items-end">

          {/* Text Search */}
          <div className="flex-1 min-w-[200px]">
            <label className="text-xs text-gray-400 uppercase mb-1 block">Search</label>
            <input
              type="text"
              value={searchText}
              onChange={handleSearchChange}
              placeholder="Search by title or category..."
              className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>

          {/* Status Dropdown */}
          <div className="min-w-[160px]">
            <label className="text-xs text-gray-400 uppercase mb-1 block">Status</label>
            <select
              value={statusFilter}
              onChange={handleStatusChange}
              className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300"
            >
              <option value="">All Statuses</option>
              <option value="Completed">Completed</option>
              <option value="In Progress">In Progress</option>
              <option value="Not Started">Not Started</option>
            </select>
          </div>

          {/* Date From */}
          <div className="min-w-[150px]">
            <label className="text-xs text-gray-400 uppercase mb-1 block">Date From</label>
            <input
              type="date"
              value={dateFrom}
              onChange={handleDateFrom}
              className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>

          {/* Date To */}
          <div className="min-w-[150px]">
            <label className="text-xs text-gray-400 uppercase mb-1 block">Date To</label>
            <input
              type="date"
              value={dateTo}
              onChange={handleDateTo}
              className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>

          {/* Clear Filters */}
          {hasActiveFilters && (
            <button
              onClick={clearFilters}
              className="text-sm text-red-500 hover:text-red-700 px-3 py-2 border border-red-200 rounded hover:bg-red-50"
            >
              Clear Filters
            </button>
          )}

        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b">
            <tr>
              {['title', 'category', 'status', 'priority', 'createdAt'].map(field => (
                <th
                  key={field}
                  onClick={() => handleSort(field)}
                  className="text-left px-6 py-3 text-xs text-gray-500 uppercase cursor-pointer hover:text-gray-700 select-none"
                >
                  {field === 'createdAt' ? 'Created At' : field.charAt(0).toUpperCase() + field.slice(1)}
                  {sortField === field ? (sortDir === 'asc' ? ' ↑' : ' ↓') : ' ↕'}
                </th>
              ))}
              <th className="text-left px-6 py-3 text-xs text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              Array(5).fill(0).map((_, i) => (
                <tr key={i} className="border-b">
                  {Array(6).fill(0).map((_, j) => (
                    <td key={j} className="px-6 py-4">
                      <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
                    </td>
                  ))}
                </tr>
              ))
            ) : paginated.length === 0 ? (
              <tr>
                <td colSpan={6} className="text-center py-12 text-gray-400">
                  No records match your filters.
                </td>
              </tr>
            ) : (
              paginated.map(record => (
                <tr key={record.id} className="border-b hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium text-gray-800">{record.title}</td>
                  <td className="px-6 py-4 text-gray-600">{record.category}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${statusColors[record.status]}`}>
                      {record.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-gray-600">{record.priority}</td>
                  <td className="px-6 py-4 text-gray-600">{record.createdAt}</td>
                  <td className="px-6 py-4">
                    <button
                      onClick={() => navigate(`/records/${record.id}`)}
                      className="text-blue-600 hover:underline mr-3"
                    >
                      View
                    </button>
                    <button
                      onClick={() => navigate(`/edit/${record.id}`)}
                      className="text-gray-500 hover:underline"
                    >
                      Edit
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-between items-center mt-4 text-sm text-gray-600">
          <span>Page {page} of {totalPages}</span>
          <div className="flex gap-2">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-3 py-1 border rounded disabled:opacity-40 hover:bg-gray-50"
            >
              Previous
            </button>
            <button
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="px-3 py-1 border rounded disabled:opacity-40 hover:bg-gray-50"
            >
              Next
            </button>
          </div>
        </div>
      )}

    </div>
  )
}