'use client'

import { useState } from 'react'
import { Dialog, DialogPanel } from '@headlessui/react'
import { Button } from '@/components/ui/button'
import { ExclamationTriangleIcon, PhoneIcon } from '@heroicons/react/24/outline'

export function EmergencyButton() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      {/* Floating Emergency Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 z-50 bg-red-600 hover:bg-red-700 text-white rounded-full p-4 shadow-lg transition-all duration-200 transform hover:scale-105"
        aria-label="Emergency SOS"
      >
        <span className="text-sm font-bold">🆘</span>
      </button>

      {/* Emergency Modal */}
      <Dialog open={isOpen} onClose={setIsOpen} className="relative z-50">
        <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
        
        <div className="fixed inset-0 flex w-screen items-center justify-center p-4">
          <DialogPanel className="max-w-lg space-y-4 bg-white p-6 rounded-lg shadow-xl">
            <div className="flex items-center space-x-3">
              <ExclamationTriangleIcon className="h-8 w-8 text-red-600" />
              <h2 className="text-lg font-semibold text-gray-900">
                Emergency Assistance
              </h2>
            </div>
            
            <p className="text-gray-600">
              Are you in immediate danger or need urgent help?
            </p>
            
            <div className="space-y-3">
              <Button 
                className="w-full bg-red-600 hover:bg-red-700"
                onClick={() => {
                  // In a real app, this would call emergency services
                  window.open('tel:100', '_self')
                }}
              >
                <PhoneIcon className="h-4 w-4 mr-2" />
                Call Security Helpline
              </Button>
              
              <Button 
                variant="outline"
                className="w-full"
                onClick={() => {
                  // Navigate to anonymous reporting
                  setIsOpen(false)
                  // In a real app: router.push('/chat?anonymous=true&emergency=true')
                }}
              >
                Anonymous Report
              </Button>
              
              <Button 
                variant="ghost"
                className="w-full"
                onClick={() => setIsOpen(false)}
              >
                Cancel
              </Button>
            </div>
            
            <div className="text-xs text-gray-500 text-center">
              Your safety is our priority. All reports are confidential.
            </div>
          </DialogPanel>
        </div>
      </Dialog>
    </>
  )
}
