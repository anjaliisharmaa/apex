'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { 
  ArrowLeftIcon,
  DocumentTextIcon,
  ArrowDownTrayIcon,
  PrinterIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { apiClient } from '@/lib/api'

interface FormTemplate {
  id: string
  name: string
  description: string
  estimatedTime: string
  complexity: 'simple' | 'medium' | 'complex'
}

// Form template data
const formTemplates: { [key: string]: FormTemplate } = {
  'maternity-leave': {
    id: 'maternity-leave',
    name: 'Maternity Leave Application',
    description: 'Apply for 26 weeks of maternity leave as per Maternity Benefits Act',
    estimatedTime: '10-15 minutes',
    complexity: 'medium'
  },
  'child-care-leave': {
    id: 'child-care-leave',
    name: 'Child Care Leave Application',
    description: 'Apply for child care leave for children up to 18 years',
    estimatedTime: '8-12 minutes',
    complexity: 'medium'
  },
  'spouse-transfer': {
    id: 'spouse-transfer',
    name: 'Spouse Ground Transfer',
    description: 'Request transfer on spouse ground with supporting documents',
    estimatedTime: '15-20 minutes',
    complexity: 'complex'
  },
  'medical-leave': {
    id: 'medical-leave',
    name: 'Medical Leave Application',
    description: 'Apply for medical leave due to health conditions',
    estimatedTime: '10-15 minutes',
    complexity: 'medium'
  },
  'harassment-complaint': {
    id: 'harassment-complaint',
    name: 'Harassment Complaint',
    description: 'File a complaint regarding workplace harassment',
    estimatedTime: '20-30 minutes',
    complexity: 'complex'
  },
  'general-transfer': {
    id: 'general-transfer',
    name: 'General Transfer Request',
    description: 'Request transfer for administrative or personal reasons',
    estimatedTime: '10-15 minutes',
    complexity: 'medium'
  }
}

export default function FormPreviewPage() {
  const params = useParams()
  const router = useRouter()
  const [formTemplate, setFormTemplate] = useState<FormTemplate | null>(null)
  const [previewContent, setPreviewContent] = useState<string>('')
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const formId = params.formId as string
    const template = formTemplates[formId]
    
    if (!template) {
      setError('Form template not found')
      setIsLoading(false)
      return
    }

    setFormTemplate(template)
    generatePreview(template)
  }, [params.formId])

  const generatePreview = async (template: FormTemplate) => {
    try {
      setIsLoading(true)
      const response = await apiClient.generateDocument({
        document_type: template.name,
        user_data: {
          // Sample data for preview
          employee_name: "Sample Employee",
          employee_id: "EMP001",
          department: "Human Resources",
          designation: "Software Engineer",
          supervisor_name: "Manager Name",
          preview_mode: true,
          // Additional sample data based on form type
          ...(template.id.includes('maternity') && {
            due_date: "March 15, 2024",
            leave_start_date: "March 1, 2024",
            leave_end_date: "September 1, 2024",
            total_days: "180 days",
            contact_during_leave: "employee@company.com"
          }),
          ...(template.id.includes('transfer') && {
            current_department: "Information Technology",
            current_location: "Mumbai",
            requested_department: "Information Technology",
            requested_location: "Delhi",
            reason_for_transfer: "Spouse job relocation",
            preferred_date: "April 1, 2024"
          }),
          ...(template.id.includes('child-care') && {
            child_name: "Sample Child",
            child_age: "2 years",
            leave_start: "February 15, 2024",
            leave_end: "August 15, 2024",
            reason: "Child care responsibilities"
          })
        }
      })
      
      setPreviewContent(response.document_content || 'Preview content generated successfully')
    } catch (error) {
      console.error('Error generating preview:', error)
      setError('Failed to generate preview. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handlePrint = () => {
    window.print()
  }

  const handleDownload = () => {
    if (!previewContent || !formTemplate) return
    
    const blob = new Blob([previewContent], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${formTemplate.name.replace(/\s+/g, '_')}_Preview.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'simple': return 'bg-green-100 text-green-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'complex': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Preview Not Available</h1>
          <p className="text-gray-600 mb-4">{error}</p>
          <Link href="/forms">
            <Button>
              <ArrowLeftIcon className="h-4 w-4 mr-2" />
              Back to Forms
            </Button>
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <Link href="/forms" className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-4">
          <ArrowLeftIcon className="h-4 w-4 mr-1" />
          Back to Forms
        </Link>
        
        {formTemplate && (
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{formTemplate.name}</h1>
              <p className="text-gray-600 mt-1">Document Preview</p>
            </div>
            <div className="mt-4 sm:mt-0 flex space-x-3">
              <Button variant="outline" onClick={handlePrint}>
                <PrinterIcon className="h-4 w-4 mr-2" />
                Print
              </Button>
              <Button variant="outline" onClick={handleDownload}>
                <ArrowDownTrayIcon className="h-4 w-4 mr-2" />
                Download
              </Button>
              <Link href={`/forms/${formTemplate.id}`}>
                <Button>
                  Start Form
                </Button>
              </Link>
            </div>
          </div>
        )}
      </div>

      {/* Form Info */}
      {formTemplate && (
        <Card className="mb-6">
          <CardContent className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <h4 className="font-medium text-gray-900">Description</h4>
                <p className="text-sm text-gray-600 mt-1">{formTemplate.description}</p>
              </div>
              <div>
                <h4 className="font-medium text-gray-900">Estimated Time</h4>
                <p className="text-sm text-gray-600 mt-1">{formTemplate.estimatedTime}</p>
              </div>
              <div>
                <h4 className="font-medium text-gray-900">Complexity</h4>
                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full mt-1 ${getComplexityColor(formTemplate.complexity)}`}>
                  {formTemplate.complexity}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Preview Content */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <DocumentTextIcon className="h-5 w-5 mr-2" />
            Document Preview
          </CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <SparklesIcon className="h-6 w-6 animate-spin text-primary-600 mr-2" />
              <span className="text-gray-600">Generating preview...</span>
            </div>
          ) : (
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="prose max-w-none">
                <pre className="whitespace-pre-wrap font-mono text-sm text-gray-800 leading-relaxed">
                  {previewContent}
                </pre>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Call to Action */}
      {!isLoading && formTemplate && (
        <div className="mt-8 text-center">
          <div className="bg-blue-50 rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Ready to create your {formTemplate.name}?
            </h3>
            <p className="text-gray-600 mb-4">
              This is a sample preview. Click below to start filling out your actual form with guided assistance.
            </p>
            <Link href={`/forms/${formTemplate.id}`}>
              <Button size="lg">
                Start Form Now
              </Button>
            </Link>
          </div>
        </div>
      )}
    </div>
  )
}