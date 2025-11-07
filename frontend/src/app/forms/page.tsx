'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { 
  MagnifyingGlassIcon,
  ClockIcon,
  DocumentTextIcon,
  UserIcon,
  HomeIcon,
  ExclamationTriangleIcon,
  CogIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface FormCategory {
  id: string
  name: string
  description: string
  icon: React.ComponentType<any>
  forms: FormTemplate[]
}

interface FormTemplate {
  id: string
  name: string
  description: string
  estimatedTime: string
  category: string
  complexity: 'simple' | 'medium' | 'complex'
  isPopular?: boolean
}

const formCategories: FormCategory[] = [
  {
    id: 'leave',
    name: 'Leave Applications',
    description: 'Various types of leave applications and requests',
    icon: ClockIcon,
    forms: [
      {
        id: 'maternity-leave',
        name: 'Maternity Leave Application',
        description: 'Apply for 26 weeks of maternity leave as per Maternity Benefits Act',
        estimatedTime: '10-15 minutes',
        category: 'leave',
        complexity: 'medium',
        isPopular: true
      },
      {
        id: 'child-care-leave',
        name: 'Child Care Leave Application',
        description: 'Apply for child care leave for children up to 18 years',
        estimatedTime: '8-12 minutes',
        category: 'leave',
        complexity: 'medium',
        isPopular: true
      },
      {
        id: 'medical-leave',
        name: 'Medical Leave Application',
        description: 'Apply for medical leave due to health conditions',
        estimatedTime: '10-15 minutes',
        category: 'leave',
        complexity: 'medium'
      },
      {
        id: 'personal-leave',
        name: 'Personal Leave Application',
        description: 'Apply for personal leave for family or personal matters',
        estimatedTime: '5-10 minutes',
        category: 'leave',
        complexity: 'simple'
      }
    ]
  },
  {
    id: 'transfer',
    name: 'Transfer Requests',
    description: 'Transfer and posting related applications',
    icon: HomeIcon,
    forms: [
      {
        id: 'spouse-transfer',
        name: 'Spouse Ground Transfer',
        description: 'Request transfer on spouse ground with supporting documents',
        estimatedTime: '15-20 minutes',
        category: 'transfer',
        complexity: 'complex',
        isPopular: true
      },
      {
        id: 'medical-transfer',
        name: 'Medical Ground Transfer',
        description: 'Request transfer on medical grounds for self or family',
        estimatedTime: '15-20 minutes',
        category: 'transfer',
        complexity: 'complex'
      },
      {
        id: 'general-transfer',
        name: 'General Transfer Request',
        description: 'Request transfer for administrative or personal reasons',
        estimatedTime: '10-15 minutes',
        category: 'transfer',
        complexity: 'medium'
      },
      {
        id: 'posting-preference',
        name: 'Posting Preference Form',
        description: 'Submit preferences for future postings and assignments',
        estimatedTime: '8-12 minutes',
        category: 'transfer',
        complexity: 'simple'
      }
    ]
  },
  {
    id: 'grievance',
    name: 'Grievance Forms',
    description: 'Report workplace issues and seek redressal',
    icon: ExclamationTriangleIcon,
    forms: [
      {
        id: 'harassment-complaint',
        name: 'Harassment Complaint',
        description: 'File a complaint regarding workplace harassment (with anonymous option)',
        estimatedTime: '20-30 minutes',
        category: 'grievance',
        complexity: 'complex'
      },
      {
        id: 'workplace-issue',
        name: 'Workplace Issue Report',
        description: 'Report general workplace issues or concerns',
        estimatedTime: '10-15 minutes',
        category: 'grievance',
        complexity: 'medium'
      },
      {
        id: 'policy-clarification',
        name: 'Policy Clarification Request',
        description: 'Request clarification on policies or procedures',
        estimatedTime: '5-8 minutes',
        category: 'grievance',
        complexity: 'simple'
      },
      {
        id: 'suggestion-feedback',
        name: 'Suggestion/Feedback Form',
        description: 'Provide suggestions for improvement or feedback',
        estimatedTime: '5-10 minutes',
        category: 'grievance',
        complexity: 'simple'
      }
    ]
  },
  {
    id: 'administrative',
    name: 'Administrative Forms',
    description: 'Personal information updates and administrative requests',
    icon: CogIcon,
    forms: [
      {
        id: 'address-change',
        name: 'Address Change Notification',
        description: 'Update your official address records',
        estimatedTime: '5-8 minutes',
        category: 'administrative',
        complexity: 'simple'
      },
      {
        id: 'emergency-contact',
        name: 'Emergency Contact Update',
        description: 'Update emergency contact information',
        estimatedTime: '5-8 minutes',
        category: 'administrative',
        complexity: 'simple'
      },
      {
        id: 'dependent-info',
        name: 'Dependent Information Update',
        description: 'Add or update dependent information for benefits',
        estimatedTime: '10-15 minutes',
        category: 'administrative',
        complexity: 'medium'
      },
      {
        id: 'salary-certificate',
        name: 'Salary Certificate Request',
        description: 'Request official salary certificate for various purposes',
        estimatedTime: '5-8 minutes',
        category: 'administrative',
        complexity: 'simple'
      }
    ]
  }
]

const allForms = formCategories.flatMap(category => category.forms)

export default function FormsPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const router = useRouter()
  
  const handlePreviewSample = (formId: string) => {
    router.push(`/forms/preview/${formId}`)
  }

  const filteredForms = allForms.filter(form => {
    const matchesSearch = form.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         form.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = selectedCategory === 'all' || form.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  const popularForms = allForms.filter(form => form.isPopular)

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'simple': return 'bg-green-100 text-green-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'complex': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Document Generator</h1>
        <p className="text-gray-600 mt-1">
          Generate official documents and applications with guided assistance
        </p>
      </div>

      {/* Search and Filter */}
      <Card className="mb-8">
        <CardContent className="p-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search forms by name or description..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="border border-gray-300 rounded-md px-3 py-2 bg-white text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="all">All Categories</option>
              {formCategories.map(category => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </div>
        </CardContent>
      </Card>

      {/* Popular Forms */}
      {searchTerm === '' && selectedCategory === 'all' && (
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Popular Forms</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {popularForms.map(form => (
              <Card key={form.id} className="hover:shadow-lg transition-shadow cursor-pointer group">
                <CardHeader className="pb-4">
                  <div className="flex items-start justify-between">
                    <CardTitle className="text-lg group-hover:text-primary-600 transition-colors">
                      {form.name}
                    </CardTitle>
                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                      Popular
                    </span>
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription className="mb-4">
                    {form.description}
                  </CardDescription>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center text-sm text-gray-500">
                      <ClockIcon className="h-4 w-4 mr-1" />
                      {form.estimatedTime}
                    </div>
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getComplexityColor(form.complexity)}`}>
                      {form.complexity}
                    </span>
                  </div>
                  <div className="space-y-2">
                    <Link href={`/forms/${form.id}`}>
                      <Button className="w-full">Start Form</Button>
                    </Link>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      className="w-full"
                      onClick={() => handlePreviewSample(form.id)}
                    >
                      Preview Sample
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Form Categories or Search Results */}
      {searchTerm === '' && selectedCategory === 'all' ? (
        // Show categories
        <div className="space-y-8">
          {formCategories.map(category => {
            const IconComponent = category.icon
            return (
              <div key={category.id}>
                <div className="flex items-center mb-4">
                  <IconComponent className="h-6 w-6 text-primary-600 mr-3" />
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900">{category.name}</h2>
                    <p className="text-sm text-gray-600">{category.description}</p>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {category.forms.map(form => (
                    <Card key={form.id} className="hover:shadow-lg transition-shadow cursor-pointer group">
                      <CardHeader className="pb-4">
                        <CardTitle className="text-lg group-hover:text-primary-600 transition-colors">
                          {form.name}
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <CardDescription className="mb-4">
                          {form.description}
                        </CardDescription>
                        <div className="flex items-center justify-between mb-4">
                          <div className="flex items-center text-sm text-gray-500">
                            <ClockIcon className="h-4 w-4 mr-1" />
                            {form.estimatedTime}
                          </div>
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getComplexityColor(form.complexity)}`}>
                            {form.complexity}
                          </span>
                        </div>
                        <div className="space-y-2">
                          <Link href={`/forms/${form.id}`}>
                            <Button className="w-full">Start Form</Button>
                          </Link>
                          <Button 
                            variant="ghost" 
                            size="sm" 
                            className="w-full"
                            onClick={() => handlePreviewSample(form.id)}
                          >
                            Preview Sample
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        // Show search results
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            {filteredForms.length > 0 ? `Found ${filteredForms.length} forms` : 'No forms found'}
          </h2>
          
          {filteredForms.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredForms.map(form => (
                <Card key={form.id} className="hover:shadow-lg transition-shadow cursor-pointer group">
                  <CardHeader className="pb-4">
                    <CardTitle className="text-lg group-hover:text-primary-600 transition-colors">
                      {form.name}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="mb-4">
                      {form.description}
                    </CardDescription>
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center text-sm text-gray-500">
                        <ClockIcon className="h-4 w-4 mr-1" />
                        {form.estimatedTime}
                      </div>
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getComplexityColor(form.complexity)}`}>
                        {form.complexity}
                      </span>
                    </div>
                    <div className="space-y-2">
                      <Link href={`/forms/${form.id}`}>
                        <Button className="w-full">Start Form</Button>
                      </Link>
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        className="w-full"
                        onClick={() => handlePreviewSample(form.id)}
                      >
                        Preview Sample
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No forms found</h3>
              <p className="text-gray-500">
                Try adjusting your search terms or browse different categories.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
