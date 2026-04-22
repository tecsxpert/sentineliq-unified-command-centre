import { useEffect, useState } from 'react'

const DUMMY_DATA = [
  { id: 1, title: 'Fix login bug', status: 'In Progress', category: 'Bug', createdAt: '2026-04-14' },
  { id: 2, title: 'Add dashboard charts', status: 'Completed', category: 'Feature', createdAt: '2026-04-15' },
  { id: 3, title: 'Write API docs', status: 'Not Started', category: 'Docs', createdAt: '2026-04-16' },
  { id: 4, title: 'Setup Docker', status: 'In Progress', category: 'DevOps', createdAt: '2026-04-17' },
  { id: 5, title: 'Security testing', status: 'Not Started', category: 'Security', createdAt: '2026-04-18' },
]

const statusColors = {
  'Completed': 'bg-green-100 text-green-800',
  'In Progress': 'bg-yellow-100 text-yellow-800',
  'Not Started': 'bg-gray-100 text-gray-700',
}

export default function ListPage() {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setTimeout(() => {
      setRecords(DUMMY_DATA)
      setLoading(false)
    }, 1000)
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-[#1B4F8A]">All Records</h1>
        <button className="bg-[#1B4F8A] text-white px-4 py-2 rounded hover:bg-blue-800">
          + New Record
        </button>
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full text-sm text-left">
          <thead className="bg-[#1B4F8A] text-white">
            <tr>
              <th className="px-6 py-3">#</th>
              <th className="px-6 py-3">Title</th>
              <th className="px-6 py-3">Category</th>
              <th className="px-6 py-3">Status</th>
              <th className="px-6 py-3">Created At</th>
              <th className="px-6 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {/* Loading skeleton */}
            {loading && Array(5).fill(0).map((_, i) => (
              <tr key={i} className="border-b">
                {Array(6).fill(0).map((_, j) => (
                  <td key={j} className="px-6 py-4">
                    <div className="h-4 bg-gray-200 rounded animate-pulse w-24"></div>
                  </td>
                ))}
              </tr>
            ))}

            {/* Empty state */}
            {!loading && records.length === 0 && (
              <tr>
                <td colSpan={6} className="px-6 py-12 text-center text-gray-400">
                  No records found.
                </td>
              </tr>
            )}

            {/* Data rows */}
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
    </div>
  )
}