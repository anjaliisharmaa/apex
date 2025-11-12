'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { apiClient, type ForumMessage } from '@/lib/api';
import {
  ArrowLeftIcon,
  ChatBubbleLeftIcon,
  HeartIcon,
  EyeSlashIcon,
  EyeIcon,
  PlusIcon,
  UserIcon,
  ClockIcon,
  PaperAirplaneIcon,
} from '@heroicons/react/24/outline';

export default function ForumPage() {
  const [messages, setMessages] = useState<ForumMessage[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [newMessage, setNewMessage] = useState('');
  const [isAnonymous, setIsAnonymous] = useState(false);
  const [isPosting, setIsPosting] = useState(false);
  const [forumInfo, setForumInfo] = useState<any>(null);
  const router = useRouter();
  const params = useParams();
  
  const forumId = Array.isArray(params.id) ? params.id[0] : params.id;

  useEffect(() => {
    const loadForumData = async () => {
      try {
        setIsLoading(true);

        if (!apiClient.isAuthenticated()) {
          router.push('/login');
          return;
        }

        if (!forumId) {
          router.push('/community');
          return;
        }

        // Load forum info and messages
        const [forumsData, messagesData] = await Promise.all([
          apiClient.getCommunityForums(),
          apiClient.getForumMessages(forumId)
        ]);

        const forum = forumsData.forums.find(f => f.id === forumId);
        setForumInfo(forum);
        setMessages(messagesData.messages);

      } catch (error) {
        console.error('Failed to load forum data:', error);
        if (error instanceof Error && error.message.includes('401')) {
          router.push('/login');
        }
      } finally {
        setIsLoading(false);
      }
    };

    loadForumData();
  }, [forumId, router]);

  const handlePostMessage = async () => {
    if (!newMessage.trim()) return;

    try {
      setIsPosting(true);
      
      await apiClient.postForumMessage(forumId, {
        content: newMessage,
        anonymous: isAnonymous
      });

      // Reload messages
      const messagesData = await apiClient.getForumMessages(forumId);
      setMessages(messagesData.messages);
      
      // Reset form
      setNewMessage('');
      setIsAnonymous(false);
      
    } catch (error) {
      console.error('Failed to post message:', error);
      alert('Failed to post message. Please try again.');
    } finally {
      setIsPosting(false);
    }
  };

  const formatTimeAgo = (timestamp: string) => {
    const now = new Date();
    const messageTime = new Date(timestamp);
    const diffInHours = Math.floor((now.getTime() - messageTime.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Just now';
    if (diffInHours < 24) return `${diffInHours}h ago`;
    return messageTime.toLocaleDateString();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!forumInfo) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Forum Not Found</h2>
          <Link href="/community">
            <Button>
              <ArrowLeftIcon className="h-4 w-4 mr-2" />
              Back to Community
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-4">
            <div className="flex items-center space-x-4">
              <Link href="/community">
                <Button variant="outline" size="sm">
                  <ArrowLeftIcon className="h-4 w-4 mr-2" />
                  Back
                </Button>
              </Link>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{forumInfo.name}</h1>
                <p className="text-sm text-gray-600">{forumInfo.description}</p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">{forumInfo.member_count} members</div>
              <Badge className="mt-1">{forumInfo.category}</Badge>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* New Message Form */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="text-lg">Share your thoughts</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <textarea
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 resize-none"
                rows={4}
                placeholder="What would you like to share with the community?"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                disabled={isPosting}
              />
              
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <label className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      checked={isAnonymous}
                      onChange={(e) => setIsAnonymous(e.target.checked)}
                      disabled={isPosting}
                    />
                    <span className="text-sm text-gray-700 flex items-center">
                      {isAnonymous ? (
                        <>
                          <EyeSlashIcon className="h-4 w-4 mr-1" />
                          Post anonymously
                        </>
                      ) : (
                        <>
                          <EyeIcon className="h-4 w-4 mr-1" />
                          Post with your name
                        </>
                      )}
                    </span>
                  </label>
                </div>
                
                <Button 
                  onClick={handlePostMessage}
                  disabled={!newMessage.trim() || isPosting}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  {isPosting ? (
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  ) : (
                    <PaperAirplaneIcon className="h-4 w-4 mr-2" />
                  )}
                  Post Message
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Messages */}
        <div className="space-y-6">
          {messages.map((message) => (
            <Card key={message.id} className={`${message.is_pinned ? 'border-blue-200 bg-blue-50' : ''}`}>
              <CardContent className="p-6">
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    {message.author_anonymous ? (
                      <div className="h-10 w-10 bg-gray-300 rounded-full flex items-center justify-center">
                        <EyeSlashIcon className="h-5 w-5 text-gray-600" />
                      </div>
                    ) : (
                      <div className="h-10 w-10 bg-blue-600 rounded-full flex items-center justify-center">
                        <UserIcon className="h-5 w-5 text-white" />
                      </div>
                    )}
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="text-sm font-medium text-gray-900">
                        {message.author}
                      </span>
                      {message.is_pinned && (
                        <Badge variant="outline" className="text-xs">
                          Pinned
                        </Badge>
                      )}
                      <span className="text-xs text-gray-500">
                        {formatTimeAgo(message.timestamp)}
                      </span>
                    </div>
                    
                    <div className="text-gray-900 mb-4 whitespace-pre-wrap">
                      {message.content}
                    </div>
                    
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <button className="flex items-center space-x-1 hover:text-red-600 transition-colors">
                        <HeartIcon className="h-4 w-4" />
                        <span>{message.likes}</span>
                      </button>
                      
                      <button className="flex items-center space-x-1 hover:text-blue-600 transition-colors">
                        <ChatBubbleLeftIcon className="h-4 w-4" />
                        <span>{message.replies} replies</span>
                      </button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {messages.length === 0 && (
          <div className="text-center py-12">
            <ChatBubbleLeftIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-medium text-gray-900 mb-2">No messages yet</h3>
            <p className="text-gray-500 mb-4">
              Be the first to start a conversation in this forum!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}