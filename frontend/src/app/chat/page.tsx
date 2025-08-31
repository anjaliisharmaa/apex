'use client'

import { useState, useRef, useEffect } from 'react'
import { 
  PaperClipIcon, 
  PaperAirplaneIcon,
  PlusIcon,
  ChevronLeftIcon,
  ChevronRightIcon
} from '@heroicons/react/24/outline'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'

interface Message {
  id: string
  content: string
  sender: 'user' | 'ai'
  timestamp: Date
  type?: 'text' | 'buttons' | 'file'
  buttons?: { label: string; action: string }[]
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
      content: 'Hello! I\'m Apex, your confidential AI companion. I\'m here to help you with policies, rights, procedures, and any workplace concerns. How can I assist you today?',
      sender: 'ai',
      timestamp: new Date(),
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
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
    setInputValue('')
    setIsLoading(true)

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: generateAIResponse(inputValue),
        sender: 'ai',
        timestamp: new Date(),
        type: inputValue.toLowerCase().includes('harassment') || inputValue.toLowerCase().includes('complaint') ? 'buttons' : 'text',
        buttons: inputValue.toLowerCase().includes('harassment') || inputValue.toLowerCase().includes('complaint') ? [
          { label: 'Learn my legal rights (POSH Act)', action: 'legal_rights' },
          { label: 'File a formal complaint', action: 'file_complaint' },
          { label: 'Contact a wellness counselor', action: 'counselor' },
          { label: 'Practice how to respond', action: 'practice' }
        ] : undefined
      }

      setMessages(prev => [...prev, aiResponse])
      setIsLoading(false)
    }, 1500)
  }

  const generateAIResponse = (userMessage: string): string => {
    const message = userMessage.toLowerCase()
    
    if (message.includes('maternity') || message.includes('leave')) {
      return "I can help you with maternity leave information. Under the Maternity Benefit Act, 1961, you're entitled to 26 weeks of paid maternity leave. Would you like me to help you generate a maternity leave application or provide more details about your benefits?"
    }
    
    if (message.includes('transfer')) {
      return "I can assist you with transfer-related queries. There are several types of transfers available including spouse ground transfer, medical ground transfer, and general transfers. What specific information do you need about the transfer process?"
    }
    
    if (message.includes('harassment') || message.includes('complaint')) {
      return "I understand this is a sensitive matter, and I'm here to support you. You have several options available, and everything we discuss is confidential. Here are some ways I can help:"
    }
    
    if (message.includes('policy') || message.includes('rule')) {
      return "I have access to a comprehensive database of government policies and rules. Could you please specify which policy or area you'd like information about? For example: POSH Act, Child Care Leave, Transfer Guidelines, etc."
    }
    
    return "Thank you for your question. I'm here to help with policies, procedures, legal rights, and any workplace concerns. Could you provide more details about what specific information you're looking for?"
  }

  const handleButtonClick = (action: string) => {
    let response = ''
    switch (action) {
      case 'legal_rights':
        response = "Under the POSH Act 2013, you have the right to a workplace free from sexual harassment. Key protections include: 1) Right to file a complaint with the Internal Committee, 2) Right to confidentiality, 3) Protection against retaliation, 4) Right to interim relief during inquiry. Would you like me to generate a formal complaint form or provide more detailed information?"
        break
      case 'file_complaint':
        response = "I can help you prepare a formal complaint. Would you like this to be anonymous? I'll guide you through the process step by step and help you gather all necessary information and documentation."
        break
      case 'counselor':
        response = "I can connect you with confidential counseling resources. Would you prefer: 1) Internal employee assistance program, 2) External professional counselors, or 3) Peer support groups? All options maintain complete confidentiality."
        break
      case 'practice':
        response = "I can help you practice different response scenarios. This can include: 1) How to document incidents, 2) Professional communication scripts, 3) Assertiveness techniques. What specific situation would you like to practice for?"
        break
    }
    
    const aiResponse: Message = {
      id: Date.now().toString(),
      content: response,
      sender: 'ai',
      timestamp: new Date(),
    }
    
    setMessages(prev => [...prev, aiResponse])
  }

  const handleFileUpload = () => {
    fileInputRef.current?.click()
  }

  const quickActions = [
    'How do I apply for maternity leave?',
    'What are my rights under POSH Act?',
    'I need help with a transfer request',
    'How do I report a workplace issue?',
    'What documents do I need for Child Care Leave?'
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
                      {conv.timestamp.toLocaleDateString()}
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
              <h1 className="font-semibold text-gray-900">Apex AI Assistant</h1>
              <p className="text-sm text-green-600">● Online</p>
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
                <p className="text-sm">{message.content}</p>
                
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
                
                <p className="text-xs opacity-70 mt-1">
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </p>
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
