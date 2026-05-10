import { useEffect, useState, useRef } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { TableSkeleton } from '../components/Skeleton'
import EmptyState from '../components/EmptyState'
import { getRecords, exportCSV } from '../services/api'   // ← ONLY new import

const statusColors = {
  'Completed':  'bg-green-100 text-green-800',
  'In Progress':'bg-yellow-100 text-yellow-800',
  'Active':     'bg-blue-100 text-blue-800',
  'Blocked':    'bg-red-100 text-red-800',
  'Not Started':'bg-gray-100 text-gray-700',
}

const priorityColors = {
  'Critical': 'text-red-600 font-bold',
  'High':     'text-orange-500 font-semibold',
  'Medium':   'text-yellow-600',
  'Low':      'text-gray-500',
}

export default function ListPage() {
  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams()

  const [searchText,   setSearchText]   = useState(searchParams.get('search')   || '')
  const [statusFilter, setStatusFilter] = useState(searchParams.get('status')   || '')
  const [dateFrom,     setDateFrom]     = useState(searchParams.get('dateFrom') || '')
  const [dateTo,       setDateTo]       = useState(searchParams.get('dateTo')   || '')
  const [records,      setRecords]      = useState([])
  const [totalElements, setTotalElements] = useState(0)
  const [totalPages,   setTotalPages]   = useState(1)
  const [loading,      setLoading]      = useState(true)
  const [exporting,    setExporting]    = useState(false)
  const [sortField,    setSortField]    = useState('createdAt')
  const [sortDir,      setSortDir]      = useState('desc')
  const [page,         setPage]         = useState(0)   // 0-indexed to match Spring Page
  const ITEMS_PER_PAGE = 8

  const debounceRef = useRef(null)

  // ── Fetch from mock API (or real API later) ──────────────────────────────
  const fetchRecords = async () => {
    setLoading(true)
    try {
      const result = await getRecords({
        page,
        size: ITEMS_PER_PAGE,
        search: searchText,
        status: statusFilter,
        sortBy: sortField,
        sortDir,
      })
      setRecords(result.content)
      setTotalElements(result.totalElements)
      setTotalPages(result.totalPages)
    } catch (err) {
      console.error('Failed to fetch records:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchRecords() }, [page, statusFilter, dateFrom, dateTo, sortField, sortDir])

  // debounce search separately so typing doesn't spam requests
  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      setPage(0)
      fetchRecords()
    }, 300)
    return () => clearTimeout(debounceRef.current)
  }, [searchText])

  // ── URL sync helpers ─────────────────────────────────────────────────────
  const updateURL = (newParams) => {
    const current = {
      search: searchParams.get('search') || '',
      status: searchParams.get('status') || '',
      dateFrom: searchParams.get('dateFrom') || '',
      dateTo: searchParams.get('dateTo') || '',
      ...newParams,
    }
    setSearchParams(Object.fromEntries(Object.entries(current).filter(([, v]) => v !== '')))
  }

  const handleSearchChange = (e) => { setSearchText(e.target.value); updateURL({ search: e.target.value }) }
  const handleStatusChange = (e) => { setStatusFilter(e.target.value); setPage(0); updateURL({ status: e.target.value }) }
  const handleDateFrom     = (e) => { setDateFrom(e.target.value);   setPage(0); updateURL({ dateFrom: e.target.value }) }
  const handleDateTo       = (e) => { setDateTo(e.target.value);     setPage(0); updateURL({ dateTo: e.target.value }) }

  const clearFilters = () => {
    setSearchText(''); setStatusFilter(''); setDateFrom(''); setDateTo(''); setPage(0)
    setSearchParams({})
  }

  const handleSort = (field) => {
    if (sortField === field) setSortDir(d => d === 'asc' ? 'desc' : 'asc')
    else { setSortField(field); setSortDir('asc') }
    setPage(0)
  }

  const handleExport = async () => {
    setExporting(true)
    try { await exportCSV({ status: statusFilter }) }
    catch (e) { console.error('Export failed:', e) }
    finally { setExporting(false) }
  }

  const hasActiveFilters = searchText || statusFilter || dateFrom || dateTo
  const displayPage = page + 1  // show 1-indexed to user

  // ── Loading skeleton ─────────────────────────────────────────────────────
  if (loading && records.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-2xl font-bold text-[#1B4F8A]">All Records</h1>
            <p className="text-sm text-gray-500 mt-1">Loading...</p>
          </div>
          <div className="flex gap-3">
            <button className="border border-gray-300 text-gray-600 px-4 py-2 rounded text-sm">Dashboard</button>
            <button className="bg-[#1B4F8A] text-white px-4 py-2 rounded text-sm">+ New Record</button>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <TableSkeleton rows={8} cols={6} />
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 sm:p-8">

      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-[#1B4F8A]">All Records</h1>
          <p className="text-sm text-gray-500 mt-1">
            {loading ? 'Refreshing...' : `${totalElements} record${totalElements !== 1 ? 's' : ''} found`}
          </p>
        </div>
        <div className="flex gap-2 sm:gap-3">
          <button
            onClick={handleExport}
            disabled={exporting}
            className="border border-gray-300 text-gray-600 px-3 py-2 rounded hover:bg-gray-50 text-sm disabled:opacity-50"
          >
            {exporting ? 'Exporting…' : '↓ CSV'}
          </button>
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
          <div className="flex-1 min-w-[200px]">
            <label className="text-xs text-gray-400 uppercase mb-1 block">Search</label>
            <input
              type="text"
              value={searchText}
              onChange={handleSearchChange}
              placeholder="Search by title, category, assignee..."
              className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>

          <div className="min-w-[160px]">
            <label className="text-xs text-gray-400 uppercase mb-1 block">Status</label>
            <select
              value={statusFilter}
              onChange={handleStatusChange}
              className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300"
            >
              <option value="">All Statuses</option>
              <option value="Active">Active</option>
              <option value="In Progress">In Progress</option>
              <option value="Completed">Completed</option>
              <option value="Blocked">Blocked</option>
            </select>
          </div>

          <div className="min-w-[150px]">
            <label className="text-xs text-gray-400 uppercase mb-1 block">Date From</label>
            <input type="date" value={dateFrom} onChange={handleDateFrom}
              className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300" />
          </div>

          <div className="min-w-[150px]">
            <label className="text-xs text-gray-400 uppercase mb-1 block">Date To</label>
            <input type="date" value={dateTo} onChange={handleDateTo}
              className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300" />
          </div>

          {hasActiveFilters && (
            <button onClick={clearFilters}
              className="text-sm text-red-500 hover:text-red-700 px-3 py-2 border border-red-200 rounded hover:bg-red-50">
              Clear Filters
            </button>
          )}
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="p-6"><TableSkeleton rows={8} cols={6} /></div>
        ) : (
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b">
              <tr>
                {[
                  { field: 'title',     label: 'Title' },
                  { field: 'category',  label: 'Category' },
                  { field: 'status',    label: 'Status' },
                  { field: 'priority',  label: 'Priority' },
                  { field: 'assignedTo',label: 'Assigned To' },
                  { field: 'createdAt', label: 'Created At' },
                ].map(({ field, label }) => (
                  <th key={field} onClick={() => handleSort(field)}
                    className="text-left px-6 py-3 text-xs text-gray-500 uppercase cursor-pointer hover:text-gray-700 select-none">
                    {label}{sortField === field ? (sortDir === 'asc' ? ' ↑' : ' ↓') : ' ↕'}
                  </th>
                ))}
                <th className="text-left px-6 py-3 text-xs text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody>
              {records.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12">
                    <EmptyState
                      variant={hasActiveFilters ? 'no-results' : 'no-data'}
                      body={hasActiveFilters ? 'No records match your filters. Try clearing them.' : 'No records yet. Create your first one!'}
                      action={hasActiveFilters
                        ? { label: 'Clear Filters', onClick: clearFilters }
                        : { label: '+ New Record', onClick: () => navigate('/create') }}
                    />
                  </td>
                </tr>
              ) : (
                records.map(record => (
                  <tr key={record.id} className="border-b hover:bg-gray-50">
                    <td className="px-6 py-4 font-medium text-gray-800 max-w-[220px] truncate">{record.title}</td>
                    <td className="px-6 py-4 text-gray-600">{record.category}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${statusColors[record.status] || 'bg-gray-100 text-gray-700'}`}>
                        {record.status}
                      </span>
                    </td>
                    <td className={`px-6 py-4 text-xs ${priorityColors[record.priority] || ''}`}>{record.priority}</td>
                    <td className="px-6 py-4 text-gray-600">{record.assignedTo}</td>
                    <td className="px-6 py-4 text-gray-500">{record.createdAt?.split('T')[0]}</td>
                    <td className="px-6 py-4">
                      <button onClick={() => navigate(`/records/${record.id}`)}
                        className="text-blue-600 hover:underline mr-3">View</button>
                      <button onClick={() => navigate(`/edit/${record.id}`)}
                        className="text-gray-500 hover:underline">Edit</button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        )}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-between items-center mt-4 text-sm text-gray-600">
          <span>Page {displayPage} of {totalPages} ({totalElements} records)</span>
          <div className="flex gap-2">
            <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0}
              className="px-3 py-1 border rounded disabled:opacity-40 hover:bg-gray-50">Previous</button>
            <button onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))} disabled={page === totalPages - 1}
              className="px-3 py-1 border rounded disabled:opacity-40 hover:bg-gray-50">Next</button>
          </div>
        </div>
      )}

    </div>
  )
}