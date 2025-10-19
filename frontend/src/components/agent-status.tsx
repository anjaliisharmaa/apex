'use client'

import { useState, useEffect } from 'react'
import { 
  HeartIcon, 
  ScaleIcon, 
  DocumentTextIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon
} from '@heroicons/react/24/outline'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { apiClient } from '@/lib/api'

interface AgentStatus {
  name: string
  status: 'online' | 'busy' | 'offline'
  specialization: string
  icon: React.ComponentType<any>
  color: string
  description: string
}

const agentConfigs: AgentStatus[] = [
  {
    name: 'ASHA',
    specialization: 'Harassment Support & Advocacy',
    icon: HeartIcon,
    color: 'text-pink-600',
    status: 'online',
    description: 'Specialized in workplace harassment support, complaint handling, and victim advocacy'
  },
  {
    name: 'Athena',
    specialization: 'Legal Documentation & Compliance',
    icon: ScaleIcon,
    color: 'text-blue-600',
    status: 'online',
    description: 'Expert in legal document generation, policy compliance, and regulatory guidance'
  },
  {
    name: 'Scribe',
    specialization: 'Employment Documentation',
    icon: DocumentTextIcon,
    color: 'text-green-600',
    status: 'online',
    description: 'Focused on employment forms, applications, and comprehensive documentation services'
  }
]

export function AgentStatus() {
  const [agents, setAgents] = useState<AgentStatus[]>(agentConfigs)
  const [isLoading, setIsLoading] = useState(true)
  // Using the singleton API client

  useEffect(() => {
    checkAgentStatus()
    // Check agent status every 30 seconds
    const interval = setInterval(checkAgentStatus, 30000)
    return () => clearInterval(interval)
  }, [])

  const checkAgentStatus = async () => {
    try {
      // In a real implementation, you'd have an endpoint to check agent status
      // For now, we'll simulate checking by making a health check call
      const response = await apiClient.healthCheck()
      
      // Update agent status based on API response
      setAgents(prevAgents => 
        prevAgents.map(agent => ({
          ...agent,
          status: response.status === 'healthy' ? 'online' : 'offline'
        }))
      )
    } catch (error) {
      console.error('Error checking agent status:', error)
      // Set agents as offline if API is not reachable
      setAgents(prevAgents => 
        prevAgents.map(agent => ({
          ...agent,
          status: 'offline'
        }))
      )
    } finally {
      setIsLoading(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'online':
        return <CheckCircleIcon className="h-4 w-4 text-green-500" />
      case 'busy':
        return <ExclamationTriangleIcon className="h-4 w-4 text-yellow-500" />
      case 'offline':
        return <XCircleIcon className="h-4 w-4 text-red-500" />
      default:
        return <XCircleIcon className="h-4 w-4 text-gray-400" />
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'online':
        return { text: 'Available', color: 'text-green-600' }
      case 'busy':
        return { text: 'Busy', color: 'text-yellow-600' }
      case 'offline':
        return { text: 'Offline', color: 'text-red-600' }
      default:
        return { text: 'Unknown', color: 'text-gray-600' }
    }
  }

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Agent Status</CardTitle>
          <CardDescription>Checking agent availability...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse space-y-3">
            {[1, 2, 3].map(i => (
              <div key={i} className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gray-200 rounded-full"></div>
                <div className="flex-1">
                  <div className="w-24 h-4 bg-gray-200 rounded mb-1"></div>
                  <div className="w-32 h-3 bg-gray-100 rounded"></div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">AI Agent Status</CardTitle>
        <CardDescription>
          Real-time status of APEX AI agents
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {agents.map((agent) => {
            const IconComponent = agent.icon
            const statusInfo = getStatusText(agent.status)
            
            return (
              <div key={agent.name} className="flex items-start space-x-3 p-3 rounded-lg border border-gray-100 hover:bg-gray-50 transition-colors">
                <div className={`flex-shrink-0 ${agent.color}`}>
                  <IconComponent className="h-6 w-6" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h3 className="font-medium text-gray-900">{agent.name}</h3>
                    <div className="flex items-center space-x-1">
                      {getStatusIcon(agent.status)}
                      <span className={`text-sm font-medium ${statusInfo.color}`}>
                        {statusInfo.text}
                      </span>
                    </div>
                  </div>
                  <p className="text-sm font-medium text-gray-600 mt-1">
                    {agent.specialization}
                  </p>
                  <p className="text-xs text-gray-500 mt-1 leading-relaxed">
                    {agent.description}
                  </p>
                </div>
              </div>
            )
          })}
        </div>
        
        {/* System Status Summary */}
        <div className="mt-6 pt-4 border-t border-gray-100">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">System Status:</span>
            <div className="flex items-center space-x-1">
              {agents.every(agent => agent.status === 'online') ? (
                <>
                  <CheckCircleIcon className="h-4 w-4 text-green-500" />
                  <span className="text-green-600 font-medium">All Systems Operational</span>
                </>
              ) : agents.some(agent => agent.status === 'online') ? (
                <>
                  <ExclamationTriangleIcon className="h-4 w-4 text-yellow-500" />
                  <span className="text-yellow-600 font-medium">Partial Service</span>
                </>
              ) : (
                <>
                  <XCircleIcon className="h-4 w-4 text-red-500" />
                  <span className="text-red-600 font-medium">Service Unavailable</span>
                </>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}