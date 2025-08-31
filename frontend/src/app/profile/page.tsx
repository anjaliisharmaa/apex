'use client'

import { useState } from 'react'
import { 
  UserIcon,
  ShieldCheckIcon,
  EyeSlashIcon,
  QuestionMarkCircleIcon,
  PencilIcon,
  PhoneIcon,
  EnvelopeIcon,
  BuildingOfficeIcon,
  KeyIcon,
  BellIcon,
  TrashIcon
} from '@heroicons/react/24/outline'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const tabs = [
  { id: 'personal', name: 'Personal Information', icon: UserIcon },
  { id: 'security', name: 'Security Settings', icon: ShieldCheckIcon },
  { id: 'privacy', name: 'Privacy Settings', icon: EyeSlashIcon },
  { id: 'support', name: 'Support', icon: QuestionMarkCircleIcon }
]

export default function ProfilePage() {
  const [activeTab, setActiveTab] = useState('personal')
  const [isEditing, setIsEditing] = useState(false)
  const [profileData, setProfileData] = useState({
    name: 'Dr. Priya Sharma',
    email: 'priya.sharma@drdo.gov.in',
    phone: '+91 98765 43210',
    organization: 'Defence Research and Development Organisation (DRDO)',
    designation: 'Senior Scientific Officer',
    empId: 'DRDO2024001',
    department: 'Electronics & Communication Engineering',
    joiningDate: '2019-06-15',
    emergencyContact: 'Mr. Rajesh Sharma - +91 98765 43211'
  })

  const [securitySettings, setSecuritySettings] = useState({
    twoFactorEnabled: true,
    sessionTimeout: '30',
    loginNotifications: true
  })

  const [privacySettings, setPrivacySettings] = useState({
    anonymousDefault: false,
    dataRetention: '5 years',
    shareAnalytics: true,
    emailNotifications: true,
    smsNotifications: false
  })

  const renderPersonalInfo = () => (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Personal Information</CardTitle>
            <CardDescription>Manage your personal details and contact information</CardDescription>
          </div>
          <Button
            variant="outline"
            onClick={() => setIsEditing(!isEditing)}
          >
            <PencilIcon className="h-4 w-4 mr-2" />
            {isEditing ? 'Cancel' : 'Edit'}
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Full Name
              </label>
              {isEditing ? (
                <Input
                  value={profileData.name}
                  onChange={(e) => setProfileData({...profileData, name: e.target.value})}
                />
              ) : (
                <p className="text-gray-900">{profileData.name}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Employee ID
              </label>
              <p className="text-gray-900">{profileData.empId}</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email Address
              </label>
              <div className="flex items-center">
                <EnvelopeIcon className="h-4 w-4 text-gray-400 mr-2" />
                {isEditing ? (
                  <Input
                    type="email"
                    value={profileData.email}
                    onChange={(e) => setProfileData({...profileData, email: e.target.value})}
                  />
                ) : (
                  <p className="text-gray-900">{profileData.email}</p>
                )}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Phone Number
              </label>
              <div className="flex items-center">
                <PhoneIcon className="h-4 w-4 text-gray-400 mr-2" />
                {isEditing ? (
                  <Input
                    value={profileData.phone}
                    onChange={(e) => setProfileData({...profileData, phone: e.target.value})}
                  />
                ) : (
                  <p className="text-gray-900">{profileData.phone}</p>
                )}
              </div>
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Organization
              </label>
              <div className="flex items-center">
                <BuildingOfficeIcon className="h-4 w-4 text-gray-400 mr-2" />
                <p className="text-gray-900">{profileData.organization}</p>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Designation
              </label>
              <p className="text-gray-900">{profileData.designation}</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Department
              </label>
              <p className="text-gray-900">{profileData.department}</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Joining Date
              </label>
              <p className="text-gray-900">{new Date(profileData.joiningDate).toLocaleDateString()}</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Emergency Contact
              </label>
              {isEditing ? (
                <Input
                  value={profileData.emergencyContact}
                  onChange={(e) => setProfileData({...profileData, emergencyContact: e.target.value})}
                />
              ) : (
                <p className="text-gray-900">{profileData.emergencyContact}</p>
              )}
            </div>
          </div>

          {isEditing && (
            <div className="flex space-x-3">
              <Button onClick={() => setIsEditing(false)}>
                Save Changes
              </Button>
              <Button variant="outline" onClick={() => setIsEditing(false)}>
                Cancel
              </Button>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )

  const renderSecuritySettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Password & Authentication</CardTitle>
          <CardDescription>Manage your password and authentication settings</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Change Password</h4>
                <p className="text-sm text-gray-500">Update your account password</p>
              </div>
              <Button variant="outline">
                <KeyIcon className="h-4 w-4 mr-2" />
                Change Password
              </Button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Two-Factor Authentication</h4>
                <p className="text-sm text-gray-500">Add an extra layer of security</p>
              </div>
              <div className="flex items-center space-x-2">
                <span className={`text-sm ${securitySettings.twoFactorEnabled ? 'text-green-600' : 'text-gray-500'}`}>
                  {securitySettings.twoFactorEnabled ? 'Enabled' : 'Disabled'}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setSecuritySettings({
                    ...securitySettings,
                    twoFactorEnabled: !securitySettings.twoFactorEnabled
                  })}
                >
                  {securitySettings.twoFactorEnabled ? 'Disable' : 'Enable'}
                </Button>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Session Timeout</h4>
                <p className="text-sm text-gray-500">Automatically log out after inactivity</p>
              </div>
              <select
                value={securitySettings.sessionTimeout}
                onChange={(e) => setSecuritySettings({
                  ...securitySettings,
                  sessionTimeout: e.target.value
                })}
                className="border border-gray-300 rounded-md px-3 py-1 text-sm"
              >
                <option value="15">15 minutes</option>
                <option value="30">30 minutes</option>
                <option value="60">1 hour</option>
                <option value="120">2 hours</option>
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Login Activity</CardTitle>
          <CardDescription>Monitor your recent login activity</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <div>
                <p className="font-medium">Current Session</p>
                <p className="text-sm text-gray-500">Windows PC • Chrome • 192.168.1.1</p>
              </div>
              <span className="text-sm text-green-600">Active now</span>
            </div>
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <div>
                <p className="font-medium">Mobile Device</p>
                <p className="text-sm text-gray-500">Android • Firefox • 192.168.1.25</p>
              </div>
              <span className="text-sm text-gray-500">2 hours ago</span>
            </div>
            <div className="flex items-center justify-between py-2">
              <div>
                <p className="font-medium">Office Computer</p>
                <p className="text-sm text-gray-500">Windows PC • Edge • 10.0.0.15</p>
              </div>
              <span className="text-sm text-gray-500">Yesterday</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderPrivacySettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Privacy Preferences</CardTitle>
          <CardDescription>Control how your data is used and stored</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Anonymous Mode Default</h4>
                <p className="text-sm text-gray-500">Start conversations in anonymous mode by default</p>
              </div>
              <input
                type="checkbox"
                checked={privacySettings.anonymousDefault}
                onChange={(e) => setPrivacySettings({
                  ...privacySettings,
                  anonymousDefault: e.target.checked
                })}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Data Retention</h4>
                <p className="text-sm text-gray-500">How long to keep your conversation data</p>
              </div>
              <select
                value={privacySettings.dataRetention}
                onChange={(e) => setPrivacySettings({
                  ...privacySettings,
                  dataRetention: e.target.value
                })}
                className="border border-gray-300 rounded-md px-3 py-1 text-sm"
              >
                <option value="1 year">1 year</option>
                <option value="3 years">3 years</option>
                <option value="5 years">5 years</option>
                <option value="indefinite">Indefinite</option>
              </select>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Share Analytics</h4>
                <p className="text-sm text-gray-500">Help improve Apex by sharing anonymous usage data</p>
              </div>
              <input
                type="checkbox"
                checked={privacySettings.shareAnalytics}
                onChange={(e) => setPrivacySettings({
                  ...privacySettings,
                  shareAnalytics: e.target.checked
                })}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Notification Preferences</CardTitle>
          <CardDescription>Choose how you want to receive notifications</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <EnvelopeIcon className="h-4 w-4 text-gray-400 mr-3" />
                <div>
                  <h4 className="font-medium">Email Notifications</h4>
                  <p className="text-sm text-gray-500">Receive updates via email</p>
                </div>
              </div>
              <input
                type="checkbox"
                checked={privacySettings.emailNotifications}
                onChange={(e) => setPrivacySettings({
                  ...privacySettings,
                  emailNotifications: e.target.checked
                })}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <PhoneIcon className="h-4 w-4 text-gray-400 mr-3" />
                <div>
                  <h4 className="font-medium">SMS Notifications</h4>
                  <p className="text-sm text-gray-500">Receive critical updates via SMS</p>
                </div>
              </div>
              <input
                type="checkbox"
                checked={privacySettings.smsNotifications}
                onChange={(e) => setPrivacySettings({
                  ...privacySettings,
                  smsNotifications: e.target.checked
                })}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Data Management</CardTitle>
          <CardDescription>Download or delete your personal data</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Download Your Data</h4>
                <p className="text-sm text-gray-500">Export all your personal data and conversations</p>
              </div>
              <Button variant="outline">Download</Button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Delete Account</h4>
                <p className="text-sm text-gray-500">Permanently delete your account and all data</p>
              </div>
              <Button variant="destructive">
                <TrashIcon className="h-4 w-4 mr-2" />
                Delete Account
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderSupport = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Contact Support</CardTitle>
          <CardDescription>Get help with any issues or questions</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Subject
              </label>
              <Input placeholder="Brief description of your issue" />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Category
              </label>
              <select className="w-full border border-gray-300 rounded-md px-3 py-2">
                <option>Technical Issue</option>
                <option>Account Problem</option>
                <option>Feature Request</option>
                <option>Privacy Concern</option>
                <option>General Question</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Message
              </label>
              <textarea 
                rows={4}
                className="w-full border border-gray-300 rounded-md px-3 py-2"
                placeholder="Please describe your issue in detail..."
              />
            </div>

            <Button>Submit Support Request</Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Frequently Asked Questions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-900">How do I change my password?</h4>
              <p className="text-sm text-gray-600 mt-1">Go to Security Settings and click on "Change Password". You'll need to enter your current password and choose a new one.</p>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-900">Is my data secure?</h4>
              <p className="text-sm text-gray-600 mt-1">Yes, all data is encrypted and stored securely. We follow government security standards and your conversations are confidential.</p>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-900">How does anonymous mode work?</h4>
              <p className="text-sm text-gray-600 mt-1">In anonymous mode, your conversations are not linked to your profile. This ensures complete privacy for sensitive discussions.</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>User Guide</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <a href="#" className="block text-sm text-primary-600 hover:text-primary-700">Getting Started with Apex</a>
            <a href="#" className="block text-sm text-primary-600 hover:text-primary-700">How to File a Complaint</a>
            <a href="#" className="block text-sm text-primary-600 hover:text-primary-700">Understanding Your Rights</a>
            <a href="#" className="block text-sm text-primary-600 hover:text-primary-700">Using Anonymous Mode</a>
            <a href="#" className="block text-sm text-primary-600 hover:text-primary-700">Generating Forms and Documents</a>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderTabContent = () => {
    switch (activeTab) {
      case 'personal':
        return renderPersonalInfo()
      case 'security':
        return renderSecuritySettings()
      case 'privacy':
        return renderPrivacySettings()
      case 'support':
        return renderSupport()
      default:
        return renderPersonalInfo()
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Profile Settings</h1>
        <p className="text-gray-600 mt-1">Manage your account settings and preferences</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Sidebar Navigation */}
        <div className="lg:col-span-1">
          <nav className="space-y-1">
            {tabs.map(tab => {
              const IconComponent = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                    activeTab === tab.id
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <IconComponent className="h-4 w-4 mr-3" />
                  {tab.name}
                </button>
              )
            })}
          </nav>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-3">
          {renderTabContent()}
        </div>
      </div>
    </div>
  )
}
