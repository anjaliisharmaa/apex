'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { 
  ChatBubbleLeftIcon,
  HomeIcon,
  DocumentIcon,
  FolderIcon,
  BookOpenIcon,
  UserIcon,
  BellIcon,
  Bars3Icon,
  XMarkIcon,
  ShieldExclamationIcon,
  CogIcon,
  UserGroupIcon
} from '@heroicons/react/24/outline'
import { AnonymousToggle } from './anonymous-toggle'
import { EmergencyButton } from './emergency-button'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Chat', href: '/chat', icon: ChatBubbleLeftIcon },
  { name: 'Cases', href: '/cases', icon: FolderIcon },
  { name: 'Forms', href: '/forms', icon: DocumentIcon },
  { name: 'Community', href: '/community', icon: UserGroupIcon },
  { name: 'Resources', href: '/resources', icon: BookOpenIcon },
  { name: 'Admin Portal', href: '/admin', icon: CogIcon },
]

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const pathname = usePathname()

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between items-center">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/dashboard" className="flex items-center space-x-2">
              <ShieldExclamationIcon className="h-8 w-8 text-primary-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">Apex</h1>
                <p className="text-xs text-gray-500 hidden sm:block">Your Confidential Companion</p>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            {navigation.map((item) => {
              const isActive = pathname === item.href
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    "inline-flex items-center px-1 pt-1 text-sm font-medium border-b-2 transition-colors",
                    isActive
                      ? "border-primary-500 text-primary-600"
                      : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700"
                  )}
                >
                  <item.icon className="h-4 w-4 mr-2" />
                  {item.name}
                </Link>
              )
            })}
          </nav>

          {/* Right side actions */}
          <div className="flex items-center space-x-4">
            {/* Anonymous Toggle */}
            <AnonymousToggle />
            
            {/* Notifications */}
            <Button variant="ghost" size="icon" className="relative">
              <BellIcon className="h-5 w-5" />
              <span className="absolute -top-1 -right-1 h-3 w-3 bg-red-500 rounded-full"></span>
            </Button>

            {/* User Menu */}
            <Button variant="ghost" size="icon">
              <UserIcon className="h-5 w-5" />
            </Button>

            {/* Mobile menu button */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? (
                <XMarkIcon className="h-6 w-6" />
              ) : (
                <Bars3Icon className="h-6 w-6" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden">
            <div className="pt-2 pb-3 space-y-1">
              {navigation.map((item) => {
                const isActive = pathname === item.href
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={cn(
                      "block pl-3 pr-4 py-2 text-base font-medium border-l-4",
                      isActive
                        ? "border-primary-500 text-primary-600 bg-primary-50"
                        : "border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50 hover:border-gray-300"
                    )}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <div className="flex items-center">
                      <item.icon className="h-5 w-5 mr-3" />
                      {item.name}
                    </div>
                  </Link>
                )
              })}
            </div>
          </div>
        )}
      </div>

      {/* Emergency Button */}
      <EmergencyButton />
    </header>
  )
}
