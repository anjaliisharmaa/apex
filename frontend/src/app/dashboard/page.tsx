import Link from 'next/link'
import { 
  ChatBubbleLeftIcon,
  DocumentIcon,
  FolderIcon,
  BookOpenIcon,
  ClockIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

export default function DashboardPage() {
  // Mock data - in a real app, this would come from an API
  const stats = {
    activeCases: 3,
    completedCases: 12,
    newNotifications: 2
  }

  const recentActivity = [
    { id: 1, action: 'Maternity Leave Application', status: 'approved', time: '2 hours ago' },
    { id: 2, action: 'Transfer Request', status: 'pending', time: '1 day ago' },
    { id: 3, action: 'Policy Query Response', status: 'completed', time: '3 days ago' },
    { id: 4, action: 'Document Generated', status: 'completed', time: '1 week ago' },
    { id: 5, action: 'Case Update', status: 'info', time: '2 weeks ago' },
  ]

  const quickTips = [
    'Did you know? You can access all POSH Act guidelines in the Resource Hub.',
    'Tip: Use Anonymous Mode for sensitive queries about workplace issues.',
    'New: Child Care Leave policies have been updated. Check Resources for details.',
  ]

  const currentTip = quickTips[0] // In a real app, this could rotate

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Welcome Section */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Welcome back!</h1>
        <p className="text-gray-600 mt-1">
          You have {stats.activeCases} active cases and {stats.newNotifications} new notifications
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Cards Grid */}
        <div className="lg:col-span-2">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Ask a Question Card */}
            <Card className="hover:shadow-lg transition-shadow cursor-pointer group">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-primary-100 rounded-lg group-hover:bg-primary-200 transition-colors">
                    <ChatBubbleLeftIcon className="h-6 w-6 text-primary-600" />
                  </div>
                  <div>
                    <CardTitle className="text-lg">Ask a Question</CardTitle>
                    <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                      24/7 Available
                    </span>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="mb-4">
                  Get instant answers about policies, rights, and procedures
                </CardDescription>
                <Link href="/chat">
                  <Button className="w-full">Start Conversation</Button>
                </Link>
              </CardContent>
            </Card>

            {/* Generate a Form Card */}
            <Card className="hover:shadow-lg transition-shadow cursor-pointer group">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-teal-100 rounded-lg group-hover:bg-teal-200 transition-colors">
                    <DocumentIcon className="h-6 w-6 text-teal-600" />
                  </div>
                  <CardTitle className="text-lg">Generate a Form</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="mb-4">
                  Create official documents and applications
                </CardDescription>
                <div className="space-y-2 mb-4">
                  <Link href="/forms/maternity-leave">
                    <Button variant="outline" size="sm" className="w-full text-left justify-start">
                      Maternity Leave
                    </Button>
                  </Link>
                  <Link href="/forms/transfer-request">
                    <Button variant="outline" size="sm" className="w-full text-left justify-start">
                      Transfer Request
                    </Button>
                  </Link>
                </div>
                <Link href="/forms">
                  <Button variant="ghost" className="w-full">View All Forms</Button>
                </Link>
              </CardContent>
            </Card>

            {/* Track My Cases Card */}
            <Card className="hover:shadow-lg transition-shadow cursor-pointer group">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-purple-100 rounded-lg group-hover:bg-purple-200 transition-colors">
                    <FolderIcon className="h-6 w-6 text-purple-600" />
                  </div>
                  <CardTitle className="text-lg">Track My Cases</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="mb-4">
                  Monitor your submissions and requests
                </CardDescription>
                <div className="flex justify-between text-sm text-gray-600 mb-4">
                  <span>{stats.activeCases} Active</span>
                  <span>{stats.completedCases} Completed</span>
                </div>
                <div className="space-y-2 mb-4">
                  <div className="text-sm">
                    <p className="font-medium">Recent: Maternity Leave App.</p>
                    <p className="text-green-600">Status: Approved</p>
                  </div>
                  <div className="text-sm">
                    <p className="font-medium">Transfer Request #TR-2024-001</p>
                    <p className="text-yellow-600">Status: Under Review</p>
                  </div>
                </div>
                <Link href="/cases">
                  <Button className="w-full">View All Cases</Button>
                </Link>
              </CardContent>
            </Card>

            {/* Resource Hub Card */}
            <Card className="hover:shadow-lg transition-shadow cursor-pointer group">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-orange-100 rounded-lg group-hover:bg-orange-200 transition-colors">
                    <BookOpenIcon className="h-6 w-6 text-orange-600" />
                  </div>
                  <CardTitle className="text-lg">Resource Hub</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="mb-4">
                  Policies, articles, and success stories
                </CardDescription>
                <div className="space-y-2 mb-4">
                  <Link href="/resources/posh-act">
                    <Button variant="ghost" size="sm" className="w-full text-left justify-start">
                      POSH Act Guide
                    </Button>
                  </Link>
                  <Link href="/resources/maternity-benefits">
                    <Button variant="ghost" size="sm" className="w-full text-left justify-start">
                      Maternity Benefits
                    </Button>
                  </Link>
                  <Link href="/resources/recent-updates">
                    <Button variant="ghost" size="sm" className="w-full text-left justify-start">
                      Recent Updates
                    </Button>
                  </Link>
                </div>
                <Link href="/resources">
                  <Button variant="outline" className="w-full">Browse All Resources</Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Recent Activity */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center">
                <ClockIcon className="h-5 w-5 mr-2" />
                Recent Activity
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {recentActivity.map((activity) => (
                  <div key={activity.id} className="flex items-start space-x-3">
                    <div className={`p-1 rounded-full mt-1 ${
                      activity.status === 'approved' ? 'bg-green-100' :
                      activity.status === 'pending' ? 'bg-yellow-100' :
                      activity.status === 'completed' ? 'bg-blue-100' : 'bg-gray-100'
                    }`}>
                      <CheckCircleIcon className={`h-3 w-3 ${
                        activity.status === 'approved' ? 'text-green-600' :
                        activity.status === 'pending' ? 'text-yellow-600' :
                        activity.status === 'completed' ? 'text-blue-600' : 'text-gray-600'
                      }`} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {activity.action}
                      </p>
                      <p className="text-xs text-gray-500">{activity.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Notifications */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Notifications</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="p-3 bg-blue-50 rounded-lg">
                  <p className="text-sm font-medium text-blue-900">
                    New policy update available
                  </p>
                  <p className="text-xs text-blue-700 mt-1">
                    Child Care Leave guidelines updated
                  </p>
                </div>
                <div className="p-3 bg-green-50 rounded-lg">
                  <p className="text-sm font-medium text-green-900">
                    Case approved
                  </p>
                  <p className="text-xs text-green-700 mt-1">
                    Your maternity leave application has been approved
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Quick Tips */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">💡 Quick Tip</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-700">{currentTip}</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
