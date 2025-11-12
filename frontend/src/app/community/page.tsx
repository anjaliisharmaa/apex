'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { apiClient, type ForumData } from '@/lib/api';
import {
  UserGroupIcon,
  LockClosedIcon,
  PlusIcon,
  MagnifyingGlassIcon,
  ClockIcon,
  ChatBubbleLeftIcon,
  SparklesIcon,
  HeartIcon,
  BriefcaseIcon,
  AcademicCapIcon,
  ShieldCheckIcon,
} from '@heroicons/react/24/outline';

export default function CommunityPage() {
  const [forums, setForums] = useState<ForumData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newForum, setNewForum] = useState({
    name: '',
    description: '',
    is_private: false,
    category: 'general'
  });
  const router = useRouter();

  useEffect(() => {
    const loadForums = async () => {
      try {
        setIsLoading(true);

        if (!apiClient.isAuthenticated()) {
          router.push('/login');
          return;
        }

        const forumsData = await apiClient.getCommunityForums();
        setForums(forumsData.forums);

      } catch (error) {
        console.error('Failed to load forums:', error);
        if (error instanceof Error && error.message.includes('401')) {
          router.push('/login');
        }
      } finally {
        setIsLoading(false);
      }
    };

    loadForums();
  }, [router]);

  const getCategoryIcon = (category: string) => {
    const icons = {
      general: ChatBubbleLeftIcon,
      support: HeartIcon,
      wellness: SparklesIcon,
      professional: BriefcaseIcon,
    };
    const IconComponent = icons[category as keyof typeof icons] || ChatBubbleLeftIcon;
    return <IconComponent className="h-5 w-5" />;
  };

  const getCategoryColor = (category: string) => {
    const colors = {
      general: 'bg-blue-100 text-blue-800',
      support: 'bg-pink-100 text-pink-800',
      wellness: 'bg-green-100 text-green-800',
      professional: 'bg-purple-100 text-purple-800',
    };
    return colors[category as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  const filteredForums = forums.filter(forum => {
    const matchesSearch = forum.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         forum.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || forum.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleCreateForum = async () => {
    try {
      if (!newForum.name.trim()) {
        alert('Please enter a forum name');
        return;
      }

      await apiClient.createForum(newForum);
      
      // Reload forums
      const forumsData = await apiClient.getCommunityForums();
      setForums(forumsData.forums);
      
      // Reset form
      setNewForum({
        name: '',
        description: '',
        is_private: false,
        category: 'general'
      });
      setShowCreateForm(false);
      
    } catch (error) {
      console.error('Failed to create forum:', error);
      alert('Failed to create forum. Please try again.');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Community Forums</h1>
              <p className="text-lg text-gray-600">Connect, share, and support each other</p>
            </div>
            <Button 
              onClick={() => setShowCreateForm(true)}
              className="bg-blue-600 hover:bg-blue-700"
            >
              <PlusIcon className="h-4 w-4 mr-2" />
              Create Forum
            </Button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search and Filters */}
        <div className="mb-8 flex flex-col lg:flex-row gap-4">
          {/* Search Bar */}
          <div className="flex-1 relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search forums by name or description..."
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          {/* Category Filters */}
          <div className="flex space-x-2">
            {['all', 'general', 'support', 'wellness', 'professional'].map((category) => (
              <Button
                key={category}
                variant={selectedCategory === category ? 'default' : 'outline'}
                onClick={() => setSelectedCategory(category)}
                className="capitalize"
              >
                {category === 'all' ? 'All Categories' : category}
              </Button>
            ))}
          </div>
        </div>

        {/* Featured Info Banner */}
        <Card className="mb-8 bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
          <CardContent className="p-6">
            <div className="flex items-center space-x-4">
              <div className="flex-shrink-0">
                <UserGroupIcon className="h-12 w-12 text-blue-600" />
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900">Welcome to the APEX Community</h3>
                <p className="text-gray-600">
                  A safe space for women in DRDO to connect, share experiences, and support each other. 
                  You can post anonymously in any forum for privacy.
                </p>
              </div>
              <div className="flex space-x-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-blue-600">{forums.length}</div>
                  <div className="text-xs text-gray-500">Active Forums</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-green-600">
                    {forums.reduce((sum, forum) => sum + forum.member_count, 0)}
                  </div>
                  <div className="text-xs text-gray-500">Total Members</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Forums Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {filteredForums.map((forum) => (
            <Link key={forum.id} href={`/community/forum/${forum.id}`}>
              <Card className="h-full hover:shadow-lg transition-shadow duration-200 cursor-pointer group">
                <CardHeader className="pb-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded-lg ${getCategoryColor(forum.category)}`}>
                        {getCategoryIcon(forum.category)}
                      </div>
                      {forum.is_private && (
                        <LockClosedIcon className="h-4 w-4 text-gray-500" />
                      )}
                    </div>
                    <Badge variant="outline" className={getCategoryColor(forum.category)}>
                      {forum.category}
                    </Badge>
                  </div>
                  <CardTitle className="group-hover:text-blue-600 transition-colors">
                    {forum.name}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                    {forum.description}
                  </p>
                  
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <div className="flex items-center space-x-1">
                      <UserGroupIcon className="h-4 w-4" />
                      <span>{forum.member_count} members</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <ClockIcon className="h-4 w-4" />
                      <span>{new Date(forum.recent_activity).toLocaleDateString()}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>

        {filteredForums.length === 0 && (
          <div className="text-center py-12">
            <UserGroupIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-medium text-gray-900 mb-2">No forums found</h3>
            <p className="text-gray-500 mb-4">
              {searchTerm ? 'No forums match your search criteria.' : 'No forums available in this category.'}
            </p>
            <Button onClick={() => setShowCreateForm(true)}>
              <PlusIcon className="h-4 w-4 mr-2" />
              Create the first forum
            </Button>
          </div>
        )}

        {/* Create Forum Modal */}
        {showCreateForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Create New Forum</h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Forum Name *
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                    value={newForum.name}
                    onChange={(e) => setNewForum({ ...newForum, name: e.target.value })}
                    placeholder="e.g., Women in AI Research"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                    rows={3}
                    value={newForum.description}
                    onChange={(e) => setNewForum({ ...newForum, description: e.target.value })}
                    placeholder="Describe what this forum is about..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Category
                  </label>
                  <select
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                    value={newForum.category}
                    onChange={(e) => setNewForum({ ...newForum, category: e.target.value })}
                  >
                    <option value="general">General</option>
                    <option value="support">Support</option>
                    <option value="wellness">Wellness</option>
                    <option value="professional">Professional</option>
                  </select>
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="private"
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    checked={newForum.is_private}
                    onChange={(e) => setNewForum({ ...newForum, is_private: e.target.checked })}
                  />
                  <label htmlFor="private" className="ml-2 block text-sm text-gray-700">
                    Private forum (invite only)
                  </label>
                </div>
              </div>

              <div className="flex space-x-3 mt-6">
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={() => setShowCreateForm(false)}
                >
                  Cancel
                </Button>
                <Button
                  className="flex-1"
                  onClick={handleCreateForum}
                >
                  Create Forum
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}