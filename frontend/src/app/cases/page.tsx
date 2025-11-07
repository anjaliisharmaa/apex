'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { 
  FunnelIcon,
  MagnifyingGlassIcon,
  EyeIcon,
  PencilIcon,
  ArrowDownTrayIcon,
  TrashIcon,
  PlusIcon
} from '@heroicons/react/24/outline'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface Case {
  id: string
  title: string
  description: string
  status: 'draft' | 'submitted' | 'under-review' | 'additional-info-required' | 'approved' | 'rejected' | 'completed'
  created_at: string
  last_updated: string
}

const statusColors = {
  'draft': 'bg-gray-100 text-gray-800',
  'submitted': 'bg-blue-100 text-blue-800',
  'under-review': 'bg-yellow-100 text-yellow-800',
  'additional-info-required': 'bg-orange-100 text-orange-800',
  'approved': 'bg-green-100 text-green-800',
  'rejected': 'bg-red-100 text-red-800',
  'completed': 'bg-purple-100 text-purple-800'
}

const statusLabels = {
  'draft': 'Draft',
  'submitted': 'Submitted',
  'under-review': 'Under Review',
  'additional-info-required': 'Additional Info Required',
  'approved': 'Approved',
  'rejected': 'Rejected',
  'completed': 'Completed'
}

export default function CasesPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [cases, setCases] = useState<Case[]>([])
  const [filteredCases, setFilteredCases] = useState<Case[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchCases = async () => {
      try {
        setLoading(true)
        const response = await fetch('http://localhost:8000/api/cases')
        if (response.ok) {
          const data = await response.json()
          setCases(data)
          setFilteredCases(data)
        }
      } catch (error) {
        console.error('Failed to fetch cases:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchCases()
  }, [])

  useEffect(() => {
    filterCases(searchTerm, statusFilter)
  }, [cases, searchTerm, statusFilter])

  const filterCases = (term: string, status: string) => {
    let filtered = cases

    if (term) {
      filtered = filtered.filter(case_ => 
        case_.title.toLowerCase().includes(term.toLowerCase()) ||
        case_.id.toLowerCase().includes(term.toLowerCase())
      )
    }

    if (status !== 'all') {
      filtered = filtered.filter(case_ => case_.status === status)
    }

    setFilteredCases(filtered)
  }

  const getStatusCounts = () => {
    const counts = {
      all: cases.length,
      active: cases.filter(c => ['submitted', 'under-review', 'additional-info-required'].includes(c.status)).length,
      completed: cases.filter(c => ['approved', 'rejected', 'completed'].includes(c.status)).length,
      draft: cases.filter(c => c.status === 'draft').length
    }
    return counts
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const statusCounts = getStatusCounts()

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Cases</h1>
          <p className="text-gray-600 mt-1">
            Track and manage your submissions and requests
          </p>
        </div>
        <Link href="/forms">
          <Button className="mt-4 sm:mt-0">
            <PlusIcon className="h-4 w-4 mr-2" />
            Create New Case
          </Button>
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-gray-900">{statusCounts.all}</div>
            <div className="text-sm text-gray-500">Total Cases</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-yellow-600">{statusCounts.active}</div>
            <div className="text-sm text-gray-500">Active Cases</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-green-600">{statusCounts.completed}</div>
            <div className="text-sm text-gray-500">Completed</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-gray-600">{statusCounts.draft}</div>
            <div className="text-sm text-gray-500">Drafts</div>
          </CardContent>
        </Card>
      </div>

      {/* Filters and Search */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-lg">Filters</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4">
            {/* Search */}
            <div className="relative flex-1">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search by case title or reference number..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>

            {/* Status Filter */}
            <div className="flex items-center space-x-2">
              <FunnelIcon className="h-4 w-4 text-gray-400" />
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="border border-gray-300 rounded-md px-3 py-2 bg-white text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="all">All Status</option>
                <option value="draft">Draft</option>
                <option value="submitted">Submitted</option>
                <option value="under-review">Under Review</option>
                <option value="additional-info-required">Additional Info Required</option>
                <option value="approved">Approved</option>
                <option value="rejected">Rejected</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Cases Table */}
      <Card>
        <CardContent className="p-0">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              <span className="ml-2 text-gray-600">Loading cases...</span>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Reference #
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Title
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Type
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Created
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Last Update
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredCases.map((case_) => (
                    <tr key={case_.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {case_.id.toUpperCase()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{case_.title}</div>
                        <div className="text-sm text-gray-500">{case_.description}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {case_.title.includes('Leave') ? 'Leave Application' : 
                         case_.title.includes('Transfer') ? 'Transfer Request' :
                         case_.title.includes('Harassment') || case_.title.includes('Complaint') ? 'Grievance' : 'Other'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${statusColors[case_.status]}`}>
                          {statusLabels[case_.status]}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {formatDate(case_.created_at)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {formatDate(case_.last_updated)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <Link href={`/cases/${case_.id}`}>
                            <Button variant="ghost" size="icon" className="h-8 w-8">
                              <EyeIcon className="h-4 w-4" />
                            </Button>
                          </Link>
                          {case_.status === 'draft' && (
                            <Button variant="ghost" size="icon" className="h-8 w-8">
                              <PencilIcon className="h-4 w-4" />
                            </Button>
                          )}
                          <Button variant="ghost" size="icon" className="h-8 w-8">
                            <ArrowDownTrayIcon className="h-4 w-4" />
                          </Button>
                          {case_.status === 'draft' && (
                            <Button variant="ghost" size="icon" className="h-8 w-8 text-red-600 hover:text-red-700">
                              <TrashIcon className="h-4 w-4" />
                            </Button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {filteredCases.length === 0 && (
            <div className="text-center py-12">
              <div className="text-gray-500">
                <FunnelIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No cases found</h3>
                <p className="text-gray-500">
                  {searchTerm || statusFilter !== 'all' 
                    ? 'Try adjusting your search or filter criteria.'
                    : 'You haven\'t created any cases yet.'}
                </p>
                {!searchTerm && statusFilter === 'all' && (
                  <Link href="/forms">
                    <Button className="mt-4">
                      <PlusIcon className="h-4 w-4 mr-2" />
                      Create Your First Case
                    </Button>
                  </Link>
                )}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Pagination */}
      {filteredCases.length > 0 && (
        <div className="mt-6 flex items-center justify-between">
          <div className="text-sm text-gray-700">
            Showing 1 to {filteredCases.length} of {filteredCases.length} results
          </div>
          <div className="flex space-x-2">
            <Button variant="outline" size="sm" disabled>
              Previous
            </Button>
            <Button variant="outline" size="sm" className="bg-primary-600 text-white">
              1
            </Button>
            <Button variant="outline" size="sm" disabled>
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
