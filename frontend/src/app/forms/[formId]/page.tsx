'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { 
  ArrowLeftIcon,
  DocumentTextIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  CalendarIcon,
  UserIcon,
  BuildingOfficeIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { apiClient } from '@/lib/api'

interface FormField {
  id: string
  label: string
  type: 'text' | 'email' | 'date' | 'textarea' | 'select' | 'tel'
  required: boolean
  placeholder?: string
  options?: string[]
  description?: string
}

interface FormTemplate {
  id: string
  name: string
  description: string
  estimatedTime: string
  complexity: 'simple' | 'medium' | 'complex'
  fields: FormField[]
  instructions: string[]
  requiredDocuments: string[]
  legalBasis: string
}

// Form templates with their specific fields
const formTemplates: { [key: string]: FormTemplate } = {
  'maternity-leave': {
    id: 'maternity-leave',
    name: 'Maternity Leave Application',
    description: 'Apply for 26 weeks of maternity leave as per Maternity Benefits Act',
    estimatedTime: '10-15 minutes',
    complexity: 'medium',
    instructions: [
      'Ensure you have your medical certificate ready',
      'Application must be submitted at least 6 weeks before expected delivery',
      'Maternity leave entitlement is 26 weeks with full pay',
      'You may split the leave period before and after delivery'
    ],
    requiredDocuments: [
      'Medical certificate with expected delivery date',
      'Previous maternity leave records (if any)',
      'Marriage certificate (if applicable)'
    ],
    legalBasis: 'Maternity Benefit Act, 2017 - Section 5',
    fields: [
      { id: 'employee_name', label: 'Full Name', type: 'text', required: true, placeholder: 'Enter your full name' },
      { id: 'employee_id', label: 'Employee ID', type: 'text', required: true, placeholder: 'Enter your employee ID' },
      { id: 'department', label: 'Department', type: 'text', required: true, placeholder: 'Enter your department' },
      { id: 'designation', label: 'Designation', type: 'text', required: true, placeholder: 'Enter your job title' },
      { id: 'supervisor_name', label: 'Supervisor/Manager Name', type: 'text', required: true, placeholder: 'Enter supervisor name' },
      { id: 'due_date', label: 'Expected Delivery Date', type: 'date', required: true, description: 'As per medical certificate' },
      { id: 'leave_start_date', label: 'Leave Start Date', type: 'date', required: true, description: 'When you want to start your leave' },
      { id: 'leave_end_date', label: 'Expected Return Date', type: 'date', required: true, description: 'Calculated based on 26 weeks' },
      { id: 'total_days', label: 'Total Leave Days', type: 'text', required: true, placeholder: 'e.g., 180 days' },
      { id: 'contact_during_leave', label: 'Contact Information During Leave', type: 'email', required: true, placeholder: 'Emergency contact email' },
      { id: 'previous_leaves', label: 'Previous Maternity Leaves', type: 'textarea', required: false, placeholder: 'List any previous maternity leaves taken (optional)' },
      { id: 'medical_certificate', label: 'Medical Certificate Details', type: 'textarea', required: true, placeholder: 'Doctor name, hospital, certificate date' }
    ]
  },
  'child-care-leave': {
    id: 'child-care-leave',
    name: 'Child Care Leave Application',
    description: 'Apply for child care leave for children up to 18 years',
    estimatedTime: '8-12 minutes',
    complexity: 'medium',
    instructions: [
      'Child care leave is available for children up to 18 years',
      'Maximum leave period is typically 6 months to 2 years',
      'Submit supporting documents for child\'s age and need',
      'Leave may be granted with or without pay as per company policy'
    ],
    requiredDocuments: [
      'Child\'s birth certificate or age proof',
      'Medical certificate (if for medical care)',
      'School admission documents (if applicable)'
    ],
    legalBasis: 'Company Child Care Leave Policy',
    fields: [
      { id: 'employee_name', label: 'Full Name', type: 'text', required: true, placeholder: 'Enter your full name' },
      { id: 'employee_id', label: 'Employee ID', type: 'text', required: true, placeholder: 'Enter your employee ID' },
      { id: 'department', label: 'Department', type: 'text', required: true, placeholder: 'Enter your department' },
      { id: 'designation', label: 'Designation', type: 'text', required: true, placeholder: 'Enter your job title' },
      { id: 'supervisor_name', label: 'Supervisor/Manager Name', type: 'text', required: true, placeholder: 'Enter supervisor name' },
      { id: 'child_name', label: 'Child\'s Name', type: 'text', required: true, placeholder: 'Enter child\'s full name' },
      { id: 'child_age', label: 'Child\'s Age', type: 'text', required: true, placeholder: 'e.g., 2 years 6 months' },
      { id: 'leave_start', label: 'Leave Start Date', type: 'date', required: true },
      { id: 'leave_end', label: 'Leave End Date', type: 'date', required: true },
      { id: 'total_duration', label: 'Total Leave Duration', type: 'text', required: true, placeholder: 'e.g., 6 months' },
      { id: 'reason', label: 'Reason for Child Care Leave', type: 'textarea', required: true, placeholder: 'Explain why child care leave is needed' },
      { id: 'care_arrangements', label: 'Existing Care Arrangements', type: 'textarea', required: false, placeholder: 'Current childcare arrangements (optional)' },
      { id: 'emergency_contact', label: 'Emergency Contact', type: 'tel', required: true, placeholder: 'Contact number during leave' }
    ]
  },
  'spouse-transfer': {
    id: 'spouse-transfer',
    name: 'Spouse Ground Transfer Request',
    description: 'Request transfer on spouse ground with supporting documents',
    estimatedTime: '15-20 minutes',
    complexity: 'complex',
    instructions: [
      'Transfer on spouse ground requires supporting documents',
      'Spouse\'s employment letter must be from recognized organization',
      'Marriage certificate is mandatory',
      'Transfer is subject to position availability at requested location'
    ],
    requiredDocuments: [
      'Spouse\'s employment letter/job offer',
      'Marriage certificate',
      'Current performance review',
      'Transfer request from spouse\'s organization (if applicable)'
    ],
    legalBasis: 'Company Transfer Policy - Section 3.2',
    fields: [
      { id: 'employee_name', label: 'Full Name', type: 'text', required: true, placeholder: 'Enter your full name' },
      { id: 'employee_id', label: 'Employee ID', type: 'text', required: true, placeholder: 'Enter your employee ID' },
      { id: 'current_department', label: 'Current Department', type: 'text', required: true, placeholder: 'Your current department' },
      { id: 'current_location', label: 'Current Work Location', type: 'text', required: true, placeholder: 'Current office location' },
      { id: 'designation', label: 'Current Designation', type: 'text', required: true, placeholder: 'Your current job title' },
      { id: 'supervisor_name', label: 'Current Supervisor', type: 'text', required: true, placeholder: 'Current reporting manager' },
      { id: 'requested_location', label: 'Requested Transfer Location', type: 'text', required: true, placeholder: 'Preferred office location' },
      { id: 'requested_department', label: 'Preferred Department', type: 'text', required: false, placeholder: 'Same department or specify new one' },
      { id: 'spouse_name', label: 'Spouse\'s Name', type: 'text', required: true, placeholder: 'Enter spouse\'s full name' },
      { id: 'spouse_organization', label: 'Spouse\'s Organization', type: 'text', required: true, placeholder: 'Spouse\'s employer name' },
      { id: 'spouse_designation', label: 'Spouse\'s Designation', type: 'text', required: true, placeholder: 'Spouse\'s job title' },
      { id: 'spouse_location', label: 'Spouse\'s Work Location', type: 'text', required: true, placeholder: 'Spouse\'s office location' },
      { id: 'marriage_date', label: 'Date of Marriage', type: 'date', required: true },
      { id: 'preferred_date', label: 'Preferred Transfer Date', type: 'date', required: true },
      { id: 'reason_for_transfer', label: 'Detailed Reason for Transfer', type: 'textarea', required: true, placeholder: 'Explain the circumstances requiring transfer' },
      { id: 'skills_relevant', label: 'Relevant Skills for New Location', type: 'textarea', required: false, placeholder: 'Skills that match requirements at new location' }
    ]
  },
  'medical-leave': {
    id: 'medical-leave',
    name: 'Medical Leave Application',
    description: 'Apply for medical leave due to health conditions',
    estimatedTime: '10-15 minutes',
    complexity: 'medium',
    instructions: [
      'Medical certificate from registered practitioner required',
      'Leave duration should be as per medical recommendation',
      'For extended leave, periodic medical updates may be required',
      'Return-to-work medical clearance needed before resuming duties'
    ],
    requiredDocuments: [
      'Medical certificate from registered doctor',
      'Hospital/clinic reports',
      'Specialist consultation reports (if applicable)',
      'Previous medical leave records (if any)'
    ],
    legalBasis: 'Company Medical Leave Policy',
    fields: [
      { id: 'employee_name', label: 'Full Name', type: 'text', required: true, placeholder: 'Enter your full name' },
      { id: 'employee_id', label: 'Employee ID', type: 'text', required: true, placeholder: 'Enter your employee ID' },
      { id: 'department', label: 'Department', type: 'text', required: true, placeholder: 'Enter your department' },
      { id: 'designation', label: 'Designation', type: 'text', required: true, placeholder: 'Enter your job title' },
      { id: 'supervisor_name', label: 'Supervisor/Manager Name', type: 'text', required: true, placeholder: 'Enter supervisor name' },
      { id: 'medical_condition', label: 'Medical Condition', type: 'textarea', required: true, placeholder: 'Brief description of medical condition' },
      { id: 'doctor_name', label: 'Attending Physician Name', type: 'text', required: true, placeholder: 'Name of treating doctor' },
      { id: 'hospital_name', label: 'Hospital/Clinic Name', type: 'text', required: true, placeholder: 'Medical facility name' },
      { id: 'leave_start', label: 'Leave Start Date', type: 'date', required: true },
      { id: 'leave_end', label: 'Expected Return Date', type: 'date', required: true },
      { id: 'total_duration', label: 'Total Leave Duration', type: 'text', required: true, placeholder: 'e.g., 2 weeks' },
      { id: 'treatment_type', label: 'Type of Treatment', type: 'select', required: true, options: ['Outpatient', 'Inpatient', 'Surgery', 'Therapy', 'Recovery', 'Other'] },
      { id: 'emergency_contact', label: 'Emergency Contact', type: 'tel', required: true, placeholder: 'Contact number during leave' },
      { id: 'previous_medical_leaves', label: 'Previous Medical Leaves', type: 'textarea', required: false, placeholder: 'Any previous medical leaves for same/related condition' }
    ]
  },
  'harassment-complaint': {
    id: 'harassment-complaint',
    name: 'Harassment Complaint Form',
    description: 'File a complaint regarding workplace harassment',
    estimatedTime: '20-30 minutes',
    complexity: 'complex',
    instructions: [
      'This form is confidential and will be handled by the Internal Complaints Committee',
      'Provide detailed information about incidents with dates and times',
      'Include witness information if available',
      'You have the right to representation during proceedings'
    ],
    requiredDocuments: [
      'Written statement of incidents',
      'Supporting evidence (emails, messages, etc.)',
      'Witness statements (if available)',
      'Previous complaint records (if any)'
    ],
    legalBasis: 'Sexual Harassment of Women at Workplace Act, 2013',
    fields: [
      { id: 'complainant_name', label: 'Your Name', type: 'text', required: true, placeholder: 'Enter your full name' },
      { id: 'employee_id', label: 'Employee ID', type: 'text', required: true, placeholder: 'Enter your employee ID' },
      { id: 'department', label: 'Department', type: 'text', required: true, placeholder: 'Your department' },
      { id: 'designation', label: 'Designation', type: 'text', required: true, placeholder: 'Your job title' },
      { id: 'contact_number', label: 'Contact Number', type: 'tel', required: true, placeholder: 'Your contact number' },
      { id: 'email', label: 'Email Address', type: 'email', required: true, placeholder: 'Your email address' },
      { id: 'respondent_name', label: 'Name of Person Against Whom Complaint is Made', type: 'text', required: true, placeholder: 'Full name of the accused' },
      { id: 'respondent_designation', label: 'Respondent\'s Designation', type: 'text', required: true, placeholder: 'Job title of the accused' },
      { id: 'respondent_department', label: 'Respondent\'s Department', type: 'text', required: true, placeholder: 'Department of the accused' },
      { id: 'incident_date', label: 'Date of Incident', type: 'date', required: true },
      { id: 'incident_time', label: 'Time of Incident', type: 'text', required: true, placeholder: 'Approximate time' },
      { id: 'incident_location', label: 'Location of Incident', type: 'text', required: true, placeholder: 'Where the incident occurred' },
      { id: 'detailed_complaint', label: 'Detailed Description of Incident', type: 'textarea', required: true, placeholder: 'Provide a detailed account of what happened' },
      { id: 'witnesses', label: 'Witnesses (if any)', type: 'textarea', required: false, placeholder: 'Names and contact details of witnesses' },
      { id: 'previous_incidents', label: 'Previous Incidents', type: 'textarea', required: false, placeholder: 'Any previous incidents with the same person' },
      { id: 'resolution_sought', label: 'Resolution Sought', type: 'textarea', required: true, placeholder: 'What resolution/action do you seek?' },
      { id: 'supporting_documents', label: 'Supporting Documents Description', type: 'textarea', required: false, placeholder: 'List any supporting documents you are submitting' }
    ]
  },
  'general-transfer': {
    id: 'general-transfer',
    name: 'General Transfer Request',
    description: 'Request transfer for administrative or personal reasons',
    estimatedTime: '10-15 minutes',
    complexity: 'medium',
    instructions: [
      'General transfer requests are reviewed based on business needs',
      'Provide clear justification for transfer request',
      'Transfer is subject to position availability',
      'Current performance will be considered in the review'
    ],
    requiredDocuments: [
      'Current performance review',
      'Justification letter',
      'Supervisor recommendation (optional)'
    ],
    legalBasis: 'Company Transfer Policy - General Provisions',
    fields: [
      { id: 'employee_name', label: 'Full Name', type: 'text', required: true, placeholder: 'Enter your full name' },
      { id: 'employee_id', label: 'Employee ID', type: 'text', required: true, placeholder: 'Enter your employee ID' },
      { id: 'current_department', label: 'Current Department', type: 'text', required: true, placeholder: 'Your current department' },
      { id: 'current_location', label: 'Current Work Location', type: 'text', required: true, placeholder: 'Current office location' },
      { id: 'designation', label: 'Current Designation', type: 'text', required: true, placeholder: 'Your current job title' },
      { id: 'supervisor_name', label: 'Current Supervisor', type: 'text', required: true, placeholder: 'Current reporting manager' },
      { id: 'requested_location', label: 'Requested Transfer Location', type: 'text', required: true, placeholder: 'Preferred office location' },
      { id: 'requested_department', label: 'Requested Department', type: 'text', required: false, placeholder: 'Preferred department (if different)' },
      { id: 'transfer_type', label: 'Type of Transfer', type: 'select', required: true, options: ['Permanent', 'Temporary', 'Deputation'] },
      { id: 'preferred_date', label: 'Preferred Transfer Date', type: 'date', required: true },
      { id: 'reason_for_transfer', label: 'Reason for Transfer Request', type: 'textarea', required: true, placeholder: 'Detailed justification for transfer' },
      { id: 'career_goals', label: 'How Transfer Aligns with Career Goals', type: 'textarea', required: false, placeholder: 'Explain career development aspects' },
      { id: 'skills_contribution', label: 'Skills You Can Contribute at New Location', type: 'textarea', required: false, placeholder: 'How your skills will benefit the new location' },
      { id: 'additional_info', label: 'Additional Information', type: 'textarea', required: false, placeholder: 'Any other relevant information' }
    ]
  }
}

export default function FormPage() {
  const params = useParams()
  const router = useRouter()
  const [formTemplate, setFormTemplate] = useState<FormTemplate | null>(null)
  const [formData, setFormData] = useState<{ [key: string]: string }>({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [currentStep, setCurrentStep] = useState(1)
  const [errors, setErrors] = useState<{ [key: string]: string }>({})

  useEffect(() => {
    const formId = params.formId as string
    const template = formTemplates[formId]
    
    if (!template) {
      router.push('/forms')
      return
    }

    setFormTemplate(template)
    
    // Initialize form data with empty values
    const initialData: { [key: string]: string } = {}
    template.fields.forEach(field => {
      initialData[field.id] = ''
    })
    setFormData(initialData)
  }, [params.formId, router])

  const handleInputChange = (fieldId: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [fieldId]: value
    }))
    
    // Clear error when user starts typing
    if (errors[fieldId]) {
      setErrors(prev => ({
        ...prev,
        [fieldId]: ''
      }))
    }
  }

  const validateForm = (): boolean => {
    if (!formTemplate) return false
    
    const newErrors: { [key: string]: string } = {}
    
    formTemplate.fields.forEach(field => {
      if (field.required && !formData[field.id]?.trim()) {
        newErrors[field.id] = `${field.label} is required`
      }
      
      // Email validation
      if (field.type === 'email' && formData[field.id] && 
          !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData[field.id])) {
        newErrors[field.id] = 'Please enter a valid email address'
      }
    })
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async () => {
    if (!formTemplate || !validateForm()) return
    
    setIsSubmitting(true)
    try {
      const response = await apiClient.generateDocument({
        document_type: formTemplate.name,
        user_data: formData
      })
      
      // Show success message and redirect or show result
      alert(`Form submitted successfully! Document generated: ${response.document_content?.substring(0, 100)}...`)
      router.push('/cases')
    } catch (error) {
      console.error('Error submitting form:', error)
      alert('Failed to submit form. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'simple': return 'bg-green-100 text-green-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'complex': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const renderField = (field: FormField) => {
    const commonProps = {
      id: field.id,
      value: formData[field.id] || '',
      onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => 
        handleInputChange(field.id, e.target.value),
      className: `w-full ${errors[field.id] ? 'border-red-500' : ''}`
    }

    switch (field.type) {
      case 'textarea':
        return (
          <textarea
            {...commonProps}
            placeholder={field.placeholder}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        )
      case 'select':
        return (
          <select
            {...commonProps}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          >
            <option value="">Select an option</option>
            {field.options?.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        )
      default:
        return (
          <Input
            {...commonProps}
            type={field.type}
            placeholder={field.placeholder}
          />
        )
    }
  }

  if (!formTemplate) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p>Loading form...</p>
        </div>
      </div>
    )
  }

  const totalSteps = 3 // Instructions, Form, Review
  const fieldsPerStep = Math.ceil(formTemplate.fields.length / 2)
  const step1Fields = formTemplate.fields.slice(0, fieldsPerStep)
  const step2Fields = formTemplate.fields.slice(fieldsPerStep)

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <Link href="/forms" className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-4">
          <ArrowLeftIcon className="h-4 w-4 mr-1" />
          Back to Forms
        </Link>
        
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{formTemplate.name}</h1>
            <p className="text-gray-600 mt-1">{formTemplate.description}</p>
          </div>
          <div className="mt-4 sm:mt-0">
            <span className={`inline-flex px-3 py-1 text-sm font-semibold rounded-full ${getComplexityColor(formTemplate.complexity)}`}>
              {formTemplate.complexity} complexity
            </span>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-600">Step {currentStep} of {totalSteps}</span>
          <span className="text-sm text-gray-600">{formTemplate.estimatedTime}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${(currentStep / totalSteps) * 100}%` }}
          />
        </div>
      </div>

      {/* Step Content */}
      {currentStep === 1 && (
        <div className="space-y-6">
          {/* Instructions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <InformationCircleIcon className="h-5 w-5 mr-2" />
                Instructions & Requirements
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Before you begin:</h4>
                  <ul className="space-y-1">
                    {formTemplate.instructions.map((instruction, index) => (
                      <li key={index} className="flex items-start text-sm text-gray-600">
                        <CheckCircleIcon className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                        {instruction}
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Required Documents:</h4>
                  <ul className="space-y-1">
                    {formTemplate.requiredDocuments.map((doc, index) => (
                      <li key={index} className="flex items-start text-sm text-gray-600">
                        <DocumentTextIcon className="h-4 w-4 text-blue-500 mr-2 mt-0.5 flex-shrink-0" />
                        {doc}
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-medium text-blue-900 mb-1">Legal Basis:</h4>
                  <p className="text-sm text-blue-800">{formTemplate.legalBasis}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <div className="flex justify-end">
            <Button onClick={() => setCurrentStep(2)}>
              Continue to Form
            </Button>
          </div>
        </div>
      )}

      {currentStep === 2 && (
        <div className="space-y-6">
          {/* Form Fields - Step 1 */}
          <Card>
            <CardHeader>
              <CardTitle>Personal & Employment Information</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {step1Fields.map(field => (
                  <div key={field.id} className={field.type === 'textarea' ? 'md:col-span-2' : ''}>
                    <label htmlFor={field.id} className="block text-sm font-medium text-gray-700 mb-1">
                      {field.label}
                      {field.required && <span className="text-red-500 ml-1">*</span>}
                    </label>
                    {renderField(field)}
                    {field.description && (
                      <p className="text-xs text-gray-500 mt-1">{field.description}</p>
                    )}
                    {errors[field.id] && (
                      <p className="text-xs text-red-600 mt-1">{errors[field.id]}</p>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <div className="flex justify-between">
            <Button variant="outline" onClick={() => setCurrentStep(1)}>
              Back to Instructions
            </Button>
            <Button onClick={() => setCurrentStep(3)}>
              Continue to Additional Details
            </Button>
          </div>
        </div>
      )}

      {currentStep === 3 && (
        <div className="space-y-6">
          {/* Form Fields - Step 2 */}
          <Card>
            <CardHeader>
              <CardTitle>Additional Details & Submission</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {step2Fields.map(field => (
                  <div key={field.id} className={field.type === 'textarea' ? 'md:col-span-2' : ''}>
                    <label htmlFor={field.id} className="block text-sm font-medium text-gray-700 mb-1">
                      {field.label}
                      {field.required && <span className="text-red-500 ml-1">*</span>}
                    </label>
                    {renderField(field)}
                    {field.description && (
                      <p className="text-xs text-gray-500 mt-1">{field.description}</p>
                    )}
                    {errors[field.id] && (
                      <p className="text-xs text-red-600 mt-1">{errors[field.id]}</p>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Submit Section */}
          <Card>
            <CardHeader>
              <CardTitle>Submit Application</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
                <div className="flex items-start">
                  <ExclamationTriangleIcon className="h-5 w-5 text-yellow-600 mr-2 mt-0.5" />
                  <div>
                    <h4 className="text-sm font-medium text-yellow-800">Review Before Submission</h4>
                    <p className="text-sm text-yellow-700 mt-1">
                      Please review all information carefully. Once submitted, changes may require a new application.
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="flex justify-between">
                <Button variant="outline" onClick={() => setCurrentStep(2)}>
                  Back to Previous
                </Button>
                <Button 
                  onClick={handleSubmit}
                  disabled={isSubmitting}
                  className="min-w-[120px]"
                >
                  {isSubmitting ? (
                    <>
                      <SparklesIcon className="h-4 w-4 mr-2 animate-spin" />
                      Submitting...
                    </>
                  ) : (
                    'Submit Application'
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}