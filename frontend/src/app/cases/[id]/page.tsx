'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { 
  ArrowLeftIcon,
  DocumentIcon,
  ChatBubbleLeftIcon,
  PhoneIcon,
  CalendarIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  XCircleIcon,
  ArrowDownTrayIcon,
  PencilIcon
} from '@heroicons/react/24/outline'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface TimelineEvent {
  id: string
  title: string
  description: string
  timestamp: string
  type: 'submitted' | 'update' | 'approved' | 'rejected' | 'info-required' | 'completed'
  user: string
}

interface CaseDocument {
  id: string
  name: string
  type: string
  size: string
  uploadDate: string
}

interface CaseDetails {
  id: string
  referenceNumber: string
  title: string
  type: string
  status: 'draft' | 'submitted' | 'under-review' | 'additional-info-required' | 'approved' | 'rejected' | 'completed'
  createdDate: string
  lastUpdate: string
  description: string
  submittedBy: string
  assignedTo: string
  department: string
  priority: 'low' | 'medium' | 'high'
  timeline: TimelineEvent[]
  documents: CaseDocument[]
  comments: string
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

const timelineIcons = {
  'submitted': CheckCircleIcon,
  'update': ClockIcon,
  'approved': CheckCircleIcon,
  'rejected': XCircleIcon,
  'info-required': ExclamationCircleIcon,
  'completed': CheckCircleIcon
}

const timelineColors = {
  'submitted': 'text-blue-600 bg-blue-100',
  'update': 'text-yellow-600 bg-yellow-100',
  'approved': 'text-green-600 bg-green-100',
  'rejected': 'text-red-600 bg-red-100',
  'info-required': 'text-orange-600 bg-orange-100',
  'completed': 'text-purple-600 bg-purple-100'
}

export default function CaseDetailPage() {
  const params = useParams()
  const [caseDetails, setCaseDetails] = useState<CaseDetails | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchCaseDetails = async () => {
      try {
        setLoading(true)
        const response = await fetch(`http://localhost:8000/api/cases/${params.id}`)
        
        if (!response.ok) {
          throw new Error('Case not found')
        }
        
        const data = await response.json()
        setCaseDetails(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load case details')
      } finally {
        setLoading(false)
      }
    }

    if (params.id) {
      fetchCaseDetails()
    }
  }, [params.id])

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-12 bg-gray-200 rounded w-1/2 mb-8"></div>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 space-y-6">
              <div className="h-64 bg-gray-200 rounded"></div>
              <div className="h-96 bg-gray-200 rounded"></div>
            </div>
            <div className="space-y-6">
              <div className="h-48 bg-gray-200 rounded"></div>
              <div className="h-32 bg-gray-200 rounded"></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (error || !caseDetails) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Case Not Found</h1>
          <p className="text-gray-600 mb-4">{error || 'The requested case could not be found.'}</p>
          <Link href="/cases" className="text-primary-600 hover:text-primary-700">
            ← Back to Cases
          </Link>
        </div>
      </div>
    )
  }

  const getProgressPercentage = () => {
    const totalSteps = 4 // submitted, review, approval, completed
    const currentStep = caseDetails.timeline.length
    return Math.min((currentStep / totalSteps) * 100, 100)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const formatDateTime = (dateString: string) => {
    const date = new Date(dateString)
    return `${date.toLocaleDateString()} at ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <Link href="/cases" className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-4">
          <ArrowLeftIcon className="h-4 w-4 mr-1" />
          Back to Cases
        </Link>
        
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{caseDetails.title}</h1>
            <p className="text-gray-600 mt-1">Reference: {caseDetails.referenceNumber}</p>
          </div>
          <div className="mt-4 sm:mt-0 flex space-x-3">
            {caseDetails.status === 'draft' && (
              <Button variant="outline">
                <PencilIcon className="h-4 w-4 mr-2" />
                Edit
              </Button>
            )}
            <Button variant="outline">
              <ArrowDownTrayIcon className="h-4 w-4 mr-2" />
              Download
            </Button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Case Overview */}
          <Card>
            <CardHeader>
              <CardTitle>Case Overview</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div>
                  <h4 className="font-medium text-gray-900">Status</h4>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${statusColors[caseDetails.status]}`}>
                    {caseDetails.status.charAt(0).toUpperCase() + caseDetails.status.slice(1).replace('-', ' ')}
                  </span>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900">Type</h4>
                  <p className="text-gray-600">{caseDetails.type}</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900">Created Date</h4>
                  <p className="text-gray-600">{formatDate(caseDetails.createdDate)}</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900">Last Update</h4>
                  <p className="text-gray-600">{formatDate(caseDetails.lastUpdate)}</p>
                </div>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Description</h4>
                <p className="text-gray-600">{caseDetails.description}</p>
              </div>

              {caseDetails.comments && (
                <div className="mt-4">
                  <h4 className="font-medium text-gray-900 mb-2">Comments</h4>
                  <p className="text-gray-600">{caseDetails.comments}</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Timeline */}
          <Card>
            <CardHeader>
              <CardTitle>Case Timeline</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flow-root">
                <ul className="-mb-8">
                  {caseDetails.timeline.map((event, eventIdx) => {
                    const IconComponent = timelineIcons[event.type]
                    return (
                      <li key={event.id}>
                        <div className="relative pb-8">
                          {eventIdx !== caseDetails.timeline.length - 1 ? (
                            <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true" />
                          ) : null}
                          <div className="relative flex space-x-3">
                            <div>
                              <span className={`h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white ${timelineColors[event.type]}`}>
                                <IconComponent className="h-4 w-4" aria-hidden="true" />
                              </span>
                            </div>
                            <div className="flex min-w-0 flex-1 justify-between space-x-4 pt-1.5">
                              <div>
                                <p className="text-sm font-medium text-gray-900">{event.title}</p>
                                <p className="text-sm text-gray-500">{event.description}</p>
                                <p className="text-xs text-gray-400 mt-1">by {event.user}</p>
                              </div>
                              <div className="whitespace-nowrap text-right text-sm text-gray-500">
                                <time dateTime={event.timestamp}>
                                  {formatDateTime(event.timestamp)}
                                </time>
                              </div>
                            </div>
                          </div>
                        </div>
                      </li>
                    )
                  })}
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Documents */}
          <Card>
            <CardHeader>
              <CardTitle>Documents</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {caseDetails.documents.map((doc) => (
                  <div key={doc.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <DocumentIcon className="h-8 w-8 text-gray-400" />
                      <div>
                        <p className="text-sm font-medium text-gray-900">{doc.name}</p>
                        <p className="text-xs text-gray-500">{doc.type} • {doc.size} • {formatDate(doc.uploadDate)}</p>
                      </div>
                    </div>
                    <Button variant="ghost" size="icon">
                      <ArrowDownTrayIcon className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Case Summary */}
          <Card>
            <CardHeader>
              <CardTitle>Case Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h4 className="text-sm font-medium text-gray-500">Submitted by</h4>
                  <p className="text-sm text-gray-900">{caseDetails.submittedBy}</p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-gray-500">Assigned to</h4>
                  <p className="text-sm text-gray-900">{caseDetails.assignedTo}</p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-gray-500">Department</h4>
                  <p className="text-sm text-gray-900">{caseDetails.department}</p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-gray-500">Priority</h4>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    caseDetails.priority === 'high' ? 'bg-red-100 text-red-800' :
                    caseDetails.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {caseDetails.priority.charAt(0).toUpperCase() + caseDetails.priority.slice(1)}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Progress */}
          <Card>
            <CardHeader>
              <CardTitle>Progress</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Completion</span>
                  <span className="font-medium">{getProgressPercentage()}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${getProgressPercentage()}%` }}
                  ></div>
                </div>
                <div className="text-xs text-gray-500">
                  {caseDetails.status === 'approved' ? 'Case approved and completed' :
                   caseDetails.status === 'under-review' ? 'Currently under review' :
                   caseDetails.status === 'submitted' ? 'Case submitted, awaiting review' :
                   'Case in progress'}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Contact Information */}
          <Card>
            <CardHeader>
              <CardTitle>Contact Information</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <Button variant="outline" className="w-full justify-start">
                  <PhoneIcon className="h-4 w-4 mr-2" />
                  Call HR Department
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <ChatBubbleLeftIcon className="h-4 w-4 mr-2" />
                  Send Message
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <CalendarIcon className="h-4 w-4 mr-2" />
                  Schedule Meeting
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Related Resources */}
          <Card>
            <CardHeader>
              <CardTitle>Related Resources</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <Link href="/resources/maternity-benefits" className="block text-sm text-primary-600 hover:text-primary-700">
                  Maternity Benefits Guide
                </Link>
                <Link href="/resources/leave-policies" className="block text-sm text-primary-600 hover:text-primary-700">
                  Leave Policies Overview
                </Link>
                <Link href="/resources/faq" className="block text-sm text-primary-600 hover:text-primary-700">
                  Frequently Asked Questions
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
