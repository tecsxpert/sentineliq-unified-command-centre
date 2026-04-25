import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import API from '../services/api'

const DUMMY_RESPONSE = {
  content: [
    { id: 1, title: 'Fix login bug', status: 'In Progress', category: 'Bug', createdAt: '2026-04-14' },
    { id: 2, title: 'Add dashboard charts', status: 'Completed', category: 'Feature', createdAt: '2026-04-15' },
    { id: 3, title: 'Write API docs', status: 'Not Started', category: 'Docs', createdAt: '2026-04-16' },
    { id: 4, title: 'Setup Docker', status: 'In Progress', category: 'DevOps', createdAt: '2026-04-17' },
    { id: 5, title: 'Security testing', status: 'Not Started', category: 'Security', createdAt: '2026-04-18' },
    { id: 6, title: 'JWT implementation', status: 'Completed', category: 'Feature', createdAt: '2026-04-19' },
    { id: 7, title: 'Redis caching', status: 'In Progress', category: 'DevOps', createdAt: '2026-04-20' },
    { id: 8, title: 'Email notifications', status: 'Not Started', category: 'Feature', createdAt: '2026-04-21' },
  ],
  totalPages: 3,
  totalElements: 8,
  number: 0,
  size: 8,
}

const statusColors = {
  'Completed': 'bg-green-100 text-green-800',
  'In Progress': 'bg-yellow-100 text-yellow-800',
  'Not Started': 'bg-gray-100 text-gray-700',
}

export default function ListPage() {
  const navigate = useNavigate()
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(0)
  const [totalPages, setTotalPages] = useState(0)
  const [totalElements, setTotalElements] = useState(0)
  const [sortBy, setSortBy] = useState('createdAt')
  const [sortDir, setSortDir] = useState('desc')

  useEffect(() => {
    fetchRecords()
  }, [page, sortBy, sortDir])

  const fetchRecords = async () => {
    setLoading(true)
    try {
      // Uncomment when backend is ready:
      // const res = await API.get(`/api/items?page=${page}&size=8&sortBy=${sortBy}&sortDir=${sortDir}`)
      // setRecords(res.data.content)
      // setTotalPages(res.data.totalPages)
      // setTotalElements(res.data.totalElements)

      setTimeout(() => {
        setRecords(DUMMY_RESPONSE.content)
        setTotalPages(DUMMY_RESPONSE.totalPages)
        setTotalElements(DUMMY_RESPONSE.totalElements)
        setLoading(false)
      }, 800)
    } catch (error) {
      console.error('Failed to fetch records:', error)
      setLoading(false)
    }
  }

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(column)
      setSortDir('asc')
    }
  }

  const SortIcon = ({ column }) => {
    if (sortBy !== column) return <span className="ml-1 text-blue-300">↕</span>
    return <span className="ml-1">{sortDir === 'asc' ? '↑' : '↓'}</span>
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-[#1B4F8A]">All Records</h1>
          <p className="text-sm text-gray-500 mt-1">Total: {totalElements} records</p>
        </div>
        <button
          onClick={() => navigate('/create')}
          className="bg-[#1B4F8A] text-white px-4 py-2 rounded hover:bg-blue-800"
        >
          + New Record
        </button>
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full text-sm text-left">
          <thead className="bg-[#1B4F8A] text-white">
            <tr>
              <th className="px-6 py-3">#</th>
              <th className="px-6 py-3 cursor-pointer hover:bg-blue-800"
                onClick={() => handleSort('title')}>
                Title <SortIcon column="title" />
              </th>
              <th className="px-6 py-3 cursor-pointer hover:bg-blue-800"
                onClick={() => handleSort('category')}>
                Category <SortIcon column="category" />
              </th>
              <th className="px-6 py-3 cursor-pointer hover:bg-blue-800"
                onClick={() => handleSort('status')}>
                Status <SortIcon column="status" />
              </th>
              <th className="px-6 py-3 cursor-pointer hover:bg-blue-800"
                onClick={() => handleSort('createdAt')}>
                Created At <SortIcon column="createdAt" />
              </th>
              <th className="px-6 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading && Array(5).fill(0).map((_, i) => (
              <tr key={i} className="border-b">
                {Array(6).fill(0).map((_, j) => (
                  <td key={j} className="px-6 py-4">
                    <div className="h-4 bg-gray-200 rounded animate-pulse w-24"></div>
                  </td>
                ))}
              </tr>
            ))}

            {!loading && records.length === 0 && (
              <tr>
                <td colSpan={6} className="px-6 py-12 text-center text-gray-400">
                  No records found.
                </td>
              </tr>
            )}

            {!loading && records.map((record) => (
              <tr key={record.id} className="border-b hover:bg-gray-50">
                <td className="px-6 py-4 text-gray-500">{record.id}</td>
                <td className="px-6 py-4 font-medium text-gray-800">{record.title}</td>
                <td className="px-6 py-4 text-gray-600">{record.category}</td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-semibold ${statusColors[record.status]}`}>
                    {record.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-gray-600">{record.createdAt}</td>
                <td className="px-6 py-4">
                  <button className="text-blue-600 hover:underline mr-3">View</button>
                  <button className="text-red-500 hover:underline">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {!loading && totalPages > 0 && (
        <div className="flex justify-between items-center mt-4">
          <p className="text-sm text-gray-500">
            Page {page + 1} of {totalPages}
          </p>
          <div className="flex gap-2">
            <button
              onClick={() => setPage(page - 1)}
              disabled={page === 0}
              className="px-3 py-1 border rounded text-sm disabled:opacity-40 hover:bg-gray-100"
            >
              ← Previous
            </button>
            {Array.from({ length: totalPages }, (_, i) => (
              <button
                key={i}
                onClick={() => setPage(i)}
                className={`px-3 py-1 border rounded text-sm ${
                  page === i ? 'bg-[#1B4F8A] text-white' : 'hover:bg-gray-100'
                }`}
              >
                {i + 1}
              </button>
            ))}
            <button
              onClick={() => setPage(page + 1)}
              disabled={page === totalPages - 1}
              className="px-3 py-1 border rounded text-sm disabled:opacity-40 hover:bg-gray-100"
            >
              Next →
            </button>
            
            <button
               onClick={() => navigate(`/records/${record.id}`)}
                className="text-blue-600 hover:underline mr-3"
                >
                   View
              </button>
          </div>
        </div>
      )}
    </div>
  )
}