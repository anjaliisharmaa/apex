'use client'

import { useState } from 'react'
import Link from 'next/link'
import { 
  MagnifyingGlassIcon,
  BookmarkIcon,
  CalendarIcon,
  ClockIcon,
  UserIcon,
  StarIcon,
  EyeIcon
} from '@heroicons/react/24/outline'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface Resource {
  id: string
  title: string
  summary: string
  category: string
  type: 'policy' | 'guide' | 'story' | 'faq' | 'news'
  readTime: string
  publishDate: Date
  author: string
  views: number
  rating: number
  isFeatured?: boolean
  isBookmarked?: boolean
}

const categories = [
  { id: 'all', name: 'All Resources' },
  { id: 'policies', name: 'Policies & Guidelines' },
  { id: 'legal', name: 'Legal Rights' },
  { id: 'stories', name: 'Success Stories' },
  { id: 'faq', name: 'FAQs' },
  { id: 'news', name: 'News & Updates' }
]

const mockResources: Resource[] = [
  {
    id: '1',
    title: 'POSH Act 2013: Complete Guide for Women Scientists',
    summary: 'Comprehensive guide covering all aspects of the Prevention of Sexual Harassment Act and your rights in the workplace.',
    category: 'legal',
    type: 'guide',
    readTime: '15 min read',
    publishDate: new Date('2024-01-15'),
    author: 'Legal Team',
    views: 1247,
    rating: 4.8,
    isFeatured: true
  },
  {
    id: '2',
    title: 'Maternity Benefits Act: Everything You Need to Know',
    summary: 'Detailed explanation of maternity benefits, leave entitlements, and how to apply for various benefits.',
    category: 'policies',
    type: 'policy',
    readTime: '12 min read',
    publishDate: new Date('2024-01-20'),
    author: 'HR Department',
    views: 892,
    rating: 4.7,
    isFeatured: true
  },
  {
    id: '3',
    title: 'Dr. Sunita Sharma: Breaking Barriers in DRDO',
    summary: 'Inspiring journey of Dr. Sunita Sharma who became the first woman scientist to lead a major defense project.',
    category: 'stories',
    type: 'story',
    readTime: '8 min read',
    publishDate: new Date('2024-02-01'),
    author: 'Editorial Team',
    views: 654,
    rating: 4.9,
    isFeatured: true
  },
  {
    id: '4',
    title: 'Child Care Leave: Updated Guidelines 2024',
    summary: 'New guidelines for child care leave including extended provisions and simplified application process.',
    category: 'policies',
    type: 'policy',
    readTime: '10 min read',
    publishDate: new Date('2024-02-10'),
    author: 'Policy Team',
    views: 543,
    rating: 4.6
  },
  {
    id: '5',
    title: 'Frequently Asked Questions: Transfer Policies',
    summary: 'Common questions and answers about transfer policies, spouse grounds, and application procedures.',
    category: 'faq',
    type: 'faq',
    readTime: '6 min read',
    publishDate: new Date('2024-02-15'),
    author: 'HR Department',
    views: 432,
    rating: 4.5
  },
  {
    id: '6',
    title: 'New Initiatives for Women Scientists Announced',
    summary: 'Government announces new initiatives including mentorship programs and career advancement opportunities.',
    category: 'news',
    type: 'news',
    readTime: '5 min read',
    publishDate: new Date('2024-02-20'),
    author: 'News Team',
    views: 321,
    rating: 4.4
  }
]

export default function ResourcesPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [bookmarkedItems, setBookmarkedItems] = useState<string[]>(['1', '3'])

  const filteredResources = mockResources.filter(resource => {
    const matchesSearch = resource.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         resource.summary.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = selectedCategory === 'all' || resource.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  const featuredResources = mockResources.filter(resource => resource.isFeatured)
  const recentResources = mockResources.slice(0, 3)
  const popularResources = [...mockResources].sort((a, b) => b.views - a.views).slice(0, 3)

  const toggleBookmark = (resourceId: string) => {
    setBookmarkedItems(prev => 
      prev.includes(resourceId) 
        ? prev.filter(id => id !== resourceId)
        : [...prev, resourceId]
    )
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'policy': return 'bg-blue-100 text-blue-800'
      case 'guide': return 'bg-green-100 text-green-800'
      case 'story': return 'bg-purple-100 text-purple-800'
      case 'faq': return 'bg-yellow-100 text-yellow-800'
      case 'news': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Sidebar */}
        <div className="lg:col-span-1">
          <div className="space-y-6">
            {/* Categories */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Categories</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {categories.map(category => (
                    <button
                      key={category.id}
                      onClick={() => setSelectedCategory(category.id)}
                      className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors ${
                        selectedCategory === category.id
                          ? 'bg-primary-100 text-primary-800 font-medium'
                          : 'text-gray-600 hover:bg-gray-100'
                      }`}
                    >
                      {category.name}
                    </button>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Quick Links */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Quick Links</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Link href="/resources/posh-act" className="block text-sm text-primary-600 hover:text-primary-700">
                    POSH Act Guidelines
                  </Link>
                  <Link href="/resources/maternity-benefits" className="block text-sm text-primary-600 hover:text-primary-700">
                    Maternity Benefits
                  </Link>
                  <Link href="/resources/transfer-policies" className="block text-sm text-primary-600 hover:text-primary-700">
                    Transfer Policies
                  </Link>
                  <Link href="/resources/grievance-redressal" className="block text-sm text-primary-600 hover:text-primary-700">
                    Grievance Redressal
                  </Link>
                  <Link href="/resources/career-development" className="block text-sm text-primary-600 hover:text-primary-700">
                    Career Development
                  </Link>
                </div>
              </CardContent>
            </Card>

            {/* Recent Updates */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Recent Updates</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {recentResources.map(resource => (
                    <div key={resource.id} className="text-sm">
                      <Link href={`/resources/${resource.id}`} className="font-medium text-gray-900 hover:text-primary-600">
                        {resource.title}
                      </Link>
                      <p className="text-xs text-gray-500 mt-1">
                        {resource.publishDate.toLocaleDateString()}
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Bookmarks */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Bookmarked</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {bookmarkedItems.length > 0 ? (
                    bookmarkedItems.map(id => {
                      const resource = mockResources.find(r => r.id === id)
                      return resource ? (
                        <Link
                          key={id}
                          href={`/resources/${id}`}
                          className="block text-sm text-primary-600 hover:text-primary-700"
                        >
                          {resource.title}
                        </Link>
                      ) : null
                    })
                  ) : (
                    <p className="text-sm text-gray-500">No bookmarks yet</p>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-3">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Resource Hub</h1>
            <p className="text-gray-600 mt-1">
              Access policies, guides, success stories, and the latest updates
            </p>
          </div>

          {/* Search */}
          <Card className="mb-8">
            <CardContent className="p-4">
              <div className="relative">
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search resources..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </CardContent>
          </Card>

          {/* Featured Content */}
          {searchTerm === '' && selectedCategory === 'all' && (
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Featured Content</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {featuredResources.map(resource => (
                  <Card key={resource.id} className="hover:shadow-lg transition-shadow cursor-pointer group">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getTypeColor(resource.type)}`}>
                              {resource.type}
                            </span>
                            <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                              Featured
                            </span>
                          </div>
                          <CardTitle className="text-lg group-hover:text-primary-600 transition-colors">
                            {resource.title}
                          </CardTitle>
                        </div>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={(e) => {
                            e.preventDefault()
                            toggleBookmark(resource.id)
                          }}
                          className="flex-shrink-0"
                        >
                          <BookmarkIcon className={`h-4 w-4 ${bookmarkedItems.includes(resource.id) ? 'fill-current text-yellow-500' : ''}`} />
                        </Button>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="mb-4">
                        {resource.summary}
                      </CardDescription>
                      <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                        <div className="flex items-center space-x-4">
                          <div className="flex items-center">
                            <ClockIcon className="h-4 w-4 mr-1" />
                            {resource.readTime}
                          </div>
                          <div className="flex items-center">
                            <EyeIcon className="h-4 w-4 mr-1" />
                            {resource.views}
                          </div>
                          <div className="flex items-center">
                            <StarIcon className="h-4 w-4 mr-1 fill-current text-yellow-500" />
                            {resource.rating}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center justify-between">
                        <div className="text-xs text-gray-500">
                          <p>By {resource.author}</p>
                          <p>{resource.publishDate.toLocaleDateString()}</p>
                        </div>
                        <Link href={`/resources/${resource.id}`}>
                          <Button size="sm">Read More</Button>
                        </Link>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}

          {/* All Resources or Search Results */}
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              {searchTerm || selectedCategory !== 'all' ? 'Search Results' : 'All Resources'}
              <span className="text-base font-normal text-gray-500 ml-2">
                ({filteredResources.length} {filteredResources.length === 1 ? 'result' : 'results'})
              </span>
            </h2>
            
            <div className="space-y-4">
              {filteredResources.map(resource => (
                <Card key={resource.id} className="hover:shadow-md transition-shadow cursor-pointer group">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getTypeColor(resource.type)}`}>
                            {resource.type}
                          </span>
                          {resource.isFeatured && (
                            <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                              Featured
                            </span>
                          )}
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition-colors mb-2">
                          {resource.title}
                        </h3>
                        <p className="text-gray-600 mb-4">{resource.summary}</p>
                        <div className="flex items-center space-x-6 text-sm text-gray-500">
                          <div className="flex items-center">
                            <UserIcon className="h-4 w-4 mr-1" />
                            {resource.author}
                          </div>
                          <div className="flex items-center">
                            <CalendarIcon className="h-4 w-4 mr-1" />
                            {resource.publishDate.toLocaleDateString()}
                          </div>
                          <div className="flex items-center">
                            <ClockIcon className="h-4 w-4 mr-1" />
                            {resource.readTime}
                          </div>
                          <div className="flex items-center">
                            <EyeIcon className="h-4 w-4 mr-1" />
                            {resource.views}
                          </div>
                          <div className="flex items-center">
                            <StarIcon className="h-4 w-4 mr-1 fill-current text-yellow-500" />
                            {resource.rating}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2 ml-4">
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={(e) => {
                            e.preventDefault()
                            toggleBookmark(resource.id)
                          }}
                        >
                          <BookmarkIcon className={`h-4 w-4 ${bookmarkedItems.includes(resource.id) ? 'fill-current text-yellow-500' : ''}`} />
                        </Button>
                        <Link href={`/resources/${resource.id}`}>
                          <Button size="sm">Read</Button>
                        </Link>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {filteredResources.length === 0 && (
              <div className="text-center py-12">
                <BookmarkIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No resources found</h3>
                <p className="text-gray-500">
                  Try adjusting your search terms or browse different categories.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
