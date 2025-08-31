'use client'

import { useState } from 'react'
import { Switch } from '@headlessui/react'
import { LockClosedIcon } from '@heroicons/react/24/outline'
import { cn } from '@/lib/utils'

export function AnonymousToggle() {
  const [isAnonymous, setIsAnonymous] = useState(false)

  return (
    <div className="flex items-center space-x-2">
      <Switch
        checked={isAnonymous}
        onChange={setIsAnonymous}
        className={cn(
          "relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2",
          isAnonymous ? "bg-purple-600" : "bg-gray-300"
        )}
      >
        <span
          className={cn(
            "inline-block h-4 w-4 transform rounded-full bg-white transition-transform",
            isAnonymous ? "translate-x-6" : "translate-x-1"
          )}
        />
      </Switch>
      <div className="flex items-center space-x-1">
        <LockClosedIcon className="h-4 w-4 text-gray-500" />
        <span className="text-sm text-gray-700">
          {isAnonymous ? "Anonymous" : "Standard"}
        </span>
      </div>
      
      {isAnonymous && (
        <div className="fixed top-16 left-0 right-0 bg-purple-600 text-white px-4 py-2 text-center text-sm z-40">
          🔒 Anonymous Mode Active - Your identity is protected
        </div>
      )}
    </div>
  )
}
