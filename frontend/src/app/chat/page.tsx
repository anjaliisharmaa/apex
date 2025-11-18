'use client'

import { useState, useRef, useEffect } from 'react'
import { 
  PaperClipIcon, 
  PaperAirplaneIcon,
  PlusIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  CpuChipIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'
import { AgentStatus } from '@/components/agent-status'
import { apiClient, formatAgentName, getWorkflowDescription, getIntentColor, type ChatResponse } from '@/lib/api'

interface Message {
  id: string
  content: string
  sender: 'user' | 'ai'
  timestamp: Date
  type?: 'text' | 'buttons' | 'file'
  buttons?: { label: string; action: string }[]
  // Enhanced for orchestrator integration
  agentUsed?: string
  workflowType?: string
  conversationState?: string
  intentAnalysis?: {
    primary_intent: string
    confidence: number
    needs_multiple_agents: boolean
  }
  individualResponses?: Array<{
    success: boolean
    response: string
    agent_used: string
  }>
}

interface Conversation {
  id: string
  title: string
  lastMessage: string
  timestamp: Date
  isAnonymous: boolean
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: 'Hello! I\'m APEX, your intelligent legal assistant powered by specialized AI agents. I coordinate with legal experts (Athena), emotional support specialists (ASHA), and document generators (Scribe) to provide comprehensive help. How can I assist you today?',
      sender: 'ai',
      timestamp: new Date(),
      agentUsed: 'orchestrator',
      workflowType: 'greeting'
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null)
  const [isAnonymous, setIsAnonymous] = useState(true)
  const [conversations] = useState<Conversation[]>([
    {
      id: '1',
      title: 'Maternity Leave Query',
      lastMessage: 'Thank you for the information...',
      timestamp: new Date(Date.now() - 86400000),
      isAnonymous: false
    },
    {
      id: '2',
      title: 'Workplace Concern',
      lastMessage: 'I need to report an incident...',
      timestamp: new Date(Date.now() - 172800000),
      isAnonymous: true
    },
    {
      id: '3',
      title: 'Transfer Request Help',
      lastMessage: 'What documents do I need...',
      timestamp: new Date(Date.now() - 259200000),
      isAnonymous: false
    }
  ])

  const messagesEndRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!inputValue.trim()) return

    const newMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, newMessage])
    const messageContent = inputValue
    setInputValue('')
    setIsLoading(true)

    try {
      // Send message to orchestrator backend
      const response: ChatResponse = await apiClient.sendChatMessage({
        message: messageContent,
        conversation_id: currentConversationId || undefined,
        anonymous: isAnonymous
      })

      console.log('Received chat response:', response); // Debug log

      // Update conversation ID if this is the first message
      if (!currentConversationId) {
        setCurrentConversationId(response.conversation_id)
      }

      const aiResponse: Message = {
        id: response.conversation_id + '_' + Date.now(),
        content: response.response,
        sender: 'ai',
        timestamp: new Date(),
        agentUsed: response.agent_used,
        workflowType: response.workflow_type || 'single_agent',
        conversationState: response.conversation_state || 'greeting',
        intentAnalysis: response.intent_analysis || {
          primary_intent: 'general',
          confidence: 0.5,
          needs_multiple_agents: false
        },
        individualResponses: response.individual_responses || [],
        type: shouldShowButtons(messageContent, response) ? 'buttons' : 'text',
        buttons: shouldShowButtons(messageContent, response) ? generateActionButtons(messageContent, response) : undefined
      }

      setMessages(prev => [...prev, aiResponse])
    } catch (error) {
      console.error('Error sending message:', error)
      
      // More detailed error message based on error type
      let errorMessage = 'I apologize, but I\'m having trouble connecting to my backend services right now. Please try again in a moment.'
      
      if (error instanceof Error) {
        console.error('Detailed error:', error.message)
        if (error.message.includes('response format') || error.message.includes('structure')) {
          errorMessage = 'Unexpected response format from API. The response structure has changed.'
        } else if (error.message.includes('404')) {
          errorMessage = 'Service endpoint not found. Please check if the backend is running.'
        } else if (error.message.includes('500')) {
          errorMessage = 'Internal server error. The backend service encountered an issue.'
        }
      }
      
      // Fallback error message
      const errorResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: errorMessage,
        sender: 'ai',
        timestamp: new Date(),
        agentUsed: 'error',
        workflowType: 'error'
      }

      setMessages(prev => [...prev, errorResponse])
    } finally {
      setIsLoading(false)
    }
  }

  const shouldShowButtons = (userMessage: string, response: ChatResponse): boolean => {
    const message = userMessage.toLowerCase()
    return (
      message.includes('harassment') || 
      message.includes('complaint') ||
      message.includes('posh') ||
      response.intent_analysis?.needs_multiple_agents ||
      response.workflow_type === 'multi_agent'
    )
  }

  const generateActionButtons = (userMessage: string, response: ChatResponse) => {
    const message = userMessage.toLowerCase()
    
    if (message.includes('harassment') || message.includes('complaint') || message.includes('posh')) {
      return [
        { label: 'Learn my legal rights (POSH Act)', action: 'legal_rights' },
        { label: 'File a formal complaint', action: 'file_complaint' },
        { label: 'Contact emotional support', action: 'counselor' },
        { label: 'Generate complaint letter', action: 'generate_complaint' }
      ]
    }
    
    if (message.includes('maternity')) {
      return [
        { label: 'Check maternity rights', action: 'maternity_rights' },
        { label: 'Generate leave application', action: 'generate_maternity_app' },
        { label: 'Get emotional support', action: 'maternity_support' },
        { label: 'View benefits calculator', action: 'benefits_calc' }
      ]
    }
    
    if (response.workflow_type === 'multi_agent') {
      return [
        { label: 'Get more legal details', action: 'more_legal' },
        { label: 'Access emotional support', action: 'emotional_help' },
        { label: 'Generate documents', action: 'create_docs' },
        { label: 'View related resources', action: 'resources' }
      ]
    }
    
    return undefined
  }



  const handleButtonClick = async (action: string) => {
    let message = ''
    
    switch (action) {
      case 'legal_rights':
        message = "Please provide detailed information about my legal rights under the POSH Act"
        break
      case 'file_complaint':
        message = "I need help filing a formal complaint. Can you guide me through the process?"
        break
      case 'counselor':
      case 'emotional_help':
        message = "I need emotional support and counseling for my workplace situation"
        break
      case 'generate_complaint':
        message = "Please generate a formal complaint letter for workplace harassment"
        break
      case 'maternity_rights':
        message = "What are my complete maternity leave rights and benefits?"
        break
      case 'generate_maternity_app':
        message = "Generate a maternity leave application for me"
        break
      case 'maternity_support':
        message = "I need emotional support during my pregnancy and maternity leave"
        break
      case 'more_legal':
        message = "I need more detailed legal information about my situation"
        break
      case 'create_docs':
        message = "Help me create the necessary documents for my case"
        break
      case 'resources':
        message = "Show me relevant resources and information for my situation"
        break
      default:
        message = `Help me with: ${action.replace('_', ' ')}`
    }
    
    // Simulate clicking the message by setting input and sending
    setInputValue(message)
    
    // Auto-send the message
    setTimeout(() => {
      sendMessage()
    }, 100)
  }

  const handleFileUpload = () => {
    fileInputRef.current?.click()
  }

  const quickActions = [
    'I\'m being harassed at work and need comprehensive help',
    'What are my maternity leave rights and how do I apply?',
    'I need both legal advice and emotional support for my situation',
    'Generate a workplace complaint letter with legal guidance',
    'Help me understand my transfer rights and create documents',
    'I\'m facing workplace discrimination - what are my options?'
  ]

  return (
    <div className="flex h-full">
      {/* Sidebar */}
      <div className={`bg-white border-r border-gray-200 transition-all duration-300 ${
        sidebarOpen ? 'w-80' : 'w-0'
      } overflow-hidden`}>
        <div className="p-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-gray-900">Conversations</h2>
            <Button size="icon" variant="ghost">
              <PlusIcon className="h-4 w-4" />
            </Button>
          </div>
          
          <div className="space-y-2 mb-4">
            <Button variant="outline" size="sm" className="w-full justify-start">
              All
            </Button>
            <Button variant="ghost" size="sm" className="w-full justify-start">
              Anonymous
            </Button>
            <Button variant="ghost" size="sm" className="w-full justify-start">
              Recent
            </Button>
          </div>

          <div className="space-y-2">
            {conversations.map((conv) => (
              <Card key={conv.id} className="p-3 cursor-pointer hover:bg-gray-50">
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium text-sm text-gray-900 truncate">
                      {conv.title}
                    </h3>
                    <p className="text-xs text-gray-500 truncate mt-1">
                      {conv.lastMessage}
                    </p>
                    <p className="text-xs text-gray-400 mt-1">
                      {typeof window !== 'undefined' ? conv.timestamp.toLocaleDateString() : ''}
                    </p>
                  </div>
                  {conv.isAnonymous && (
                    <span className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">
                      Anonymous
                    </span>
                  )}
                </div>
              </Card>
            ))}
          </div>
          
          {/* Agent Status */}
          <div className="mt-6">
            <AgentStatus />
          </div>
        </div>
      </div>

      {/* Toggle Sidebar Button */}
      <Button
        variant="ghost"
        size="icon"
        className="absolute left-2 top-20 z-10"
        onClick={() => setSidebarOpen(!sidebarOpen)}
      >
        {sidebarOpen ? (
          <ChevronLeftIcon className="h-4 w-4" />
        ) : (
          <ChevronRightIcon className="h-4 w-4" />
        )}
      </Button>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="bg-white border-b border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="font-semibold text-gray-900">APEX AI Assistant</h1>
              <p className="text-sm text-green-600">● Orchestrator Online</p>
            </div>
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                <label htmlFor="anonymous-toggle" className="text-sm text-gray-600">
                  Anonymous Mode
                </label>
                <button
                  id="anonymous-toggle"
                  onClick={() => setIsAnonymous(!isAnonymous)}
                  className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors ${
                    isAnonymous ? 'bg-purple-600' : 'bg-gray-300'
                  }`}
                >
                  <span
                    className={`inline-block h-3 w-3 transform rounded-full bg-white transition-transform ${
                      isAnonymous ? 'translate-x-5' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
              {currentConversationId && (
                <span className="text-xs text-gray-500">
                  Session: {currentConversationId.slice(-8)}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-md px-4 py-2 rounded-lg ${
                message.sender === 'user' 
                  ? 'bg-primary-600 text-white' 
                  : 'bg-white border border-gray-200 text-gray-900'
              }`}>
                {/* Agent and Workflow Info for AI messages */}
                {message.sender === 'ai' && message.agentUsed && (
                  <div className="flex items-center space-x-2 mb-2 text-xs">
                    <CpuChipIcon className="h-3 w-3" />
                    <span className={getIntentColor(message.intentAnalysis?.primary_intent)}>
                      {formatAgentName(message.agentUsed)}
                    </span>
                    {message.workflowType && (
                      <>
                        <span className="text-gray-400">•</span>
                        <span className="text-gray-600">
                          {getWorkflowDescription(message.workflowType)}
                        </span>
                      </>
                    )}
                    {message.intentAnalysis?.needs_multiple_agents && (
                      <CheckCircleIcon className="h-3 w-3 text-green-500" title="Multi-agent coordination" />
                    )}
                  </div>
                )}
                
                <p className="text-sm">{message.content}</p>
                
                {/* Individual responses for multi-agent workflows */}
                {message.individualResponses && message.individualResponses.length > 1 && (
                  <div className="mt-3 p-2 bg-gray-50 rounded text-xs">
                    <p className="font-medium text-gray-700 mb-1">Specialist Contributions:</p>
                    {message.individualResponses.map((resp, index) => (
                      <div key={index} className="flex items-center space-x-1 text-gray-600">
                        <span className="w-2 h-2 bg-green-400 rounded-full"></span>
                        <span>{formatAgentName(resp.agent_used)}</span>
                      </div>
                    ))}
                  </div>
                )}
                
                {message.buttons && (
                  <div className="mt-3 space-y-2">
                    {message.buttons.map((button, index) => (
                      <Button
                        key={index}
                        variant="outline"
                        size="sm"
                        className="w-full text-left justify-start bg-white"
                        onClick={() => handleButtonClick(button.action)}
                      >
                        {button.label}
                      </Button>
                    ))}
                  </div>
                )}
                
                <div className="flex items-center justify-between mt-1">
                  <p className="text-xs opacity-70">
                    {typeof window !== 'undefined' ? message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''}
                  </p>
                  {message.intentAnalysis && (
                    <p className="text-xs opacity-60">
                      {Math.round(message.intentAnalysis.confidence * 100)}% confidence
                    </p>
                  )}
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 rounded-lg px-4 py-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Actions */}
        {messages.length === 1 && (
          <div className="px-4 py-2 border-t border-gray-200 bg-gray-50">
            <p className="text-sm text-gray-600 mb-2">Quick actions:</p>
            <div className="flex flex-wrap gap-2">
              {quickActions.map((action, index) => (
                <Button
                  key={index}
                  variant="outline"
                  size="sm"
                  onClick={() => setInputValue(action)}
                  className="text-xs"
                >
                  {action}
                </Button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="bg-white border-t border-gray-200 p-4">
          <div className="flex items-end space-x-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={handleFileUpload}
              className="flex-shrink-0"
            >
              <PaperClipIcon className="h-4 w-4" />
            </Button>
            
            <div className="flex-1">
              <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
                placeholder="Type your message..."
                className="resize-none"
              />
            </div>
            
            <Button
              onClick={sendMessage}
              disabled={!inputValue.trim() || isLoading}
              className="flex-shrink-0"
            >
              <PaperAirplaneIcon className="h-4 w-4" />
            </Button>
          </div>
          
          <p className="text-xs text-gray-500 mt-2 text-center">
            Your conversations are confidential and secure
          </p>
        </div>

        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          onChange={(e) => {
            // Handle file upload
            console.log('File selected:', e.target.files?.[0])
          }}
        />
      </div>
    </div>
  )
}
